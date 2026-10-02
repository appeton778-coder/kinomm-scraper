import requests
import json
import urllib.parse

def extract_movie_details():
    url = "https://kinomm.cc/movies.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }

    print("[*] Fetching data from kinomm.cc...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        raw_data = response.json()
        
        clean_movies = []
        
        for item in raw_data:
            if item.get("type") == "movie":
                primary_server = next((srv for srv in item.get("servers", []) if "Primary" in srv.get("name", "")), None)
                
                video_urls = []
                if primary_server:
                    for quality_data in primary_server.get("qualities", []):
                        video_urls.append({
                            "quality": quality_data.get("quality"),
                            "videoUrl": quality_data.get("videoUrl")
                        })
                
                # --- Image Proxy ထည့်သွင်းခြင်း ---
                original_poster = item.get("posterUrl", "")
                # URL ကို Proxy ဖြတ်သန်းပြီး ရယူမည် (Myanmar ISP Block ကို ကျော်ဖြတ်နိုင်ရန်)
                proxy_poster = f"https://images.weserv.nl/?url={urllib.parse.quote(original_poster)}" if original_poster else ""
                
                clean_movies.append({
                    "title": item.get("title", "Unknown"),
                    "type": item.get("type", "movie"),
                    "category": item.get("category", "Unknown"),
                    "posterUrl": proxy_poster,  # Proxy URL ကို အသုံးပြုမည်
                    "videoUrls": video_urls
                })
        
        print(f"[+] Total Movies extracted: {len(clean_movies)}")
        
        output_file = "clean_movies.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(clean_movies, f, indent=2, ensure_ascii=False)
        print(f"[+] Successfully saved to '{output_file}'")
        
        print("\n--- Sample Extracted Data (First 2 Movies) ---")
        for i, movie in enumerate(clean_movies[:2], start=1):
            print(f"\n{i}. {movie['title']} ({movie['category']})")
            print(f"   Proxy Poster Link: {movie['posterUrl']}")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    extract_movie_details()
