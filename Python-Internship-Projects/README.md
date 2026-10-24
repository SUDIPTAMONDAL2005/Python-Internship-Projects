# Python Internship Projects

Four beginner-friendly Python console projects built with the standard library only (Python 3).

| File | Project | What it does |
|------|---------|--------------|
| `hangman.py` | Hangman Word Guessing Game | Guess a hidden word in 6 attempts with ASCII gallows art. Repeated letters do not cost an attempt. |
| `portfolio.py` | Stock Portfolio Performance Tracker | Enter tickers, buy prices and shares. Shows total value and gain/loss per holding, and logs a summary to `portfolio_summary.csv`. |
| `organizer.py` | Automated File Organizer | Sorts files into category folders (Images, Documents, ...), handles duplicate names and permission errors. |
| `chatbot.py` | Rule-Based Support Chatbot | Answers questions about hours, products, prices and refunds using regex, with fallback replies and `bye`/`exit`/`quit`. |

## How to run

```bash
python hangman.py
python portfolio.py
python organizer.py
python chatbot.py
```

On Windows, use `py` instead of `python` if needed.

## Notes
- `organizer.py` moves files. Test it on the `Organizer-Test` folder first.
- `portfolio.py` uses a built-in sample price list; unknown tickers ask for a manual price.
- `chatbot.py` saves the conversation to `chat_log.json`.

## Tools
Python 3, `random`, `csv`, `os`, `shutil`, `pathlib`, `re`, `json`.
