import requests
from bs4 import BeautifulSoup
import csv

url_principale = 'http://books.toscrape.com/'
# mise en page fichié csv:
"""with open("P02_02_PremierLivre.csv", "w") as données:
    données.write(
        "product_page_url, title, product_description, image_ul, upc, product_type, price_exclu_tax,price_inclu_tax, number_available, review_rating " + "\n")
"""

def recup_info_1livre(url):
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        infoComplet_un_livre = []
        retour_info_un_livre = {}
        infoComplet_un_livre.append(retour_info_un_livre)
        print(infoComplet_un_livre)
        product_page_url = url
        retour_info_un_livre["product page url"]= product_page_url
        title = soup.find('h1').text
        retour_info_un_livre["title"]= title
        product_description = soup.select("#product_description+p")
        retour_info_un_livre["product description"] = product_description
        image_url = soup.select("img")
        retour_info_un_livre["image url"] = image_url
        tds = soup.findAll("td")
        upc = tds[0].text
        retour_info_un_livre["upc"] = upc
        product_type = tds[1].text
        retour_info_un_livre["product type"] = product_type
        price_exclu_tax = tds[2].text
        retour_info_un_livre["price exclu tax"] = price_exclu_tax
        price_including_tax = tds[3].text
        retour_info_un_livre["price including tax"] = price_including_tax
        number_available = tds[5].text
        retour_info_un_livre["number available"] = number_available
        review_rating = soup.find("p", {"class": "star-rating"})["class"]
        retour_info_un_livre["review rating"] = review_rating
        # print(len(retour_info_un_livre))




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
                print(current_url)
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
            prin = "une seule page."
            print(prin)
            for n in liens:
                a = n.find("a")["href"]
                urls.append(a.replace("../../../", "http://books.toscrape.com/catalogue/"))
                print(urls)

        return urls





urls = recup_url_1cathegorie("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")
for url in urls:
    recup_info_1livre(url)


    # enregistrement des informations du livre:
    """"with open("P02_02_PremierLivre.csv", "a", newline='') as données:
        données.write(
            product_page_url + "," + title + "," + str(product_description) + "," + str(image_url) + "," + str(
                upc) + "," + str(product_type) + "," + str(price_exclu_tax) + "," + str(
                price_including_tax) + "," + str(number_available) + "," + str(review_rating))
    """



"""faire une dico pour le  retour de la récup d'un livre
stocker en liste toutes les info de tout les livres d'une cathégorie
faire une fonction qui récu la liste de toute les urls des cathégorie du menu
"""




