# AskEmploymentLaw
AskEmploymentLaw is a ChatGPT like application for employment law QnA. Currently for Indonesian.

[![AskEmploymentLaw Testing](https://github.com/jalalAzhmatkhan/AskEmploymentLaw/actions/workflows/lint.yml/badge.svg)](https://github.com/jalalAzhmatkhan/AskEmploymentLaw/actions/workflows/lint.yml)

## How to Run
### Without Docker
1. Please use Python 3.10.
2. Create a new virtual environment:
    `pip3.10 -m venv venv`
    and activate it:
    `source venv/bin/activate` (Linux)
    `venv\Scripts\activate` (Windows)
3. Install dependencies listed on the `requirements.txt` file:
    `pip install -r requirements.txt`
4. Run DB migration: `alembic upgrade head`
5. Install Firefox for Playwright: `playwright install firefox`

## Engineer
1. Data Scientist: Jalaluddin Al Mursyidy Fadhlurrahman Azhmatkhan
