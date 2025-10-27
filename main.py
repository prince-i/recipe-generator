import streamlit as st
from PIL import Image
import io
from google import genai

# Initialize the Gemini API client
client = genai.Client()

# Function to call the Gemini API for recipe generation
def get_recipe_from_image(image, api_token):
    # First, convert the image to a suitable format (base64 or binary) for the API.
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # You may need to adjust this API call to correctly handle image processing in Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # Specify the Gemini model you're using
        contents="Generate a recipe based on this image",  # You might need to refine this prompt
        image_data=img_byte_arr,  # Image data to send to the model
    )
    
    return response

# Streamlit app interface
def app():
    st.title("Recipe Generator")
    st.write("Upload an image of an ingredient or dish, and we'll generate a recipe for you!")

    # User inputs the API token here
    api_token = st.text_input("Enter your Gemini API Token:", type="password")

    if not api_token:
        st.warning("Please enter your API token to proceed.")
        return

    # Button to open camera or upload file
    image_file = st.file_uploader("Upload an image of a dish or ingredient", type=["jpg", "jpeg", "png"])

    if image_file is not None:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Generate recipe when the user uploads an image
        if st.button("Generate Recipe"):
            st.write("Generating recipe... Please wait.")
            
            # Call the Gemini API to generate the recipe
            recipe_data = get_recipe_from_image(image, api_token)
            
            if recipe_data:
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
