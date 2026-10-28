import os
import feedparser
from google import genai
from dotenv import load_dotenv

# 1. Load API Key securely
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

#client
client = genai.Client(api_key=api_key)

# 2. ESPN NFL RSS Feed URL
rss_url = "https://www.espn.com/espn/rss/nfl/news"

def fetch_latest_news():
    print("[+] Fetching latest NFL news from ESPN...")
    feed = feedparser.parse(rss_url)
    
    if feed.entries:
        latest_entry = feed.entries[0]
        news_data = f"Headline: {latest_entry.title}\nDetails: {latest_entry.description}"
        return news_data
    return None

def generate_post(news_content):
    print("[+] Generating AI Prompts and Facebook Caption...\n")
    
    system_prompt = f"""
    You are an expert US Sports Social Media Manager and AI Prompt Engineer.
    Task: I will give you the latest US sports news. Generate two things:
    
    1. [AI Image Prompt]: A detailed text-to-image prompt for Midjourney/Canva. 
    Do NOT include real player faces. Use styles like "cinematic stadium lighting", "dramatic shadows", "neon sports graphics", or "comic book style vector art".
    
    2. [Facebook Caption]: An engaging, short Facebook caption (under 3 sentences). 
    Ask a controversial or debate-style question. Include 5 trending US sports hashtags.
    
    News Input:
    {news_content}
    """
    
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=system_prompt,
    )
    return response.text

if __name__ == "__main__":
    news = fetch_latest_news()
    
    if news:
        print("-" * 50)
        print(f"LATEST NEWS FOUND:\n{news}")
        print("-" * 50)
        
        result = generate_post(news)
        
        print("\n=== YOUR FACEBOOK POST READY ===")
        print(result)
        print("==================================")
    else:
        print("[-] No news found.")