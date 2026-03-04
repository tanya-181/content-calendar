"""
hashtag_engine.py
-----------------
Suggests relevant hashtags based on topic keywords and platform.
Uses keyword-to-category mapping + platform-specific popular tags.
"""

import re

# ── Keyword → Category Mapping ─────────────────────────────────────────────

CATEGORY_MAP = {
    "fitness": ["workout", "gym", "exercise", "health", "fit", "training", "cardio", "yoga", "run", "lifting"],
    "food": ["food", "recipe", "cook", "eat", "meal", "delicious", "bake", "cuisine", "chef", "nutrition"],
    "travel": ["travel", "trip", "vacation", "explore", "adventure", "journey", "destination", "wanderlust", "tour"],
    "tech": ["tech", "code", "software", "developer", "programming", "ai", "data", "app", "startup", "digital"],
    "fashion": ["fashion", "style", "outfit", "clothing", "wear", "trend", "ootd", "dress", "accessories"],
    "beauty": ["beauty", "makeup", "skincare", "glow", "hair", "cosmetics", "selfcare", "routine"],
    "motivation": ["motivat", "inspire", "success", "mindset", "goal", "hustle", "grind", "positiv", "growth"],
    "business": ["business", "entrepreneur", "marketing", "brand", "sales", "startup", "invest", "finance", "money"],
    "education": ["learn", "study", "education", "school", "student", "knowledge", "course", "skill", "tip"],
    "nature": ["nature", "outdoor", "environment", "green", "plant", "garden", "wildlife", "earth", "sustainable"],
    "art": ["art", "design", "creative", "draw", "paint", "illustration", "photo", "visual", "aesthetic"],
    "music": ["music", "song", "artist", "band", "concert", "playlist", "beat", "melody", "rhythm"],
    "sports": ["sport", "football", "basketball", "cricket", "soccer", "tennis", "match", "team", "game", "player"],
    "lifestyle": ["lifestyle", "life", "daily", "morning", "routine", "home", "family", "self", "wellness"],
}

# ── Platform-Specific Hashtag Sets ────────────────────────────────────────

