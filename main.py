from bs4 import BeautifulSoup
import requests
import json


# Get the URL
product_url = "https://www.walmart.com/ip/Exclusivo-Mezcla-Plush-Fuzzy-Large-Fleece-Throw-Blanket-50-x-70-Dusty-Pink-Soft-Warm-Lightweight/501459727?athAsset=eyJhdGhjcGlkIjoiNTAxNDU5NzI3IiwiYXRoc3RpZCI6IkNTMDIwIiwiYXRoYW5jaWQiOiJJdGVtQ2Fyb3VzZWwiLCJhdGhyayI6MC4wfQ==&athena=true"

# Import the headers by inspecting the website
HEADERS = {
    "Accept": "*/*",
    "Accept-encoding": "gzip, deflate, br, zstd",
    "Accept-language": "en-GB,en-US;q=0.9,en;q=0.8,fa;q=0.7,ar;q=0.6",
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}


def get_product_links(query, page_number=1):
    search_url = f"https://www.walmart.com/search?q={query}&page={page_number}"

    response = requests.get(search_url, headers=HEADERS)
    print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    product_links = []

    for link in links:
        link_href = link["href"]
        if "/ip" in link_href:
            full_url = link_href
        else:
            full_url = "https://walmart.com" + link_href

        product_links.append(full_url)

    return product_links


def extract_product_info(product_url):

    # Send a request to the server inclulding headers to look human

    response = requests.get(product_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # Search for what you want using .find method
    script_tag = soup.find("script", id="__NEXT_DATA__")

    # It converts the JSON string into a Python dictionary using json.loads(). + extract Initial Data using props
    data = json.loads(script_tag.string)
    initial_data = data["props"]["pageProps"]["initialData"]["data"]
    product_data = initial_data["product"]
    reviews_data = initial_data.get("reviews", {})

    # Store data into a dictionary for use

    product_info = {
        "price": product_data["priceInfo"]["currentPrice"]["price"],
        "review_count": reviews_data.get("totalReviewCount", 0),
        "item_id": product_data["usItemId"],
        "avg_rating": reviews_data.get("averageOcerallRating", 0),
        "product_name": product_data["name"],
        "brand": product_data.get("brand", ""),
        "availability": product_data["imageInfo"]["thumbnailUrl"],
        "short_description": product_data.get("shortDescription", ""),
    }
    return product_info


def main():
    OUTPUT_FILE = "product_info.jsonl"

    with open(OUTPUT_FILE, "a") as file:
        page_number = 1
        while True:
            links = get_product_links("blankets", page_number)
            if not links or page_number > 99:
                break

            for link in links:
                try:
                    product_info = extract_product_info(link)
                    if product_info:
                        file.write(json.dumps(product_info) + "\n")
                except Exception as e:
                    print(f"Failed to process URL {link}. Error{e}")

            page_number += 1
            print(f"Search page {page_number}")


if __name__ == "__main__":
    main()


# First try


# with open('home.html', 'r') as html_file:
#     content = html_file.read()


#     soup = BeautifulSoup(content, 'lxml')
#     course_cards = soup.find_all('div', class_='card')
#     for course in course_cards:
#         course_name = course.h5.text
#         course_price = course.a.text.split()[-1]

#         print(f'{course_name} costs {course_price}')


# html_text = requests.get('http://books.toscrape.com/')

# soup = BeautifulSoup(html_text.text, ('html.parser'))

# books = soup.find('li', class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
# bookButton = books.find('button', class_='btn btn-primary btn-block').text
# prices = books.find('p', class_='price_color').text

# print(bookButton)
# print(prices)
