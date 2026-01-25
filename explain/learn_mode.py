import random

TIPS = [
    "Reconnaissance often precedes exploitation.",
    "Blocking early reduces attack success rates.",
    "Port scanning is commonly automated.",
    "Time-based correlation reduces false positives."
]

def print_tip():
    print(f"\n💡 Tip:\n{random.choice(TIPS)}")
