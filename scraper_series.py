import requests
import json
import urllib.parse

def extract_series_details():
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
        
        clean_series = []
        
        for item in raw_data:
            # Series သက်သက်ကိုပဲ စစ်ထုတ်မယ်
            if item.get("type") == "series":
                
                # --- Image Proxy ထည့်သွင်းခြင်း ---
                original_poster = item.get("posterUrl", "")
                proxy_poster = f"https://images.weserv.nl/?url={urllib.parse.quote(original_poster)}" if original_poster else ""
                
                # --- Seasons နဲ့ Episodes တွေထဲက Video URL တွေကို ဆွဲယူခြင်း ---
                seasons_data = []
                for season in item.get("seasons", []):
                    season_info = {
                        "season_title": season.get("title", f"Season {season.get('seasonNumber')}"),
                        "episodes": []
                    }
                    
                    for episode in season.get("episodes", []):
                        ep_info = {
                            "episode_number": episode.get("episodeNumber"),
                            "episode_title": episode.get("title", "Unknown Episode"),
                            "video_urls": []
                        }
                        
                        # Primary Server ကို ရှာဖွေမယ်
                        primary_server = next((srv for srv in episode.get("servers", []) if "Primary" in srv.get("name", "")), None)
                        
                        # Primary Server မရှိရင် ပထမဆုံး Server ကို ယူမယ်
                        if not primary_server and episode.get("servers"):
                            primary_server = episode.get("servers")[0]
                            
                        if primary_server:
                            for quality_data in primary_server.get("qualities", []):
                                ep_info["video_urls"].append({
                                    "quality": quality_data.get("quality"),
                                    "videoUrl": quality_data.get("videoUrl")
                                })
                                
                        season_info["episodes"].append(ep_info)
                    
                    seasons_data.append(season_info)
                
                # လိုချင်တဲ့ Field တွေကို စုစည်းမယ်
                clean_series.append({
                    "title": item.get("title", "Unknown"),
                    "type": item.get("type", "series"),
                    "category": item.get("category", "Unknown"),
                    "year": item.get("year", "Unknown"),
                    "posterUrl": proxy_poster,
                    "seasons": seasons_data
                })
        
        print(f"[+] Total Series extracted: {len(clean_series)}")
        
        # ရလာတဲ့ Data ကို File အသစ်ထဲ သိမ်းမည်
        output_file = "clean_series.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(clean_series, f, indent=2, ensure_ascii=False)
        print(f"[+] Successfully saved to '{output_file}'")
        
        # Console မှာ နမူနာ (၂) ကားစာ ပြသပေးမယ်
        print("\n" + "="*60)
        print("SAMPLE OUTPUT (First 2 Series):")
        print("="*60)
        for i, series in enumerate(clean_series[:2], start=1):
            print(f"\n--- Series {i}: {series['title']} ({series['year']}) ---")
            print(f"Category: {series['category']}")
            print(f"Poster: {series['posterUrl']}")
            for season in series['seasons'][:1]: # ပထမဆုံး Season ကိုပဲ နမူနာပြမယ်
                print(f"  -> {season['season_title']}")
                for ep in season['episodes'][:2]: # ပထမဆုံး Episode ၂ ခုကိုပဲ နမူနာပြမယ်
                    print(f"     Ep {ep['episode_number']}: {ep['episode_title']}")
                    for v in ep['video_urls']:
                        print(f"        [{v['quality']}] {v['videoUrl']}")
        print("="*60)

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    extract_series_details()
