from flask import Flask, request, send_file, render_template_string
import pandas as pd
import json
import tempfile

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Zendesk JSON → CSV</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Space Grotesk', sans-serif;
      background: #f3f4f6;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .container {
      background: white;
      padding: 2.5rem;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.08);
      text-align: center;
      width: 100%;
      max-width: 480px;
      transition: box-shadow 0.3s ease;
    }
    .container:hover {
      box-shadow: 0 12px 28px rgba(0,0,0,0.1);
    }
    h1 {
      font-weight: 600;
      font-size: 1.5rem;
      margin-bottom: 1.5rem;
      color: #111827;
    }
    input[type=file] {
      margin: 1rem 0;
      font-size: 0.95rem;
    }
    input[type=submit] {
      background: #111;
      color: white;
      padding: 0.6rem 1.2rem;
      border: none;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.95rem;
      cursor: pointer;
      transition: background 0.2s ease;
    }
    input[type=submit]:hover {
      background: #333;
    }
    @media (max-width: 500px) {
      .container {
        margin: 1rem;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Zendesk JSON → CSV</h1>
    <form action="/" method=post enctype=multipart/form-data>
      <input type=file name=file required><br>
      <input type=submit value="Convert to CSV">
    </form>
  </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if not file:
            return "No file uploaded."

        tickets = []

        for line in file:
            try:
                ticket = json.loads(line)
                ticket_id = ticket.get("id")
                comments = ticket.get("comments", [])

                convo = []
                for comment in comments:
                    author = comment.get("author_id")
                    message = comment.get("plain_body", "").strip()
                    if message:
                        convo.append(f"Author {author}: {message}")

                full_convo = "\n\n".join(convo)
                tickets.append({
                    "ticket_id": ticket_id,
                    "conversation": full_convo
                })

            except json.JSONDecodeError:
                continue

        df = pd.DataFrame(tickets)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        df.to_csv(tmp.name, index=False)

        return send_file(tmp.name, as_attachment=True, download_name="conversations.csv")

    return render_template_string(HTML_FORM)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
