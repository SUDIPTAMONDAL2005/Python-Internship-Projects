"""Task 2: Stock Portfolio Performance Tracker."""
import csv
from datetime import datetime
from pathlib import Path

CSV_FILE = Path(__file__).parent / "portfolio_summary.csv"

# Offline sample price list (no internet or API key needed).
# If a ticker is not here, the program asks you to type the current price.
SAMPLE_PRICES = {
    "AAPL": 230.00, "MSFT": 420.00, "GOOGL": 175.00, "AMZN": 190.00,
    "TSLA": 250.00, "NVDA": 130.00, "META": 520.00, "INFY": 18.50,
    "TCS": 4100.00, "RELIANCE": 2900.00,
}

portfolio = {}  # ticker -> {"shares": float, "buy_price": float, "current": float}


def ask_number(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value > 0:
                return value
            print("Enter a number greater than 0.")
        except ValueError:
            print("Invalid number. Try again.")


def get_current_price(ticker):
    if ticker in SAMPLE_PRICES:
        return SAMPLE_PRICES[ticker]
    print(f"No stored price for {ticker}.")
    return ask_number("Enter the current market price: ")


def add_position():
    ticker = input("Ticker symbol (e.g. AAPL): ").strip().upper()
    if not ticker.isalnum():
        print("Invalid ticker.")
        return
    buy_price = ask_number("Buy price per share: ")
    shares = ask_number("Number of shares: ")
    current = get_current_price(ticker)

    if ticker in portfolio:  # buying more: average the buy price
        old = portfolio[ticker]
        total_shares = old["shares"] + shares
        avg = (old["shares"] * old["buy_price"] + shares * buy_price) / total_shares
        portfolio[ticker] = {"shares": total_shares, "buy_price": avg, "current": current}
    else:
        portfolio[ticker] = {"shares": shares, "buy_price": buy_price, "current": current}
    print(f"Added {shares:g} share(s) of {ticker}.")


def remove_position():
    ticker = input("Ticker to remove: ").strip().upper()
    if portfolio.pop(ticker, None):
        print(f"{ticker} removed.")
    else:
        print("Ticker not found.")


def calculate():
    rows = []
    for ticker, p in portfolio.items():
        invested = p["shares"] * p["buy_price"]
        value = p["shares"] * p["current"]
        change = (value - invested) / invested * 100
        rows.append((ticker, p["shares"], p["buy_price"], p["current"], invested, value, change))
    total_invested = sum(r[4] for r in rows)
    total_value = sum(r[5] for r in rows)
    total_change = (total_value - total_invested) / total_invested * 100 if total_invested else 0
    return rows, total_invested, total_value, total_change


def show_summary():
    if not portfolio:
        print("Your portfolio is empty. Add a position first.")
        return
    rows, invested, value, change = calculate()
    print("\n" + "=" * 78)
    print(f"{'Ticker':<10}{'Shares':>8}{'Buy':>10}{'Now':>10}{'Invested':>12}{'Value':>12}{'Gain/Loss':>12}")
    print("-" * 78)
    for t, s, b, c, inv, val, pct in rows:
        print(f"{t:<10}{s:>8g}{b:>10.2f}{c:>10.2f}{inv:>12.2f}{val:>12.2f}{pct:>+11.2f}%")
    print("-" * 78)
    print(f"{'TOTAL':<10}{'':>8}{'':>10}{'':>10}{invested:>12.2f}{value:>12.2f}{change:>+11.2f}%")
    print("=" * 78)
    save_to_csv(rows, invested, value, change)


def save_to_csv(rows, invested, value, change):
    """Append this summary to portfolio_summary.csv with a timestamp."""
    is_new = not CSV_FILE.exists()
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["Timestamp", "Ticker", "Shares", "Buy Price",
                                 "Current Price", "Invested", "Current Value", "Gain/Loss %"])
            for t, s, b, c, inv, val, pct in rows:
                writer.writerow([stamp, t, s, round(b, 2), round(c, 2),
                                 round(inv, 2), round(val, 2), round(pct, 2)])
            writer.writerow([stamp, "TOTAL", "", "", "", round(invested, 2),
                             round(value, 2), round(change, 2)])
        print(f"Summary saved to {CSV_FILE.name}")
    except PermissionError:
        print("Could not save: close portfolio_summary.csv if it is open in Excel.")


def main():
    print("STOCK PORTFOLIO PERFORMANCE TRACKER")
    while True:
        print("\n1. Add stock   2. View summary (saves CSV)   3. Remove stock   4. Quit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_position()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            remove_position()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
