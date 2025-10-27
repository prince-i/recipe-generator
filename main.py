import streamlit as st
from PIL import Image
import io
from google import genai

# Hardcode your Gemini API token here
API_TOKEN = "YOUR_GEMINI_API_TOKEN_HERE"  # Replace with your actual API token

# Initialize the Gemini API client using the hardcoded API token
def get_gemini_client(api_token):
    """ Initialize the Gemini API client with the provided API token. """
    return genai.Client(api_key=api_token)

# Function to call the Gemini API for recipe generation
def get_recipe_from_image(image):
    # Initialize the Gemini client using the hardcoded API token
    client = get_gemini_client(API_TOKEN)

    # Convert the uploaded image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Generate the recipe content using Gemini API
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Specify the Gemini model
            contents="Generate a recipe based on this image",  # You can customize this prompt
            image_data=img_byte_arr  # Image data to send to the model
        )
        return response
    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return None

# Streamlit app interface
def app():
    st.title("Recipe Generator")
    st.write("Upload an image of an ingredient or dish, and we'll generate a recipe for you!")

    # Button to open camera or upload file
    image_file = st.file_uploader("Upload an image of a dish or ingredient", type=["jpg", "jpeg", "png"])

    if image_file is not None:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Generate recipe when the user uploads an image
        if st.button("Generate Recipe"):
            st.write("Generating recipe... Please wait.")
            
            # Call Gemini API to generate the recipe
            recipe_data = get_recipe_from_image(image)
            
            if recipe_data:
                # Displaying the generated recipe
                st.subheader("Recipe Name:")
                st.write(recipe_data.get('name', 'N/A'))

                st.subheader("Ingredients:")
                ingredients = recipe_data.get('ingredients', [])
                if ingredients:
                    st.write(", ".join(ingredients))
                else:
                    st.write("Ingredients not found.")
                
                st.subheader("Instructions:")
                instructions = recipe_data.get('instructions', 'Instructions not available.')
                st.write(instructions)
                
            else:
                st.error("Could not generate recipe, please try again.")
    
    else:
        st.write("Please upload an image to generate a recipe.")

# Run the app
if __name__ == "__main__":
    app()
