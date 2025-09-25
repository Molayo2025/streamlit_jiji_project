import time
import requests
import pandas as pd

def extract_attr(attrs, key):
    if isinstance(attrs, list):
        for a in attrs:
            if a.get("name", "").lower() == key.lower():
                return a.get("value", "")
    return ""

def extract_brand(title):
    if not title:
        return ""
    brands = ["HP", "Lenovo", "Dell", "Samsung", "Toshiba", "Apple", "Asus", "Acer", "Sony"]
    title_l = title.lower()
    for b in brands:
        if b.lower() in title_l:
            return b
    return ""

collected = []
page = 1
rows_needed = 200
max_pages = 50   # safety cap
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; DataCollector/1.0; +youremail@example.com)"
})
timeout = 10

while len(collected) < rows_needed and page <= max_pages:
    url = f"https://jiji.ng/api_web/v1/listing?slug=electronics&page={page}"
    try:
        resp = session.get(url, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"Request failed on page {page}: {e}")
        break

    adverts = data.get("adverts_list", {}).get("adverts", [])
    if not adverts:
        break

    for ad in adverts:
        collected.append({
            "Title": ad.get("title", "") or "",
            "Price": ad.get("price_obj", {}).get("value"),
            "Category": ad.get("category_name", "") or "",
            "Subcategory": ad.get("category_slug", "") or "",
            "Location": ad.get("region_parent_name", "") or "",
            "City": ad.get("region_name", "") or "",
            "Condition": extract_attr(ad.get("attrs", []), "Condition"),
            "Brand": extract_brand(ad.get("title", "") or "")
        })
        if len(collected) >= rows_needed:
            break

    page += 1
    time.sleep(0.8)   # be polite: ~1 request/sec

# safe DataFrame creation with dynamic index
rows = collected[:rows_needed]
df = pd.DataFrame(rows)
df.index = range(1, len(df) + 1)

# normalize data types
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

print(df.head())
print("Collected rows:", df.shape[0])

df.to_csv("jiji_electronics_2.csv", index=True)
