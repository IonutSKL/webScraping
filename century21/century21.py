import sys

import requests
from bs4 import BeautifulSoup
import pandas

r = requests.get("https://www.emag.ro/laptopuri/c?ref=hp_menu_quick-nav_1_1&type=category")
c = r.content
soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("div",{"class":"card-item js-product-data"})
page_nr = soup.find_all("a", {"class": "js-change-page hidden-xs hidden-sm"})[-1].text
page_nr = int(page_nr)+1

#print(list)
'''
y = slice(0,-2)
price_sup = all[0].find("p", {"class": "product-new-price"}).find("sup").text
price = all[0].find( "p", {"product-new-price"} ).text.strip(" Lei")
price_sup2 = "," + price_sup
price_without_sup = price[y]
final_price = price_without_sup + price_sup2 + " Lei"

print("price without sup", price_without_sup)
print("final price", final_price)
'''

list = []
base_url = ("https://www.emag.ro/laptopuri/p")
for page in range(1, int(page_nr), 1):
    print(base_url+str(page)+"/c")
    r = requests.get(base_url+str(page)+"/c")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class": "card-item js-product-data"})
    for item in all:
        d = {}
        d["Product"] = item.find( "a", {"class": "product-title js-product-url"} ).text.replace( "\n", " " ).strip()
        #add price
        y = slice(0, -2)
        price_sup = item.find( "p", {"class": "product-new-price"} ).find( "sup" ).text
        price = item.find( "p", {"product-new-price"} ).text.strip( " Lei" )
        price_sup2 = "," + price_sup
        price_without_sup = price[y]
        d["Price"] = price_without_sup + price_sup2 + " Lei"
        try:
            d["Status"] = item.find( "p", {"class": "product-stock-status"} ).text
        except:
            print( "Not available" )
        list.append( d )


df = pandas.DataFrame(list)
df.to_csv("emag_laptops_final.csv")