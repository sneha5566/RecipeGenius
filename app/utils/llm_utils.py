# utils/llm_utils.py

from transformers import pipeline

nutrition_generator = pipeline("text2text-generation", 
    model="google/flan-t5-base")  # Replace with better model if desired

def generate_nutrition(dish_name):
    prompt = (
       
        f"Provide nutritional facts for {dish_name}. List the following in bullet points:\n"
        f"- Calories\n- Protein (g)\n- Carbohydrates (g)\n- Fat (g)\n- Vitamins A, B, C, and D"
        
    )
    output = nutrition_generator(prompt, max_length=150, do_sample=True, temperature=0.3)[0]['generated_text']
    return output
