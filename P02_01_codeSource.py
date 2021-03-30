import requests
from bs4 import BeautifulSoup
import csv

url_principale = 'http://books.toscrape.com'
# mise en page fichié csv:
"""with open("P02_02_PremierLivre.csv", "w") as données:
    données.write(
        "product_page_url, title, product_description, image_ul, upc, product_type, price_exclu_tax,price_inclu_tax, number_available, review_rating " + "\n")
"""

def recup_info_1livre(url):
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        retour_info_un_livre = {}
        # product_page_url = url
        retour_info_un_livre["product page url"]= url
        # title = soup.find('h1').text
        retour_info_un_livre["title"]= soup.find('h1').text
        # product_description = soup.select("#product_description+p")
        retour_info_un_livre["product description"] = soup.select("#product_description+p")
        # image_url = soup.select("img")
        retour_info_un_livre["image url"] = soup.select("img")
        tds = soup.findAll("td")
        # upc = tds[0].text
        retour_info_un_livre["upc"] = tds[0].text
        # product_type = tds[1].text
        retour_info_un_livre["product type"] = tds[1].text
        # price_exclu_tax = tds[2].text
        retour_info_un_livre["price exclu tax"] = tds[2].text
        # price_including_tax = tds[3].text
        retour_info_un_livre["price including tax"] = tds[3].text
        # number_available = tds[5].text
        retour_info_un_livre["number available"] = tds[5].text
        # review_rating = soup.find("p", {"class": "star-rating"})["class"]
        retour_info_un_livre["review rating"] = soup.find("p", {"class": "star-rating"})["class"]
        print(retour_info_un_livre)
        return retour_info_un_livre

def recup_url_1cathegorie(url):
    res = requests.get(url)
    # récuperer toute les url
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        liens = soup.findAll("h3")
        urls = []
        # récup nb de pages (balise => <li class="current"
        li = soup.find("li", {"class": "current"})
        # condition verifiant si il y a plusieurs page
        if li != None:
            nbre_page = li.text.strip()[-1]
            # si c'est vrais, boucle qui tourne le nb de page
            for i in range(1, int(nbre_page)+1) :
                current_url = url.replace("index.html", "page-" + str(i) + ".html")
                #print(current_url)
                # création beautifulsoupe, en remplacement "index" par le nom de la page
                res = requests.get(current_url)
                soup = BeautifulSoup(res.text, 'lxml')
                # print(soup)
                # récup h3
                h3 = soup.findAll("h3")
                # boucle pour récup et recomposer les liens (l 53 à 56)
                for n in h3:
                    a = n.find("a")["href"]
                    urls.append(a.replace("../../../", "http://books.toscrape.com/catalogue/" ))
        else:
            for n in liens:
                a = n.find("a")["href"]
                urls.append(a.replace("../../../", "http://books.toscrape.com/catalogue/"))
                # print(a)

        return urls


def recup_liens_cathegori_menu(url):
    print(url)
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        # liens_nav = []
        # récup le menu
        nav = soup.find("aside").findAll("a")
        print(nav)
        # boucle pour récup les liens dans le nav ET recomposer les liens
            #  a = n.find("a")["href"] ===== récup des liens
            #  urls.append(a.replace("../../../", "http://books.toscrape.com/catalogue/" )) ===== recompose les liens.


recup_liens_cathegori_menu(url_principale)

# boucle:

"""urls = recup_url_1cathegorie("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html") === sup liens pour passer a la fonction
infoComplet_un_livre = []
for url in urls:
    infoComplet_un_livre.append(recup_info_1livre(url))
"""





    # enregistrement des informations du livre:
""""with open("P02_02_PremierLivre.csv", "a", newline='') as données:
        données.write(
            product_page_url + "," + title + "," + str(product_description) + "," + str(image_url) + "," + str(
                upc) + "," + str(product_type) + "," + str(price_exclu_tax) + "," + str(
                price_including_tax) + "," + str(number_available) + "," + str(review_rating))
    """








