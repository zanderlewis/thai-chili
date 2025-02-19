import json
import requests
from bs4 import BeautifulSoup
import os

def scrape_kwickmenu_from_url(url='https://thaichiliasianbistronc.kwickmenu.com/'):
    response = requests.get(url)
    response.raise_for_status()  # raise an exception for HTTP errors
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    categories = []
    # find all li elements with a class starting with "cat"
    for li in soup.find_all('li', class_=lambda c: c and c.startswith('cat')):
        cat_data = li.get('data-item')
        if not cat_data:
            continue
        # Parse the HTML snippet inside data-item attribute
        cat_soup = BeautifulSoup(cat_data, 'html.parser')
        items = []
        for item_li in cat_soup.find_all('li', class_='item noimg'):
            item_data = {}
            # Try to get the name from <b class='n'>. If not found, fallback to the first <b> tag.
            name_elem = item_li.find('b', class_='n')
            if not name_elem:
                b_tags = item_li.find_all('b')
                if b_tags:
                    name_elem = b_tags[0]
            if name_elem:
                item_data['name'] = name_elem.get_text(strip=True)
            price_elem = item_li.find('b', class_='p')
            if price_elem:
                item_data['price'] = price_elem.get_text(strip=True)
            desc_elem = item_li.find('p')
            item_data['description'] = desc_elem.get_text(strip=True) if desc_elem else ""
            items.append(item_data)
        # Optionally extract a category name from the outer li text
        category_name = li.get_text(strip=True)
        categories.append({
            'category': category_name,
            'items': items
        })
    return categories

def main():
    # Scrape from the remote URL
    try:
        categories = scrape_kwickmenu_from_url('https://thaichiliasianbistronc.kwickmenu.com/')

        # Write the scraped menu to a new JSON file, prettified
        scraped_menu = {'categories': categories}
        os.makedirs('src/data', exist_ok=True)
        with open('src/data/menu.json', 'w', encoding='utf-8') as f:
            json.dump(scraped_menu, f, indent=4)
    except Exception as e:
        print("Error scraping the URL:", e)

if __name__ == '__main__':
    main()