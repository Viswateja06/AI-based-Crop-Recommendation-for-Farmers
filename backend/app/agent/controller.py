import re

def detect_intent(query: str) -> str:
    """
    Simulates an NLP intent router.
    In a full production application, this might use LangChain + OpenAI,
    or a HuggingFace Zero-Shot classification pipeline.
    """
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
    else:
        return "general"

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

def generate_response(intent: str, query: str, lang: str = "en") -> str:
    """
    Routes the query to the appropriate mock handler based on intent.
    """
    safe_lang = lang if lang in ["en", "hi", "te"] else "en"
    return RESPONSES.get(intent, RESPONSES["general"])[safe_lang]

def process_query(query: str, lang: str = "en") -> dict:
    intent = detect_intent(query)
    response = generate_response(intent, query, lang)
    return {
        "intent": intent,
        "query": query,
        "response": response
    }
