import requests
from bs4 import BeautifulSoup
import csv

url_principale = 'http://books.toscrape.com/'


def recup_info_1livre(url):
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
        """"with open("P02_02_PremierLivre.csv", "a", newline='') as données:
            données.write(
                product_page_url + "," + title + "," + str(product_description) + "," + str(image_url) + "," + str(
                    upc) + "," + str(product_type) + "," + str(price_exclu_tax) + "," + str(
                    price_including_tax) + "," + str(number_available) + "," + str(review_rating))
        """



def recup_url_1cathegorie(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    # récuperer toute les url
    if res.ok:
        liens = soup.findAll("h3")
        urls = []
        # récup nb de pages (balise => <li class="current"
        listeLi = []
        li = soup.find("li", {"class": "current"})
        # condition verifiant si il y a plusieurs page
        if li is li != 'none':
            Li = li.text
            # print(Li)
            page = url
            # si c'est vrais, boucle qui tourne le nb de page
            while page:
                # création beautifulsoupe, en remplacement "index" par le nom de la page
                res = requests.get(url)
                soup = BeautifulSoup(res.text, 'lxml')
                # print(soup)
                # récup h3
                h3 = soup.findAll("h3")
                print(h3)
                # boucle pour récup et recomposer les liens (l 53 à 56)
                for n in liens:
                    a = n.find("a")["href"]
                    urls.append(url_principale + a)#.replace("../../../catalogue/", "http://books.toscrape.com/catalogue/" ))
                    print(str(urls))
            break
            # si AttributeError:
                # return
    else:
        print("pas de page")
        return recup_info_1livre(url)


        return urls


recup_url_1cathegorie("http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html")









