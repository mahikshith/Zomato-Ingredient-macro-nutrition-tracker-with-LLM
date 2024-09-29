import streamlit as st
import google.generativeai as genai
import os
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure the Google Gemini 1.5 Pro API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Handling image - gemini needs it is MIMe type
def byte_formatter(image):
    if image is not None:
        # Convert image to bytes
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format=image.format)  # Save the image to BytesIO buffer
        img_byte_arr = img_byte_arr.getvalue()  # Get the byte data
        
        image_parts = [
            {
                "mime_type": "image/png" if image.format.lower() == 'png' else "image/jpeg",  # Handle mime type
                "data": img_byte_arr
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image found")

def call_gemini_api(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content({
        "parts": [
            {"text": input_prompt},
            image[0]
        ]
    })
    return response.text

prompt = """
You are a nutritionist assistant. Use your imagination to answer the following questions:
 You will be given a picture of a food item , 
I want the output response in the form bullet points under different sections i.e , 
and 
Food category , ingredients - if successfully identified ingredients how many (count).
 Calories per food item or ingredients and also mention if carbohydrates, protein 
 and others ... that can be extracted from the food items or ingredients. 
 And finally in the end mention total calories, total protein, total carbohydrates 
 and so on ... (this is important).

1. What is the food item?
2. How many calories does it have?
3. Is it healthy or not?
4. Give a brief description of the food item.
    Formats the model's response into sections:
    - Food Category
    - Ingredients with count
    - Calories per food item or ingredient
    - Macronutrients (Carbohydrates, Protein, Fats)
5. In the end give out in line by line - Total calories, proteins, carbohydrates, and fats 

6. Provide other information if needed like mentioned here but not specific to (such as if it as healthy food option or not and 
specify some healthy alternative ingredients to reduce calories and fat and also Allergy Awareness in the end.)
"""

# Streamlit App UI
def main():
    
    st.set_page_config(page_title="Zomato - Food Ingredient Tracker", page_icon="🍔")

    st.subheader("Zomato Ingredient Tracker :blue[Macro Nutritionist Expert] :sunglasses:")

    
    # File uploader for image input
    uploaded_image = st.file_uploader("Upload an image of your food", type=["jpg", "jpeg", "png"])

    # Display uploaded image
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Submit button to analyze the image
    if st.button("Tell me about the food"):
        img_byte_data = byte_formatter(image)
        food_info = call_gemini_api(prompt, img_byte_data)

        st.subheader("Food Information")
        st.write(food_info)

if __name__ == "__main__":
    main()
