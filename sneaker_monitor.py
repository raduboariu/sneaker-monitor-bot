
import requests
import time
import json

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1364897914555600906/8k-flwPSlnAdqWDThe87k1tiwK7sW8iew3OlOFp7bR-iYVpgZNhRIUqVcGdBczJUdASI"

sent_items = set()

def send_to_discord(title, link, image, date, source):
    data = {
        "embeds": [{
            "title": title,
            "url": link,
            "description": f"**Release Date**: {date or 'Unknown'}\n**Source**: {source}",
            "thumbnail": {"url": image},
            "color": 65280
        }]
    }
    requests.post(DISCORD_WEBHOOK, json=data)

def check_nike_snkrs():
    url = "https://api.nike.com/product_feed/threads/v2/?anchor=0&count=20&filter=marketplace(EU)&filter=language(en-GB)&filter=upcoming(true)"
    resp = requests.get(url).json()

    for product in resp.get("objects", []):
        pid = product.get("id")
        title = product.get("productInfo", [{}])[0].get("productContent", {}).get("fullTitle", "No Title")
        link = f"https://www.nike.com/launch/t/{product.get('slug')}"
        img = product.get("productInfo", [{}])[0].get("productContent", {}).get("imageUrl", "")
        date = product.get("productInfo", [{}])[0].get("launchView", {}).get("startEntryDate", "TBD")

        if pid not in sent_items:
            if any(keyword in title.lower() for keyword in ["travis", "off-white", "jordan", "collab", "union", "spider-man", "nocta", "ambush", "fragment", "sacai", "supreme", "acg"]):
                send_to_discord(title, link, img, date, "Nike SNKRS")
                sent_items.add(pid)

def check_travis_store():
    url = "https://shop.travisscott.com/"
    resp = requests.get(url).text
    if "Air Jordan" in resp or "Travis" in resp or "Nike" in resp:
        key = f"travis-{int(time.time())}"
        if key not in sent_items:
            send_to_discord("Possible Drop on Travis Scott's Store!", url, "https://seeklogo.com/images/T/travis-scott-logo-535E1357A2-seeklogo.com.png", "", "TravisScott.com")
            sent_items.add(key)

def main():
    while True:
        print("Checking for drops...")
        try:
            check_nike_snkrs()
            check_travis_store()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)  # every 60 seconds

if __name__ == "__main__":
    main()
