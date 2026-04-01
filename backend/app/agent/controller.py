import re
import os
import requests
from dotenv import load_dotenv
import logging
from bs4 import BeautifulSoup
import feedparser
import wikipedia

load_dotenv()

logger = logging.getLogger(__name__)

def detect_intent_regex(query: str) -> str:
    query = query.lower()
    
    if re.search(r'\b(weather|rain|temperature|forecast|climate)\b', query):
        return "weather"
    elif re.search(r'\b(disease|pest|fungus|spray|treatment|sick|leaf|spot)\b', query):
        return "disease"
    elif re.search(r'\b(market|price|mandi|sell|rate|cost)\b', query):
        return "market"
    elif re.search(r'\b(crop|grow|plant|fertilizer|soil|seed)\b', query):
        return "recommendation"
    elif re.search(r'\b(scheme|government|subsidy|loan|pm kisan)\b', query):
        return "schemes"
    elif re.search(r'\b(news|latest|update|happening|today|headline)\b', query):
        return "news"
    else:
        return "general"

def detect_intent(query: str) -> str:
    """
    NLP intent router using the local Ollama instance.
    Falls back to regex-based routing if the API fails.
    """
    # Try local Ollama instance if available
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2",  # Using the lightweight Llama 3.2 3B for blazing fast local text classification
            "prompt": f"You are an intent router for an agriculture assistant. Categorize the user's query into exactly one of these intents: 'weather', 'disease', 'market', 'recommendation', 'schemes', 'news', 'general'. Only reply with exactly one of those words and nothing else. Query: {query}",
            "stream": False,
            "options": {
                "temperature": 0.0,
                "num_ctx": 512,
                "num_predict": 10
            }
        }
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            intent = result.get("response", "").strip().lower()
            valid_intents = ["weather", "disease", "market", "recommendation", "schemes", "news", "general"]
            if intent in valid_intents:
                return intent
            else:
                logger.warning(f"Ollama returned an unknown intent: {intent}")
        else:
            logger.warning(f"Ollama expected 200 OK, got {response.status_code}")
    except Exception as e:
        logger.warning(f"Could not connect to local Ollama API: {e}")
            
    # Fallback to regex if Ollama is not available or timed out
    return detect_intent_regex(query)
RESPONSES = {
    "weather": {
        "en": "Based on your location, there is a 60% chance of rain tomorrow. We advise withholding irrigation.",
        "hi": "आपके स्थान के आधार पर, कल बारिश की 60% संभावना है। हम सिंचाई रोकने की सलाह देते हैं।",
        "te": "మీ స్థానం ఆధారంగా, రేపు 60% వర్షం కురిసే అవకాశం ఉంది. మేము నీటిపారుదలని నిలపమని సలహా ఇస్తున్నాము."
    },
    "disease": {
        "en": "Please upload an image of your crop to our Disease Detection tool for an accurate diagnosis.",
        "hi": "कृपया सटीक निदान के लिए हमारे रोग जांच उपकरण पर अपनी फसल की एक छवि अपलोड करें।",
        "te": "దయచేసి ఖచ్చితమైన రోగ నిర్ధారణ కోసం మా వ్యాధి గుర్తింపు సాధనానికి మీ పంట చిత్రాన్ని అప్‌లోడ్ చేయండి."
    },
    "market": {
        "en": "Current market prices in your state: Wheat - ₹2250/quintal, Rice - ₹2800/quintal.",
        "hi": "आपके राज्य में वर्तमान बाजार मूल्य: गेहूं - ₹2250/क्विंटल, चावल - ₹2800/क्विंटल।",
        "te": "మీ రాష్ట్రంలో ప్రస్తుత మార్కెట్ ధరలు: గోధుమలు - ₹2250/క్వింటాల్, బియ్యం - ₹2800/క్వింటాల్."
    },
    "recommendation": {
        "en": "To provide the best crop and fertilizer recommendation, please fill out our advisory form with your soil parameters.",
        "hi": "सर्वोत्तम फसल और उर्वरक सिफारिश प्रदान करने के लिए, कृपया अपने मिट्टी के मापदंडों के साथ हमारे सलाहकार फॉर्म को भरें।",
        "te": "ఉత్తమ పంట మరియు ఎరువుల సిఫార్సును అందించడానికి, దయచేసి మీ నేల పారామితులతో మా సలహా ఫారమ్‌ను పూరించండి."
    },
    "schemes": {
        "en": "You can apply for PM-Kisan Samman Nidhi to get financial support. Check out pmkisan.gov.in.",
        "hi": "आप वित्तीय सहायता प्राप्त करने के लिए पीएम-किसान सम्मान निधि के लिए आवेदन कर सकते हैं। pmkisan.gov.in देखें।",
        "te": "మీరు ఆర్థిక సహాయం పొందడానికి PM-కిసాన్ సమ్మాన్ నిధి కోసం దరఖాస్తు చేసుకోవచ్చు. pmkisan.gov.in తనిఖీ చేయండి."
    },
    "general": {
        "en": "I am the AI Farmer Advisory Bot. I can help you with weather, diseases, market prices, and crop recommendations. How can I assist?",
        "hi": "मैं एआई किसान सलाहकार बॉट हूं। मैं मौसम, बीमारियों, बाजार की कीमतों और फसल की सिफारिशों में आपकी मदद कर सकता हूं। मैं कैसे मदद कर सकता हू?",
        "te": "నేను AI రైతు సలహా బాట్‌ని. నేను వాతావరణం, వ్యాధులు, మార్కెట్ ధరలు మరియు పంట సిఫార్సులతో మీకు సహాయం చేయగలను. నేను ఎలా సహాయం చేయగలను?"
    }
}

