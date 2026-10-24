"""Task 4: Rule-Based Interactive Terminal Assistant / Chatbot."""
import json
import re
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "chat_log.json"
EXIT_WORDS = {"bye", "exit", "quit"}

# Each intent: a regex of keywords and a response.
INTENTS = {
    "greeting": {
        "pattern": r"\b(hi|hello|hey|good (morning|afternoon|evening))\b",
        "response": "Hello! How can I help you today?",
    },
    "hours": {
        "pattern": r"\b(hours?|open|opening|close|closing|timings?|time)\b",
        "response": "We are open Monday to Friday, 9:00 AM to 6:00 PM, and Saturday, 10:00 AM to 2:00 PM. We are closed on Sundays.",
    },
    "products": {
        "pattern": r"\b(products?|items?|catalog|sell|offer|services?)\b",
        "response": "We offer three products: Basic Plan (Rs 499/month), Pro Plan (Rs 999/month) and Enterprise Plan (custom pricing).",
    },
    "price": {
        "pattern": r"\b(price|prices|cost|pricing|how much|fees?)\b",
        "response": "Basic is Rs 499/month, Pro is Rs 999/month. Enterprise pricing is custom, so please contact sales.",
    },
    "refund": {
        "pattern": r"\b(refund|return|money back|cancel)\b",
        "response": "You can request a refund within 14 days of purchase. Email support@example.com with your order number.",
    },
    "contact": {
        "pattern": r"\b(contact|email|phone|call|support|help desk)\b",
        "response": "Reach us at support@example.com or call +91-00000-00000 during business hours.",
    },
    "thanks": {
        "pattern": r"\b(thanks?|thank you|thx)\b",
        "response": "You're welcome! Anything else I can help with?",
    },
}

FALLBACK = ("Sorry, I didn't understand that. You can ask about our business hours, "
            "products, prices, refunds or contact details. Type 'bye' to exit.")


def normalize(text):
    """Lowercase, strip, and collapse extra spaces and punctuation."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s']", " ", text)
    return re.sub(r"\s+", " ", text)


def detect_intent(text):
    for name, data in INTENTS.items():
        if re.search(data["pattern"], text):
            return name
    return None


def get_reply(text, state):
    # Conversation state: remember the user's name.
    match = re.search(r"\b(?:my name is|i am|i'm)\s+([a-z]+)", text)
    if match:
        state["name"] = match.group(1).capitalize()
        return f"Nice to meet you, {state['name']}! How can I help?"

    if re.search(r"\bwhat('?s| is) my name\b", text):
        if state.get("name"):
            return f"Your name is {state['name']}."
        return "I don't know your name yet. Tell me with 'my name is ...'."

    intent = detect_intent(text)
    if intent is None:
        return FALLBACK

    state["last_intent"] = intent
    reply = INTENTS[intent]["response"]
    if intent == "greeting" and state.get("name"):
        reply = f"Hello again, {state['name']}! How can I help?"
    return reply


def save_log(history):
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except OSError:
        print("(Could not save chat log.)")


def main():
    state = {}
    history = []
    print("SUPPORT BOT - ask about hours, products, prices, refunds or contact.")
    print("Type 'bye', 'exit' or 'quit' to leave.\n")

    while True:
        raw = input("You: ")
        text = normalize(raw)
        if not text:
            print("Bot: Please type something.")
            continue
        if text in EXIT_WORDS:
            reply = "Goodbye! Have a great day."
            print("Bot:", reply)
            history.append({"time": datetime.now().isoformat(timespec="seconds"),
                            "user": raw, "bot": reply})
            break
        reply = get_reply(text, state)
        print("Bot:", reply)
        history.append({"time": datetime.now().isoformat(timespec="seconds"),
                        "user": raw, "bot": reply})

    save_log(history)


if __name__ == "__main__":
    main()
