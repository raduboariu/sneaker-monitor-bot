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
    try:
        response = requests.post(DISCORD_WEBHOOK, json=data, timeout=10)
        response.raise_for_status()
        print(f"Sent to Discord: {title}")
    except Exception as e:
        print(f"Failed to send to Discord: {e}")

def check_nike_snkrs():
    url = "https://api.nike.com/product_feed/threads/v2/?anchor=0&count=20&filter=marketplace(EU)&filter=language(en-GB)&filter=upcoming(true)"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"Failed to fetch from Nike SNKRS. Status code: {resp.status_code}")
            return

        data = resp.json()

        for product in data.get("objects", []):
            pid = product.get("id")
            title = product.get("productInfo", [{}])[0].get("productContent", {}).get("fullTitle", "No Title")
            link = f"https://www.nike.com/launch/t/{product.get('slug')}"
            img = product.get("productInfo", [{}])[0].get("productContent", {}).get("imageUrl", "")
            date = product.get("productInfo", [{}])[0].get("launchView", {}).get("startEntryDate", "TBD")

            if pid and pid not in sent_items:
                if any(keyword in title.lower() for keyword in ["travis", "off-white", "jordan", "collab", "union", "spider-man", "nocta", "ambush", "fragment", "sacai", "supreme", "acg"]):
                    send_to_discord(title, link, img, date, "Nike SNKRS")
                    sent_items.add(pid)

    except Exception as e:
        print(f"Error checking Nike SNKRS: {e}")

def check_travis_store():
    url = "https://shop.travisscott.com/"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            print(f"Failed to fetch Travis Scott store. Status code: {resp.status_code}")
            return

        content = resp.text
        if any(keyword in content for keyword in ["Air Jordan", "Travis", "Nike"]):
            key = f"travis-{int(time.time())}"
            if key not in sent_items:
                send_to_discord(
                    "Possible Drop on Travis Scott's Store!",
                    url,
                    "https://seeklogo.com/images/T/travis-scott-logo-535E1357A2-seeklogo.com.png",
                    "",
                    "TravisScott.com"
                )
                sent_items.add(key)

    except Exception as e:
        print(f"Error checking Travis Scott store: {e}")

def main():
    print("Sneaker monitor bot started!")
    while True:
        print("Checking for drops...")
        check_nike_snkrs()
        check_travis_store()
        time.sleep(60)  # Wait 60 seconds

if __name__ == "__main__":
    main()
