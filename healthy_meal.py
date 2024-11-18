import tkinter as tk
from tkinter import ttk, messagebox
import threading
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healthy Meal Planner")
        self.root.configure(bg="#f0f0f0")
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)

        header_label = tk.Label(main_frame, text="Healthy Meal Planner", font=("Helvetica", 19, "bold"), bg="#f0f0f0")
        header_label.pack(pady=10)

        ingredients_frame = tk.Frame(main_frame, bg="#ffffff", padx=10, pady=10, relief="groove", bd=2)
        ingredients_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        ingredients_label = ttk.Label(ingredients_frame, text="Enter available ingredients (comma-separated):", font=("Helvetica", 10, "bold"), background="#ffffff")
        ingredients_label.pack(anchor="w")

        self.ingredients_text = tk.Text(ingredients_frame, height=4, width=50, font=("Helvetica", 10))
        self.ingredients_text.pack(fill=tk.X, pady=5)

        restrictions_frame = tk.Frame(main_frame, bg="#ffffff", padx=10, pady=10, relief="groove", bd=2)
        restrictions_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        restrictions_label = ttk.Label(restrictions_frame, text="Enter dietary restrictions (comma-separated):", font=("Helvetica", 10, "bold"), background="#ffffff")
        restrictions_label.pack(anchor="w")

        self.restrictions_entry = ttk.Entry(restrictions_frame, font=("Helvetica", 10))
        self.restrictions_entry.pack(fill=tk.X, pady=5)

        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.BOTH, pady=10)

        generate_button = ttk.Button(button_frame, text="Generate Recipe", command=self.generate_recipe)
        generate_button.pack(pady=10)

        recipe_frame = tk.Frame(main_frame, bg="#ffffff", padx=10, pady=10, relief="groove", bd=2)
        recipe_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        recipe_label = ttk.Label(recipe_frame, text="Recipe:", font=("Helvetica", 12, "bold"), background="#ffffff")
        recipe_label.pack(anchor="w")

        self.recipe_output = tk.Text(recipe_frame, height=6, font=("Helvetica", 10))
        self.recipe_output.pack(fill=tk.BOTH, pady=5)

        instructions_frame = tk.Frame(main_frame, bg="#ffffff", padx=10, pady=10, relief="groove", bd=2)
        instructions_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        instructions_label = ttk.Label(instructions_frame, text="Instructions:", font=("Helvetica", 12, "bold"), background="#ffffff")
        instructions_label.pack(anchor="w")

        self.instructions_output = tk.Text(instructions_frame, height=10, font=("Helvetica", 10))
        self.instructions_output.pack(fill=tk.BOTH, pady=5)

        nutrition_frame = tk.Frame(main_frame, bg="#ffffff", padx=10, pady=10, relief="groove", bd=2)
        nutrition_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        nutrition_label = ttk.Label(nutrition_frame, text="Nutritional Information:", font=("Helvetica", 12, "bold"), background="#ffffff")
        nutrition_label.pack(anchor="w")

        self.nutrition_output = tk.Text(nutrition_frame, height=4, font=("Helvetica", 10))
        self.nutrition_output.pack(fill=tk.BOTH, pady=5)

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

    def filter_ingredients(self, available, restrictions):
        filtered = {}
        for ingredient, details in available.items():
            if ingredient not in restrictions:
                filtered[ingredient] = details
        return filtered

    def suggest_substitutions(self, restrictions):
        suggestions = {}
        for item in restrictions:
            if item in self.SUBSTITUTIONS:
                suggestions[item] = self.SUBSTITUTIONS[item]
        return suggestions

    def generate_recipe(self):
        ingredients_input = self.ingredients_text.get("1.0", tk.END).lower()
        restrictions_input = self.restrictions_entry.get().lower()

        user_ingredients = [item.strip() for item in ingredients_input.split(",") if item.strip()]
        restrictions = [item.strip() for item in restrictions_input.split(",")] if restrictions_input else []

        available_ingredients = {}
        for ingredient in user_ingredients:
            if ingredient in self.INGREDIENTS:
                available_ingredients[ingredient] = self.INGREDIENTS[ingredient]
            else:
                messagebox.showwarning("Warning", f"Ingredient '{ingredient}' not recognized and will be ignored.")

        if not available_ingredients:
            messagebox.showerror("Error", "No valid ingredients entered.")
            return

        filtered_ingredients = self.filter_ingredients(available_ingredients, restrictions)

        if not filtered_ingredients:
            messagebox.showerror("Error", "No ingredients available after applying restrictions.")
            return

        substitutions = self.suggest_substitutions(restrictions)
        if substitutions:
            subs_message = "\n".join([f"{item}: Try using {', '.join(alts)} instead." for item, alts in substitutions.items()])
            messagebox.showinfo("Substitution Suggestions", subs_message)

        self.recipe_output.delete("1.0", tk.END)
        self.instructions_output.delete("1.0", tk.END)
        self.nutrition_output.delete("1.0", tk.END)

        self.recipe_output.insert(tk.END, "Generating recipe, please wait...\n")
        self.root.update_idletasks()

        threading.Thread(target=self.generate_and_display_recipe, args=(filtered_ingredients,)).start()

    def generate_and_display_recipe(self, filtered_ingredients):
        ingredients_list = list(filtered_ingredients.keys())

        recipe_text = self.generate_recipe_api(ingredients_list)

        if not recipe_text:
            return

        self.recipe_output.delete("1.0", tk.END)
        self.recipe_output.insert(tk.END, recipe_text)

        recipe_name_line = recipe_text.split("\n")[0]
        recipe_name = recipe_name_line.replace("Recipe Name:", "").strip()

        instructions_text = self.create_instructions_api(recipe_name, ingredients_list)

        if not instructions_text:
            return

        self.instructions_output.delete("1.0", tk.END)
        self.instructions_output.insert(tk.END, instructions_text)

        total_calories = sum([self.INGREDIENTS[ing]['calories'] for ing in filtered_ingredients])
        total_protein = sum([self.INGREDIENTS[ing]['protein'] for ing in filtered_ingredients])
        total_fat = sum([self.INGREDIENTS[ing]['fat'] for ing in filtered_ingredients])
        total_carbs = sum([self.INGREDIENTS[ing]['carbs'] for ing in filtered_ingredients])

        nutrition_info = (
            f"Calories: {total_calories} kcal\n"
            f"Protein: {total_protein} g\n"
            f"Fat: {total_fat} g\n"
            f"Carbohydrates: {total_carbs} g"
        )

        self.nutrition_output.delete("1.0", tk.END)
        self.nutrition_output.insert(tk.END, nutrition_info)

    def generate_recipe_api(self, ingredients_list, max_calories=700, min_calories = 250):
        ingredient_names = ', '.join(ingredients_list)
        prompt = (
            f"Create a creative and healthy recipe using the following ingredients: {ingredient_names}. "
            f"The recipe should be under {max_calories} and higher {min_calories} calories per serving."
            "Provide the recipe name, a list of ingredients with quantities, and a brief description."
        )
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4o',
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
                n=1,
            )
            recipe_text = response['choices'][0]['message']['content'].strip()
            return recipe_text
        except openai.error.OpenAIError as e:
            messagebox.showerror("API Error", f"An error occurred: {e}")
            return ""

    def create_instructions_api(self, recipe_name, ingredients_list):
        ingredient_names = ', '.join(ingredients_list)
        prompt = (
            f"Provide detailed, step-by-step cooking instructions for the recipe '{recipe_name}' "
            f"using the following ingredients: {ingredient_names}. "
            "Include any necessary preparation and cooking times."
        )
        try:
            response = openai.ChatCompletion.create(
                model='gpt-4o',
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
                n=1,
            )
            instructions_text = response['choices'][0]['message']['content'].strip()
            return instructions_text
        except openai.error.OpenAIError as e:
            messagebox.showerror("API Error", f"An error occurred: {e}")
            return ""

if __name__ == "__main__":
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()
