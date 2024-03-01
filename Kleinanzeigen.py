import requests
import re
import constants
from bs4 import BeautifulSoup

URL_BASE = "https://www.kleinanzeigen.de/"
WEBSITE = "Kleinanzeigen"
PAGES = ["", "/seite:2", "/seite:3", "/seite:4"]
TYPE_PRICE_LIST = [
    ["kaufen", "600000", "c196l3331", "Buy"],
    ["mieten", "1800", "c203l3331", "Rent"]
]

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
}

def kleinanzeigen():
    immo_list = []
    immo_list_clean = []
    for i in TYPE_PRICE_LIST:
        for j in PAGES:

            response = requests.get(URL_BASE+f"s-wohnung-{i[0]}/berlin/preis::{i[1]}/{j}{i[2]}+wohnung_{i[0]}.zimmer_d:2%2C", headers=header)
            response_text = response.text

            soup = BeautifulSoup(response_text, "html.parser")

            posts = soup.find_all(class_="aditem-main")

            for post in posts:

                district = post.find(class_='aditem-main--top--left').getText()
                district_clean = re.sub(r'[0-9]', '', district).lstrip().rstrip()

                description = post.find(class_='ellipsis').getText()

                price = re.sub(r'[VB€.,]', '', post.find(class_='aditem-main--middle--price-shipping--price').getText()).rstrip().lstrip()

                rooms = ' '.join([_.getText() for _ in post.find_all(class_='simpletag')])

                link = URL_BASE + post.find(name='a')['href']

                sub_response = requests.get(link, headers=header)
                sub_response_text = sub_response.text
                sub_soup = BeautifulSoup(sub_response_text, "html.parser")
                last_updated = sub_soup.select(selector="#viewad-extra-info span")[0].getText()

                if district_clean.lower() in constants.DISTRICT_LIST and int(price) > 100 and not any(substring in description.lower() for substring in constants.EXCLUDE_LIST) and description not in immo_list:

                    immo_list.append([
                        i[3],
                        last_updated,
                        description,
                        district_clean,
                        int(price),
                        rooms,
                        WEBSITE,
                        link
                    ])

    [immo_list_clean.append(x) for x in immo_list if x not in immo_list_clean]

    return immo_list_clean