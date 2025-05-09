# Zendesk JSON to CSV Converter

A simple web tool for Seymour Duncan's Customer Service team to convert Zendesk ticket exports (in JSON format) into clean, readable CSV files.

Built with Flask and Pandas, this tool extracts relevant conversations from Zendesk export files and formats them for easy review.

## 🚀 Features

- Upload a `.json` file exported from Zendesk
- Extracts ticket ID and comment history
- Outputs a `.csv` file with one row per ticket
- Clean, modern UI for internal use
- Fast, secure, and easy to deploy

## 🛠 Tech Stack

- Python 3
- Flask
- Pandas
- HTML/CSS (with Google Fonts)

## 📦 Requirements

Install dependencies:
```bash
pip install -r requirements.txt
