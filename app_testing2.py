from flask import Flask, render_template, request, jsonify
import openai
import os

# export OPENAI_API_KEY=
openai.api_key = os.getenv('OPENAI_API_KEY')
# and if network unreachable error just generate and use new key

app = Flask(__name__)

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
    "beef": ["lentils", "mushrooms"],
    "cheddar cheese": ["vegan cheese", "nutritional yeast"],
    "wheat flour": ["almond flour", "coconut flour"],
    "sugar": ["honey", "stevia"],
    "soy sauce": ["coconut aminos", "tamari"],
    "mayonnaise": ["mashed avocado", "hummus"],
    "sour cream": ["yogurt", "cashew cream"],
    "cream": ["coconut cream", "cashew cream"],
    "fish sauce": ["soy sauce", "miso paste"],
    "bread crumbs": ["crushed nuts", "oats"],
    "pasta": ["zucchini noodles", "spaghetti squash"],
    "egg (for baking)": ["applesauce", "chia seeds"],
    "peanut butter": ["almond butter", "sunflower seed butter"],
    "soy products": ["seitan", "jackfruit"],
    "salt": ["herbs", "lemon juice"],
    "cream cheese": ["cashew cheese", "tofu spread"],
    "yogurt": ["coconut yogurt", "soy yogurt"],
    "rice": ["cauliflower rice", "quinoa"],
    "ground beef": ["textured vegetable protein", "lentils"],
    "shrimp": ["tofu", "jackfruit"],
}

def filter_ingredients(available, restrictions):
    filtered = {}
    for ingredient, details in available.items():
        if ingredient not in restrictions:
            filtered[ingredient] = details
    return filtered

def suggest_substitutions(restrictions):
    suggestions = {}
    for item in restrictions:
        if item in SUBSTITUTIONS:
            suggestions[item] = SUBSTITUTIONS[item]
    return suggestions

@app.route('/')
def index():
    return render_template('index_testing.html')

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.json
    ingredients = data.get("ingredients")
    restrictions = data.get("restrictions", [])

    available_ingredients = {ing: INGREDIENTS[ing] for ing in ingredients if ing in INGREDIENTS}
    filtered_ingredients = filter_ingredients(available_ingredients, restrictions)

    if not filtered_ingredients:
        return jsonify({"error": "No valid ingredients after filtering with restrictions."})

    recipe_response = generate_recipe_api(list(filtered_ingredients.keys()))

    # Extract recipe name from recipe_response
    recipe_name = recipe_response.split("\n")[0]

    instructions_text = create_instructions_api(recipe_name, list(filtered_ingredients.keys()))
    nutrition_info = calculate_nutrition(filtered_ingredients)

    return jsonify({
        "recipe_name": recipe_name,
        "recipe": recipe_response,
        "instructions": instructions_text,
        "nutrition": nutrition_info
    })

@app.route('/generate_recipe_vegetarian', methods=['POST'])
def generate_recipe_vegetarian():
    data = request.json
    ingredients = data.get("ingredients")
    restrictions = data.get("restrictions", [])

    # Add non-vegetarian ingredients to restrictions
    non_vegetarian = ["beef", "chicken breast", "salmon", "egg", "milk", "cheddar cheese", "yogurt"]
    restrictions.extend(non_vegetarian)

    available_ingredients = {ing: INGREDIENTS[ing] for ing in ingredients if ing in INGREDIENTS}
    filtered_ingredients = filter_ingredients(available_ingredients, restrictions)

    if not filtered_ingredients:
        return jsonify({"error": "No valid vegetarian ingredients after filtering with restrictions."})

    recipe_response = generate_vegetarian_recipe_api(list(filtered_ingredients.keys()))

    # Extract recipe name from recipe_response
    recipe_name = recipe_response.split("\n")[0]

    instructions_text = create_instructions_api(recipe_name, list(filtered_ingredients.keys()))
    nutrition_info = calculate_nutrition(filtered_ingredients)

    return jsonify({
        "recipe_name": recipe_name,
        "recipe": recipe_response,
        "instructions": instructions_text,
        "nutrition": nutrition_info
    })

def generate_recipe_api(ingredients_list, max_calories=700, min_calories=250):
    ingredient_names = ', '.join(ingredients_list)
    prompt = (
        f"Create a healthy and creative recipe using the following ingredients: {ingredient_names}. "
        f"The recipe should be between {min_calories} and {max_calories} calories per serving. "
        "Provide the recipe name, a list of ingredients with quantities, and a brief description. "
        "Try to make a healthy recipe with low fat, high protein, and medium carbohydrates in general."
    )
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini', 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,  # for testing and building now but adjust when submitting 
            temperature=0.7,
            n=1,
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"An error occurred: {e}"

def generate_vegetarian_recipe_api(ingredients_list, max_calories=700, min_calories=250):
    ingredient_names = ', '.join(ingredients_list)
    prompt = (
        f"Create a healthy and creative vegetarian recipe using the following ingredients: {ingredient_names}. "
        f"The recipe should be between {min_calories} and {max_calories} calories per serving. "
        "Provide the recipe name, a list of ingredients with quantities, and a brief description. "
        "Ensure all ingredients are vegetarian. Try to make a healthy recipe with low fat, high protein, and medium carbohydrates in general."
    )
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini', 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,  # for testing and building now but adjust when submitting 
            temperature=0.7,
            n=1,
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"An error occurred: {e}"

def create_instructions_api(recipe_name, ingredients_list):
    ingredient_names = ', '.join(ingredients_list)
    prompt = (
        f"Provide detailed, step-by-step cooking instructions for the recipe '{recipe_name}' "
        f"using the following ingredients: {ingredient_names}. "
        "Include any necessary preparation and cooking times."
    )
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4o-mini', 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,   # for testing and building now but adjust when submitting 
            temperature=0.7,
            n=1,
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"An error occurred: {e}"

def calculate_nutrition(filtered_ingredients):
    total_calories = sum([INGREDIENTS[ing]['calories'] for ing in filtered_ingredients])
    total_protein = sum([INGREDIENTS[ing]['protein'] for ing in filtered_ingredients])
    total_fat = sum([INGREDIENTS[ing]['fat'] for ing in filtered_ingredients])
    total_carbs = sum([INGREDIENTS[ing]['carbs'] for ing in filtered_ingredients])

    return {
        "calories": total_calories,
        "protein": total_protein,
        "fat": total_fat,
        "carbohydrates": total_carbs
    }

if __name__ == '__main__':
    app.run(debug=True)
