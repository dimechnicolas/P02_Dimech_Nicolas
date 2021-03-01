import requests
from bs4 import BeautifulSoup
import csv


def recup_info_1livre():
    url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    # mise en page fichié csv:
    with open("P02_02_PremierLivre.csv", "w") as données:
        données.write(
            "product_page_url, title, product_description, image_ul, upc, product_type, price_exclu_tax,price_inclu_tax, number_available, review_rating " + "\n")
    # récupération des informations d'un livre
    if res.ok:
        product_page_url = url
        title = soup.find('h1').text
        product_description = soup.select("#product_description+p")
        image_url = soup.select("img")
        tds = soup.findAll("td")
        upc = tds[0].text
        product_type = tds[1].text
        price_exclu_tax = tds[2].text
        price_including_tax = tds[3].text
        number_available = tds[5].text
        review_rating = soup.find("p", {"class": "star-rating"})["class"]
        # enregistrement des informations du livre:
        with open("P02_02_PremierLivre.csv", "a", newline='') as données:
            données.write(
                product_page_url + "," + title + "," + str(product_description) + "," + str(image_url) + "," + str(
                    upc) + "," + str(product_type) + "," + str(price_exclu_tax) + "," + str(
                    price_including_tax) + "," + str(number_available) + "," + str(review_rating))



def recup_url_1cathégorie():
    url = 'http://books.toscrape.com/catalogue/category/books/poetry_23/index.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    # récuperer toute les url
    if res.ok:
        liens = soup.findAll("h3")
        for n in liens:
            a = n.find("a")