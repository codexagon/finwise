XP_REWARDS = {
    "transaction_logged": 10,
    "transaction_deleted": -5,
    "milestone_reached": 50,
    "income_bonus": 5,
}

def calculate_transaction_xp(amount, type, transaction_count):
    base_xp = XP_REWARDS["transaction_logged"]

    amount_bonus = 0
    if amount >= 1000:
        amount_bonus = 15
    elif amount >= 500:
        amount_bonus = 10
    elif amount >= 100:
        amount_bonus = 5

    income_bonus = XP_REWARDS["income_bonus"] if type == "Income" else 0
    milestone_bonus = XP_REWARDS["milestone_reached"] if transaction_count in [10, 25, 50, 100, 500, 1000] else 0

    return base_xp + amount_bonus + income_bonus + milestone_bonus