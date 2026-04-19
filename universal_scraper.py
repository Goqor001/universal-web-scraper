import requests
from bs4 import BeautifulSoup
import pandas as pd

# Настройки сайта.
config = {
    "container": {
        "tag": "div",
        "class": "quote"
    },
    "fields":{
        "text":{
            "tag": "span",
            "class": "text",
            "type": "text"
        },
        "author":{
            "tag": "small",
            "class": "author",
            "type": "text"
        },
        "tags":{
            "tag": "a",
            "class": "tag",
            "type": "list"
        },
        "link":{
            "tag": "a",
            "type": "attribute",
            "attr": "href"
        }
    }
}

# Получает html.
def get_html(url):
    try:
        headers = {
            "User-Agent":"Mozilla/5.0"
        }
        response = requests.get(url,headers=headers,timeout=5)

        if response.status_code != 200:
            print(f"Status code error: {response.status_code}")
            return None
        
        return response.text
    except:
        print("Error Loading page.")
        return None

# Парсит один html по config.
def parse_items(html, config, base_url):
    if html is None:
        print("No HTML, stop")
        return []
    
    soup = BeautifulSoup(html,"html.parser")
    containers = soup.find_all(config["container"]["tag"],class_=config["container"]["class"])
    all_data = []

    for container in containers:
        row = {}
        for field_name, field_config in config["fields"].items():
            if field_config["type"] == "text":
                if "class" in field_config:
                    element = container.find(field_config["tag"],class_=field_config["class"])
                else:
                    element = container.find(field_config["tag"])

                if element is None:
                    row[field_name] = ""
                else:
                    row[field_name] = element.text.strip()

            elif field_config["type"] == "list":
                if "class" in field_config:
                    elements = container.find_all(field_config["tag"],class_=field_config["class"])
                else:
                    elements = container.find_all(field_config["tag"])

                if not elements:
                    row[field_name] = []
                else:
                    finally_elements = [el.text.strip() for el in elements]
                    row[field_name] = finally_elements

            elif field_config["type"] == "attribute":
                if "class" in field_config:
                    element = container.find(field_config["tag"],class_=field_config["class"])
                else:
                    element = container.find(field_config["tag"])

                if element is None:
                    row[field_name] = None
                else:
                    attribute = url + element.get(field_config["attr"],"")
                    row[field_name] = attribute

        all_data.append(row)
    return all_data

# Проверяет есть ли следуюшая страница.
def has_next_page(html):
    soup = BeautifulSoup(html,"html.parser")
    next_btn = soup.find("li",class_="next")
    return next_btn is not None

# Сохраняет результат.
def save_csv(data,filename="quotes.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename,index=False,encoding="utf-8")

all_data = []
page = 1
base_url = "http://quotes.toscrape.com"

while True:
    print(f"Parsing page {page}")

    url = f"{base_url}/page/{page}/"
    
    html = get_html(url)

    if html is None:
        print("Failed to load page")
        break
    
    data = parse_items(html,config,base_url)

    if not data:
        break

    all_data.extend(data)
    print(f"Page {page}: {len(data)} items")

    if not has_next_page(html):
        print("No more page")
        break
    
    page += 1

if not all_data:
    print("No data collected")
else:
    save_csv(all_data)
    print(f"Saved {len(all_data)} items")
