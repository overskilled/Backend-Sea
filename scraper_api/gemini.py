import google.generativeai as genai
import os



genai.configure(api_key="AIzaSyBiX-QWrANjeCx6U39FqGBU2GzvwG1ErHw")

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_or_analyze_article(article_text: str, instructions: str = None) -> str:
    """
    Send article text to Gemini with optional instructions (e.g., summarize, analyze tone).
    """
    if not instructions:
        instructions = "Summarize the following article content in plain English."

    prompt = f"{instructions}\n\nArticle Content:\n{article_text}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error from Gemini: {str(e)}"
