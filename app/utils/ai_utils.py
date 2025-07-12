from transformers import pipeline

generator = pipeline("text2text-generation", model="flax-community/t5-recipe-generation")

def generate_recipe(prompt):
    try:
        output = generator(prompt, max_new_tokens=300, num_return_sequences=1)
        text = output[0]['generated_text']

        # Return a structured response
        return {
            'title': 'Generated Recipe',
            'ingredients': [],
            'instructions': text,
            'cook_time': 'N/A',
            'nutrition_text': 'Estimate not available'
        }

    except Exception as e:
        return {
            'title': 'Error',
            'ingredients': [],
            'instructions': f"⚠️ Error: {e}",
            'cook_time': 'N/A',
            'nutrition_text': 'Estimate not available'
        }
