import openai
import os

# open AI api key inside my env (printenv, export OPENAI_API_KEY=)
openai.api_key = os.getenv('OPENAI_API_KEY')

INGREDIENTS = {
    "beef": {"calories": 250, "protein": 26, "fat": 15, "carbs": 0, "unit": "100g"},
    "cheddar cheese": {"calories": 402, "protein": 25, "fat": 33, "carbs": 1.3, "unit": "100g"},
    "bell pepper": {"calories": 31, "protein": 1, "fat": 0.3, "carbs": 6, "unit": "100g"},
    "cucumber": {"calories": 16, "protein": 0.7, "fat": 0.1, "carbs": 3.6, "unit": "100g"},
    "tomato": {"calories": 18, "protein": 0.9, "fat": 0.2, "carbs": 3.9, "unit": "100g"},
    "apple": {"calories": 52, "protein": 0.3, "fat": 0.2, "carbs": 14, "unit": "100g"},
    "banana": {"calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 23, "unit": "100g"},
    "almonds": {"calories": 579, "protein": 21, "fat": 50, "carbs": 22, "unit": "100g"},
    "yogurt": {"calories": 59, "protein": 10, "fat": 0.4, "carbs": 3.6, "unit": "100g"},
    "peanut butter": {"calories": 588, "protein": 25, "fat": 50, "carbs": 20, "unit": "100g"},
    "avocado": {"calories": 160, "protein": 2, "fat": 15, "carbs": 9, "unit": "100g"},
    "mushroom": {"calories": 22, "protein": 3.1, "fat": 0.3, "carbs": 3.3, "unit": "100g"},
    "chickpeas": {"calories": 164, "protein": 8.9, "fat": 2.6, "carbs": 27, "unit": "100g"},
    "oats": {"calories": 389, "protein": 16.9, "fat": 6.9, "carbs": 66, "unit": "100g"},
    "milk": {"calories": 42, "protein": 3.4, "fat": 1, "carbs": 5, "unit": "100g"},
    "chicken breast": {"calories": 165, "protein": 31, "fat": 3.6, "carbs": 0, "unit": "100g"},
    "broccoli": {"calories": 55, "protein": 3.7, "fat": 0.6, "carbs": 11, "unit": "100g"},
    "carrot": {"calories": 41, "protein": 0.9, "fat": 0.2, "carbs": 10, "unit": "100g"},
    "rice": {"calories": 130, "protein": 2.4, "fat": 0.2, "carbs": 28, "unit": "100g"},
    "olive oil": {"calories": 884, "protein": 0, "fat": 100, "carbs": 0, "unit": "100g"},
    "garlic": {"calories": 149, "protein": 6.4, "fat": 0.5, "carbs": 33, "unit": "100g"},
    "onion": {"calories": 40, "protein": 1.1, "fat": 0.1, "carbs": 9.3, "unit": "100g"},
    "potato": {"calories": 77, "protein": 2, "fat": 0.1, "carbs": 17, "unit": "100g"},
    "spinach": {"calories": 23, "protein": 2.9, "fat": 0.4, "carbs": 3.6, "unit": "100g"},
    "tofu": {"calories": 76, "protein": 8, "fat": 4.8, "carbs": 1.9, "unit": "100g"},
    "salmon": {"calories": 208, "protein": 20, "fat": 13, "carbs": 0, "unit": "100g"},
    "lentils": {"calories": 116, "protein": 9, "fat": 0.4, "carbs": 20, "unit": "100g"},
    "quinoa": {"calories": 120, "protein": 4.4, "fat": 1.9, "carbs": 21, "unit": "100g"},
    "egg": {"calories": 155, "protein": 13, "fat": 11, "carbs": 1.1, "unit": "100g"},
}


SUBSTITUTIONS = {
    "chicken breast": ["tofu", "lentils"],
    "milk": ["soy milk", "almond milk"],
    "butter": ["olive oil", "coconut oil"],
    "egg": ["banana", "flaxseed"],
}

# Function to filter ingredients based on dietary restrictions
def filter_ingredients(available, restrictions):
    filtered = {}
    for ingredient, details in available.items():
        if ingredient not in restrictions:
            filtered[ingredient] = details
    return filtered

# Function to suggest substitutions for restricted ingredients
def suggest_substitutions(restrictions):
    suggestions = {}
    for item in restrictions:
        if item in SUBSTITUTIONS:
            suggestions[item] = SUBSTITUTIONS[item]
    return suggestions

# open AI API basic usage
# modify prompting 
def generate_recipe(ingredients_list, max_calories=700, min_calories=250):
    ingredient_names = ', '.join(ingredients_list)
    prompt = (
        f"Create a creative and healthy recipe using the following ingredients: {ingredient_names}. "
        f"The recipe should be under {max_calories} and higher {min_calories} calories per serving"
        "Provide the recipe name, a list of ingredients with quantities, and a brief description."
    )
    
    response = openai.ChatCompletion.create(
        model='gpt-4o',  
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500, # I think this is already enough 
        temperature=0.7,
        n=1,
    )
    
    recipe_text = response['choices'][0]['message']['content'].strip()
    return recipe_text

# creat instructions how to make the recipe 
def create_instructions(recipe_name, ingredients_list):
    ingredient_names = ', '.join(ingredients_list)
    prompt = (
        f"Provide detailed, step-by-step cooking instructions for the recipe '{recipe_name}' "
        f"using the following ingredients: {ingredient_names}. "
        "Include any necessary preparation and cooking times."
    )
    
    response = openai.ChatCompletion.create(
        model='gpt-4o',  # Use 'gpt-4' if you have access
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
        n=1,
    )
    
    instructions_text = response['choices'][0]['message']['content'].strip()
    return instructions_text

# Main program
def main():
    print("Welcome to the Enhanced Healthy Meal Planner!")

    # Get user's available ingredients
    print("\nPlease enter the ingredients you have available (comma-separated):")
    user_ingredients_input = input("> ").lower()
    user_ingredients = [item.strip() for item in user_ingredients_input.split(",")]

    # Validate ingredients
    available_ingredients = {}
    for ingredient in user_ingredients:
        if ingredient in INGREDIENTS:
            available_ingredients[ingredient] = INGREDIENTS[ingredient]
        else:
            print(f"Ingredient '{ingredient}' not recognized and will be ignored.")

    if not available_ingredients:
        print("No valid ingredients entered. Exiting.")
        return

    # Get dietary restrictions
    print("\nEnter any dietary restrictions (comma-separated, e.g., 'tofu, egg'):")
    restrictions_input = input("> ").lower()
    restrictions = [item.strip() for item in restrictions_input.split(",")] if restrictions_input else []

    # Filter ingredients
    filtered_ingredients = filter_ingredients(available_ingredients, restrictions)

    if not filtered_ingredients:
        print("No ingredients available after applying restrictions. Exiting.")
        return

    # Suggest substitutions
    substitutions = suggest_substitutions(restrictions)
    if substitutions:
        print("\nSubstitution Suggestions:")
        for restricted_item, alternatives in substitutions.items():
            print(f" - {restricted_item}: Try using {', '.join(alternatives)} instead.")

    # Generate recipe using OpenAI API
    print("\nGenerating a creative recipe...")
    ingredients_list = list(filtered_ingredients.keys())
    recipe_text = generate_recipe(ingredients_list)

    # Display the recipe
    print(f"\n--- Recipe ---\n{recipe_text}")

    # Display nutritional information (sum up the ingredients)
    total_calories = sum([INGREDIENTS[ing]['calories'] for ing in filtered_ingredients])
    total_protein = sum([INGREDIENTS[ing]['protein'] for ing in filtered_ingredients])
    total_fat = sum([INGREDIENTS[ing]['fat'] for ing in filtered_ingredients])
    total_carbs = sum([INGREDIENTS[ing]['carbs'] for ing in filtered_ingredients])

    print("\n--- Nutritional Information ---")
    print(f"Calories: {total_calories} kcal")
    print(f"Protein: {total_protein} g")
    print(f"Fat: {total_fat} g")
    print(f"Carbohydrates: {total_carbs} g")

if __name__ == "__main__":
    main()
