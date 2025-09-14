# config/agno_config.py - AGNO with SQL Server
import os
from agno.models.groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_groq_model():
    """Get configured Groq model"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    return Groq(
        id="llama-3.1-70b-versatile",
        api_key=api_key
    )

def test_groq_connection():
    """Test Groq API connection"""
    try:
        model = get_groq_model()
        print("✅ Groq model configured successfully")
        return True
    except Exception as e:
        print(f"❌ Groq configuration failed: {e}")
        return False

# AGNO Configuration
AGNO_CONFIG = {
    "model": get_groq_model,
    "debug_mode": True,
    "show_tool_calls": True,
    "markdown": True
}

if __name__ == "__main__":
    print("🔍 Testing Groq configuration...")
    test_groq_connection()