import csv
import re
import argparse
from collections import defaultdict


def clean_description(description):
    description = re.sub(r"(?i)apple\s*pay|apl\s*pay|aplp?ay", "", description)
    description = re.sub(r"(?i)tst\*", "", description)
    description = re.sub(r"\s+", " ", description)
    return description.strip()


def clean_text(text):
    return re.sub(r"[^A-Z0-9 ]", "", text.upper()).strip()


def extract_location(description):
    match = re.search(r"([A-Z ]+)\s([A-Z]{2})", description.upper())
    if match:
        city = match.group(1).title().strip()
        state = match.group(2)
        return f"{city}, {state}"
    return "Unknown"


def normalize_word(word):
    fixes = {
        "PIZZ": "PIZZA",
        "CHICKFILA": "CHICK FIL A",
        "CINCI": "CINCINNATI"
    }
    return fixes.get(word, word)


def extract_merchant(description):
    cleaned = clean_text(description)

    cleaned = re.sub(r"\b[A-Z]{2}\b", "", cleaned)
    cleaned = re.sub(r"\d+", "", cleaned)

    words = cleaned.split()

    location_like = {
        "MIDDLETOWN", "CINCINNATI", "CHESTER", "WEST", "MASON",
        "LIBERTY", "TOWNS", "CARMEL"
    }

    filtered = []
    for w in words:
        w = normalize_word(w)
        if w in location_like:
            continue
        if len(w) > 12:
            continue
        filtered.append(w)

    if not filtered:
        return "UNKNOWN"

    if len(filtered) >= 2:
        merchant = f"{filtered[0]} {filtered[1]}"
    else:
        merchant = filtered[0]

    return merchant.title()


def load_csv(file_path):
    transactions = []

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 3:
                continue

            date = row[0].strip()
            description = clean_description(row[1].strip())
            amount = row[2].strip()

            transactions.append({
                "date": date,
                "description": description,
                "amount": amount
            })

    return transactions


def process_transactions(transactions):
    grouped = defaultdict(list)
    enriched = []

    for t in transactions:
        if "date" not in t or "description" not in t or "amount" not in t:
            continue

        try:
            date = t["date"]
            desc = t["description"]
            amount = float(t["amount"])
        except:
            continue

        merchant = extract_merchant(desc)
        location = extract_location(desc)
        category = merchant

        enriched.append({
            "date": date,
            "description": desc,
            "merchant": merchant,
            "category": category,
            "location": location,
            "amount": amount
        })

        grouped[merchant].append(amount)

    return enriched, grouped


def print_summary(grouped):
    print("\n=== SPENDING SUMMARY ===")
    for merchant, amounts in grouped.items():
        print(f"{merchant}: ${sum(amounts):.2f}")


def print_locations(transactions):
    print("\n=== LOCATIONS FOUND ===")
    seen = set()

    for t in transactions:
        loc = t["location"]
        if loc != "Unknown" and loc not in seen:
            print(f"- {loc} ({t['merchant']})")
            seen.add(loc)


def main():
    parser = argparse.ArgumentParser(description="Bank Statement Analyzer")

    parser.add_argument("--file", required=True)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--locations", action="store_true")

    args = parser.parse_args()

    transactions = load_csv(args.file)
    enriched, grouped = process_transactions(transactions)

    if args.summary:
        print_summary(grouped)

    if args.locations:
        print_locations(enriched)

    if not args.summary and not args.locations:
        print("No output selected. Use --summary or --locations.")


if __name__ == "__main__":
    main()