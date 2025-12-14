import math

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

def calculate_level(xp):
    return math.floor(math.sqrt(xp / 100)) + 1

def xp_for_level(level):
    if level <= 1:
        return 0
    return 100 * ((level - 1) ** 2)

def xp_progress_in_level(current_xp):
    current_level = calculate_level(current_xp)

    xp_for_current = xp_for_level(current_level)
    xp_for_next = xp_for_level(current_level + 1)

    xp_in_level = current_xp - xp_for_current
    xp_gap = xp_for_next - xp_for_current

    return {
        "level": current_level,
        "xp_in_level": xp_in_level,
        "xp_gap": xp_gap,
        "progress": int((xp_in_level / xp_gap) * 100) if xp_gap > 0 else 0
    }