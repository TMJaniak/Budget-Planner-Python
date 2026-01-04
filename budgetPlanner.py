# budgetPlanner.py

def read_month_file(filename):
    category_totals = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    continue  
                _, amount_str, category = parts
                amount = float(amount_str)
                category = category.strip()

                if category not in category_totals:
                    category_totals[category] = 0.0
                category_totals[category] += amount
    except FileNotFoundError:
        return {}
    return category_totals


def calculate_budget(selected_months):
    """Given a list of valid month names (e.g. ['jan', 'feb']),
       calculate and return:
       (regular_budget_dict, sinking_fund_amount, sinking_categories_set)
       or (None, None, None) if insufficient data.
    """
    num_months = len(selected_months)
    if num_months <= 1:
        return None, None, None

    category_totals = {}
    category_month_count = {}

    month_to_file = {
        "jan": "jan_expenses.txt",
        "feb": "feb_expenses.txt",
        "mar": "mar_expenses.txt",
        "apr": "apr_expenses.txt",
        "may": "may_expenses.txt",
    }

    for month in selected_months:
        filename = month_to_file[month]
        month_data = read_month_file(filename)

        for cat, amt in month_data.items():
            if cat not in category_totals:
                category_totals[cat] = 0.0
            category_totals[cat] += amt

        for cat in month_data:
            if cat not in category_month_count:
                category_month_count[cat] = 0
            category_month_count[cat] += 1

    regular_budget = {}
    sinking_categories = set()

    for cat, count in category_month_count.items():
        if count > 1:
            regular_budget[cat] = category_totals[cat] / num_months
        else:
            sinking_categories.add(cat)

    sinking_total = 0.0
    for cat in sinking_categories:
        sinking_total += category_totals[cat]
    sinking_fund_amount = sinking_total / num_months

    return regular_budget, sinking_fund_amount, sinking_categories


def main():
    month_to_file = {
        "jan": "jan_expenses.txt",
        "feb": "feb_expenses.txt",
        "mar": "mar_expenses.txt",
        "apr": "apr_expenses.txt",
        "may": "may_expenses.txt",
    }

    user_input = input("Which months' expenses should be used to plan the budget: ")
    raw_months = user_input.split(",")

    selected_months = []
    for m in raw_months:
        month = m.strip().lower()
        if not month:
            continue
        if month in month_to_file:
            selected_months.append(month)
        else:
            print(f"You do not have the expenses record for {month}.")

    regular_budget, sinking_fund, sinking_categories = calculate_budget(selected_months)

    if regular_budget is None:
        if len(selected_months) == 0:
            print("Insufficient data to calculate the budget. None of the months you entered exist.")
        else:
            print("Insufficient data to calculate the budget. You selected only one valid month.")
        return

    print("Based on the analysis of your expenses for the selected months, "
          "your budget is calculated as follows:")

    for cat in sorted(regular_budget.keys()):
        print(f"{cat}: ${regular_budget[cat]:.2f}")

    print()
    print(f"Finally, you should leave ${sinking_fund:.2f} as sinking fund for occasional spending, "
          "such as things in the categories of:")
    for cat in sorted(sinking_categories):
        print(f"    {cat}")


if __name__ == "__main__":
    main()
