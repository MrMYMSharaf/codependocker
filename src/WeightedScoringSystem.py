import math
import numpy as np  # Ensure NumPy is available

def calculate_interest(users, name):
    """
    Determines the category in which a specific user is most interested based on weighted scoring.
    
    :param users: List of dictionaries containing transaction data for each user.
    :param name: The selected user name.
    :return: The most interested category or an error message.
    """

    if not users:
        return "No data available"

    # Find the user in the dataset
    user_data = next((user for user in users if user.get("Name") == name), None)

    if not user_data:
        return f"User '{name}' not found."

    # Define transaction categories
    categoriesVolume = ['Online Shopping(Volume)', 'Super Market(Volume)', 'Grocery(Volume)', 
                        'Travelling(Volume)', 'Payments(Volume)', 'Other(Volume)']
    categoriesCount = ['Online Shopping(Count)', 'Super Market(Count)', 'Grocery(Count)', 
                       'Travelling(Count)', 'Payments(Count)', 'Other(Count)']

    # Find max values for normalization, replacing NaN with 1 to avoid zero division
    max_counts = {
        cat: max((user.get(cat, 0) for user in users if not math.isnan(user.get(cat, 0))), default=1)
        for cat in categoriesCount
    }
    max_volumes = {
        cat: max((user.get(cat, 0) for user in users if not math.isnan(user.get(cat, 0))), default=1)
        for cat in categoriesVolume
    }

    print(f"DEBUG - Max Counts: {max_counts}")
    print(f"DEBUG - Max Volumes: {max_volumes}")

    scores = {}

    for count_category, volume_category in zip(categoriesCount, categoriesVolume):
        count_value = user_data.get(count_category, 0)
        volume_value = user_data.get(volume_category, 0)

        # Convert NaN values to 0
        count_value = 0 if math.isnan(count_value) else count_value
        volume_value = 0 if math.isnan(volume_value) else volume_value

        count_norm = count_value / max_counts[count_category] if max_counts[count_category] else 0
        volume_norm = volume_value / max_volumes[volume_category] if max_volumes[volume_category] else 0

        # Weighted Score Calculation (60% count + 40% volume)
        scores[count_category] = (count_norm * 0.6) + (volume_norm * 0.4)

    # Debugging output to check scores
    print(f"DEBUG - Scores for {name}: {scores}")

    # Remove NaN values from scores by replacing them with 0
    scores = {k: (v if not math.isnan(v) else 0) for k, v in scores.items()}

    # Determine the category with the highest score
    interest_category = max(scores, key=scores.get)

    # Return formatted category name
    return interest_category.replace("(Count)", "").title()
