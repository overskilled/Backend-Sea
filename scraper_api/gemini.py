import google.generativeai as genai
import os



genai.configure(api_key="AIzaSyBiX-QWrANjeCx6U39FqGBU2GzvwG1ErHw")

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

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
    
def fetch_person_info_from_gemini(name: str) -> str:
    """
    Fetch a short biography and achievements of a person using Gemini.
    """
    prompt = f"""
    You are a professional research analyst for a due diligence firm. Your job is to conduct a complete and unbiased investigation into the public profile of the individual named **{name}**.

    Your task is to conduct a web-based investigation using all publicly available information, be it from google, facebook, linkedIn and any possible path and create a detailed report with the following structure:

    ---

    1. **Full Name & Known Aliases**  
    - Legal full name  
    - Any known nicknames, pseudonyms, or aliases

    2. **Basic Information**  
    - Date of birth, place of birth  
    - Nationality  
    - Languages spoken

    3. **Current Occupation & Roles**  
    - Job title(s), company or organization  
    - Industry of operation  
    - Any past roles of note

    4. **Education & Qualifications**  
    - Schools, universities attended  
    - Degrees or certifications obtained  
    - Known academic performance or affiliations

    5. **Professional Background**  
    - Work history  
    - Career milestones and achievements  
    - Key projects or deals

    6. **Media & Public Appearances**  
    - Notable mentions in the press  
    - Public interviews, articles, or TED talks  
    - Social media presence and influence

    7. **Legal & Regulatory Issues**  
    - Any past or pending litigations, arrests, or controversies  
    - Regulatory sanctions or investigations (if any)

    8. **Financial Information**  
    - Known net worth (if available)  
    - Investments, business interests  
    - Ownership of companies, brands, or real estate

    9. **Reputation & Public Sentiment**  
    - Public opinion from news and social media  
    - Endorsements or criticisms by credible figures  
    - Affiliations with political, religious, or social movements

    10. **Affiliations & Networks**  
    - Known partnerships, board memberships  
    - Relationships with prominent individuals or institutions

    11. **Charitable or Philanthropic Activities**  
    - Known donations, NGO work, or charitable efforts

    12. **Risks & Red Flags**  
    - Summarize all findings that may present reputational, legal, or financial risks

    13. **Sources & Citations**  
    - Summarize the types of sources this information was derived from (e.g., news articles, Wikipedia, LinkedIn, etc.)

    ---

    **Constraints & Instructions:**

    - Be neutral and fact-based.  
    - Summarize in clear, professional tone.  
    - Avoid speculative claims unless widely reported.  
    - If data is missing, mention it as “Not publicly available.”  
    - Prioritize credibility: official sources > verified media > crowd-sourced content.

    Now, provide a complete due diligence report on: **{name}**
    """

    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error from Gemini: {str(e)}"
