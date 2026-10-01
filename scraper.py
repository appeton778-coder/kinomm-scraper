import requests
import json

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
            # Movie သက်သက်ကိုပဲ စစ်ထုတ်မယ် (?tab=movies နဲ့ အတူတူပါ)
            if item.get("type") == "movie":
                
                # Primary Server (Fast) ကို ရှာဖွေမယ်
                primary_server = next((srv for srv in item.get("servers", []) if "Primary" in srv.get("name", "")), None)
                
                video_urls = []
                if primary_server:
                    # Primary Server ထဲက Quality အလိုက် Video URL တွေကို ယူမယ် (ဥပမာ - 1080p, 480p)
                    for quality_data in primary_server.get("qualities", []):
                        video_urls.append({
                            "quality": quality_data.get("quality"),
                            "videoUrl": quality_data.get("videoUrl")
                        })
                
                # လိုချင်တဲ့ Field တွေကိုပဲ သီးသန့် စုစည်းမယ်
                clean_movies.append({
                    "title": item.get("title", "Unknown"),
                    "type": item.get("type", "movie"),
                    "category": item.get("category", "Unknown"),
                    "posterUrl": item.get("posterUrl", ""),
                    "videoUrls": video_urls
                })
        
        print(f"[+] Total Movies extracted: {len(clean_movies)}")
        
        # ရလာတဲ့ Clean Data ကို File အသစ်ထဲ သိမ်းမည်
        output_file = "clean_movies.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(clean_movies, f, indent=2, ensure_ascii=False)
        print(f"[+] Successfully saved to '{output_file}'")
        
        # Console မှာ နမူနာ (၃) ကားစာ ပြသပေးမယ်
        print("\n--- Sample Extracted Data (First 3 Movies) ---")
        for i, movie in enumerate(clean_movies[:3], start=1):
            print(f"\n{i}. {movie['title']} ({movie['category']})")
            print(f"   Poster: {movie['posterUrl']}")
            for v in movie['videoUrls']:
                print(f"   Video ({v['quality']}): {v['videoUrl']}")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    extract_movie_details()