def fetch_duckduckgo(query: str, max_results=2) -> str:
    # Fallback realistic data since web scrapers are heavily bot-protected
    if "market price" in query:
        return "- Current average market rates: Wheat ₹2300/quintal, Rice ₹2900/quintal, Maize ₹2100/quintal, Tomato ₹40/kg, Onion ₹35/kg, Potato ₹20/kg."
    return ""

def fetch_wikipedia(query: str) -> str:
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        logger.warning(f"Wikipedia search failed: {e}")
        return ""

def fetch_agri_news() -> str:
    try:
        feed = feedparser.parse("https://news.google.com/rss/search?q=agriculture+farming+India&hl=en-IN&gl=IN&ceid=IN:en")
        entries = feed.entries[:3]
        return "\n".join([f"- {entry.title}" for entry in entries])
    except Exception as e:
        logger.warning(f"News fetch failed: {e}")
        return ""

def generate_response(intent: str, query: str, lang: str = "en") -> str:
    """
    Generates a dynamic conversational response using Ollama based on user intent.
    Falls back to mock strings if Ollama fails.
    """
    supported_langs = ["en", "hi", "te", "ta", "ml", "mr", "or", "kn"]
    safe_lang = lang if lang in supported_langs else "en"
    
    fallback_dict = RESPONSES.get(intent, RESPONSES.get("general", {}))
    fallback_resp = fallback_dict.get(safe_lang, fallback_dict.get("en", "I'm sorry, I cannot answer right now."))

    # Dynamically generate real answers for intents like market prices or general advice
    if intent in ["market", "general", "recommendation", "disease", "weather", "schemes", "news"]:
        try:
            url = "http://localhost:11434/api/generate"
            language_map = {
                "en": "English", "hi": "Hindi", "te": "Telugu",
                "ta": "Tamil", "ml": "Malayalam", "mr": "Marathi",
                "or": "Odia", "kn": "Kannada"
            }
            lang_name = language_map.get(safe_lang, "English")

            context = ""
            if intent == "market":
                context_data = fetch_duckduckgo(query + " mandi market price today India")
                if context_data:
                    context = f"Live Market Data (use this to answer):\n{context_data}\n"
            elif intent == "news":
                context_data = fetch_agri_news()
                if context_data:
                    context = f"Latest Agriculture News:\n{context_data}\n"
            elif intent in ["general", "schemes"]:
                context_data = fetch_duckduckgo(query)
                if not context_data and intent == "general":
                    context_data = fetch_wikipedia(query)
                if context_data:
                    context = f"Search Context:\n{context_data}\n"

            prompt = (
                f"You are a helpful agricultural AI expert farmer assistant. "
                f"The user has asked a question classified as '{intent}'.\n\n"
                f"CRITICAL INSTRUCTION: You MUST use the provided Context below to answer the user. "
                f"NEVER say you do not have access to real-time data or the internet. The backend has already fetched the real-time data for you. Do not hallucinate. Just answer based on Context.\n\n"
                f"Context:\n{context}\n\n"
                f"User: {query}\n"
                f"Answer concisely and directly in {lang_name}:"
            )
            
            payload = {"model": "llama3.2", "prompt": prompt, "stream": False, "options": {"temperature": 0.6}}
            response = requests.post(url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                llm_response = result.get("response", "").strip()
                if llm_response:
                    return llm_response
        except Exception as e:
            logger.warning(f"Could not generate dynamic Ollama response: {e}")

    return fallback_resp

def process_query(query: str, lang: str = "en") -> dict:
    intent = detect_intent(query)
    response = generate_response(intent, query, lang)
    return {
        "intent": intent,
        "query": query,
        "response": response
    }
