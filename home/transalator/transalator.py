from dotenv import load_dotenv
import google.generativeai as genai
import os
from .system_instructions import get_prompt  # Directly import the dictionary

# Load environment variables
load_dotenv()

class TranslateEngine:
    def __init__(self):
        """Initialize with API key from environment"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=self.api_key)
        
    def translate(self, text: str, dialect: str = 'egyptian') -> str:
        """
        Translate text to specified dialect
        
        Args:
            text: Input text to translate
            dialect: Target dialect (default: Egyptian)
            
        Returns:
            Translated text
        """
        # Get prompt for dialect (fallback to Egyptian if not found)
        prompt = get_prompt(dialect.lower())
        
        # Create model with dialect-specific instructions
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 1024,
            },
            system_instruction=prompt
        )
        
        # Generate translation
        response = model.generate_content(text)
        
        # Return translated text
        print(response.text.strip())
        return response.text.strip()