HASHTAGS = {
    "fitness": {
        "instagram": ["#fitness", "#workout", "#gymlife", "#fitnessmotivation", "#healthylifestyle",
                      "#fitfam", "#exercise", "#gains", "#bodybuilding", "#personaltrainer"],
        "twitter":   ["#fitness", "#workout", "#fitnessmotivation", "#healthyliving", "#gymlife"],
        "linkedin":  ["#fitness", "#wellness", "#healthylifestyle", "#worklifebalance", "#selfcare"],
    },
    "food": {
        "instagram": ["#foodie", "#foodphotography", "#instafood", "#homecooking", "#foodlover",
                      "#yummy", "#delicious", "#foodblogger", "#recipe", "#healthyfood"],
        "twitter":   ["#food", "#foodie", "#recipe", "#cooking", "#foodlover"],
        "linkedin":  ["#food", "#foodindustry", "#nutrition", "#healthyeating", "#culinary"],
    },
    "travel": {
        "instagram": ["#travel", "#wanderlust", "#travelgram", "#explore", "#adventure",
                      "#travelphotography", "#instatravel", "#travelblogger", "#vacation", "#worldtravel"],
        "twitter":   ["#travel", "#wanderlust", "#adventure", "#explore", "#vacation"],
        "linkedin":  ["#travel", "#businesstravel", "#remotework", "#digitalnomad", "#globetrotter"],
    },
    "tech": {
        "instagram": ["#tech", "#technology", "#coding", "#developer", "#programming",
                      "#softwareengineering", "#ai", "#datascience", "#innovation", "#startup"],
        "twitter":   ["#tech", "#coding", "#developer", "#AI", "#programming", "#buildinpublic"],
        "linkedin":  ["#technology", "#softwareengineering", "#AI", "#datascience", "#innovation",
                      "#developer", "#programming", "#machinelearning", "#python", "#career"],
    },
    "fashion": {
        "instagram": ["#fashion", "#style", "#ootd", "#fashionblogger", "#outfitoftheday",
                      "#streetstyle", "#fashionista", "#lookbook", "#trend", "#instafashion"],
        "twitter":   ["#fashion", "#style", "#ootd", "#fashionblogger", "#trend"],
        "linkedin":  ["#fashion", "#fashionindustry", "#retail", "#style", "#brand"],
    },
    "beauty": {
        "instagram": ["#beauty", "#makeup", "#skincare", "#beautyblogger", "#makeuptutorial",
                      "#glowup", "#selfcare", "#beautytips", "#skincareroutine", "#naturalmakeup"],
        "twitter":   ["#beauty", "#makeup", "#skincare", "#beautytips", "#selfcare"],
        "linkedin":  ["#beauty", "#beautyindustry", "#wellness", "#skincare", "#cosmetics"],
    },
    "motivation": {
        "instagram": ["#motivation", "#inspiration", "#mindset", "#success", "#goals",
                      "#positivevibes", "#hustle", "#growthmindset", "#entrepreneur", "#quotes"],
        "twitter":   ["#motivation", "#inspiration", "#mindset", "#success", "#hustle"],
        "linkedin":  ["#motivation", "#leadership", "#success", "#growthmindset", "#careerdevelopment"],
    },
    "business": {
        "instagram": ["#business", "#entrepreneur", "#startup", "#marketing", "#success",
                      "#smallbusiness", "#brand", "#hustle", "#businessowner", "#entrepreneurship"],
        "twitter":   ["#business", "#entrepreneur", "#startup", "#marketing", "#fintech"],
        "linkedin":  ["#business", "#entrepreneur", "#leadership", "#marketing", "#startup",
                      "#innovation", "#networking", "#sales", "#branding", "#strategy"],
    },
    "education": {
        "instagram": ["#education", "#learning", "#study", "#knowledge", "#student",
                      "#elearning", "#onlinelearning", "#skills", "#tips", "#growth"],
        "twitter":   ["#education", "#learning", "#edtech", "#study", "#knowledge"],
        "linkedin":  ["#education", "#learning", "#skills", "#elearning", "#careeradvice",
                      "#professionaldevelopment", "#upskilling", "#growth", "#onlinelearning"],
    },
    "nature": {
        "instagram": ["#nature", "#outdoors", "#environment", "#green", "#sustainability",
                      "#naturephotography", "#earthday", "#wildlife", "#ecofriendly", "#gogreen"],
        "twitter":   ["#nature", "#environment", "#sustainability", "#climateaction", "#green"],
        "linkedin":  ["#sustainability", "#environment", "#greenbusiness", "#climatechange", "#esg"],
    },
    "art": {
        "instagram": ["#art", "#design", "#creative", "#illustration", "#digitalart",
                      "#artist", "#artwork", "#drawing", "#painting", "#graphicdesign"],
        "twitter":   ["#art", "#design", "#creative", "#illustration", "#artist"],
        "linkedin":  ["#design", "#creative", "#uxdesign", "#graphicdesign", "#branding"],
    },
    "music": {
        "instagram": ["#music", "#newmusic", "#musician", "#songwriter", "#artist",
                      "#playlist", "#indiemusic", "#hiphop", "#pop", "#producer"],
        "twitter":   ["#music", "#newmusic", "#nowplaying", "#artist", "#musician"],
        "linkedin":  ["#music", "#musicindustry", "#entertainment", "#artist", "#creative"],
    },
    "sports": {
        "instagram": ["#sports", "#athlete", "#football", "#basketball", "#cricket",
                      "#fitness", "#team", "#champion", "#sportslife", "#training"],
        "twitter":   ["#sports", "#athlete", "#game", "#champion", "#football"],
        "linkedin":  ["#sports", "#sportsmanagement", "#athlete", "#teamwork", "#leadership"],
    },
    "lifestyle": {
        "instagram": ["#lifestyle", "#daily", "#morningroutine", "#wellbeing", "#selfcare",
                      "#wellness", "#mindfulness", "#happy", "#life", "#inspo"],
        "twitter":   ["#lifestyle", "#wellness", "#selfcare", "#daily", "#mindfulness"],
        "linkedin":  ["#lifestyle", "#worklifebalance", "#wellness", "#productivity", "#mindfulness"],
    },
}

GENERIC_TAGS = {
    "instagram": ["#instagood", "#photooftheday", "#content", "#contentcreator", "#viral", "#reels"],
    "twitter":   ["#trending", "#viral", "#content", "#socialmedia"],
    "linkedin":  ["#contentmarketing", "#socialmedia", "#linkedin", "#networking"],
}


def tokenize(text: str) -> list[str]:
    """Lowercase and split text into words."""
    return re.findall(r"[a-z]+", text.lower())


def detect_categories(topic: str) -> list[str]:
    """Detect which categories the topic belongs to."""
    tokens = tokenize(topic)
    matched = []
    for category, keywords in CATEGORY_MAP.items():
        for token in tokens:
            if any(token.startswith(kw) or kw.startswith(token) for kw in keywords):
                if category not in matched:
                    matched.append(category)
    return matched


def suggest_hashtags(topic: str, platform: str = "instagram", max_tags: int = 15) -> list[str]:
    """
    Main function: given a topic string and platform, return a list of suggested hashtags.
    """
    platform = platform.lower()
    if platform not in ("instagram", "twitter", "linkedin"):
        platform = "instagram"

    categories = detect_categories(topic)
    result = []

    for cat in categories:
        tags = HASHTAGS.get(cat, {}).get(platform, [])
        for tag in tags:
            if tag not in result:
                result.append(tag)

    # Fill with generic tags if not enough
    for tag in GENERIC_TAGS.get(platform, []):
        if tag not in result:
            result.append(tag)

    return result[:max_tags]
