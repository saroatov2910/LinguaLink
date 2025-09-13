# Import the Google Generative AI library
import google.generativeai as genai
# Import the Gemini API key from the configuration file
from src.config import GEMINI_API_KEY

# Configure the library with your API key
genai.configure(api_key=GEMINI_API_KEY)
# Create an instance of the Generative Model
model = genai.GenerativeModel('gemini-1.5-flash')

def translate_text_gemini(text, source_lang, target_lang):
    """
    Translates text using the Gemini API.
    
    Args:
        text (str): The text to translate.
        source_lang (str): The source language of the text.
        target_lang (str): The target language for the translation.
        
    Returns:
        str: The translated text, or the original text if an error occurs.
    """
    try:
        # Create a specific prompt for conversational translation.
        # This helps the model provide a clean translation without extra text.
        prompt = f"Translate this for a WhatsApp conversation, from {source_lang} to {target_lang}. Give only the translation and nothing else: '{text}'"
        # Generate content using the model
        response = model.generate_content(prompt)
        # Return the translated text
        return response.text
    except Exception as e:
        # Print any errors that occur during the translation process
        print(f"An error occurred during translation: {e}")
        # Return the original text as a fallback
        return text
