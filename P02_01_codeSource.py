import re
import requests
from bs4 import BeautifulSoup
import os

url_principale = 'http://books.toscrape.com/'
os.mkdir("donnees_scrapees")
os.mkdir("images")

def recup_livre(url): # récupération des données pour 1 livre
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        info_livre = {}
        info_livre["product_page_url"] = url
        info_livre["title"] = soup.find("h1").text
        info_livre["product_description"] = soup.select("#product_description+p")
        info_livre["image_url"] = 'http://books.toscrape.com/' + soup.find('img')['src']
        tds = soup.findAll("td")
        info_livre["upc"] = tds[0].text
        info_livre["product_type"] = tds[1].text
        info_livre["price_exclu_tax"] = tds[2].text
        info_livre["price_including_tax"] = tds[3].text
        info_livre["number_available"] = tds[5].text
        info_livre["review_rating"] = soup.find("p", {"class": "star-rating"})["class"]
        res_img = requests.get(info_livre["image_url"])
        print(info_livre["image_url"])
        if res_img.ok:
            title = re.sub("\W+", "_", info_livre["title"].strip().replace(" ", "_"))
            with open("images/" + title + ".jpg" , "wb") as image:
                image.write(res_img.content)
        return info_livre # retour dans fichier csv



def recup_url_cathegorie(url):
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
                # création beautifulsoupe, en remplacement "index" par le nom de la page
                res = requests.get(current_url)
                soup = BeautifulSoup(res.text, 'lxml')
                # print(soup)
                # récup h3
                h3 = soup.findAll("h3")
                # boucle pour récup et recomposer les liens
                for n in h3:
                    a = n.find("a")["href"]
                    urls.append(a.replace("../../../", "http://books.toscrape.com/catalogue/" ))
        else:
            for n in liens:
                a = n.find("a")["href"]
                urls.append(a.replace("../../../", "http://books.toscrape.com/catalogue/"))

        return urls


def recup_liens_cathegori_menu(url):
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        liens_nav = {}
        # récup le menu
        nav = soup.find("aside").findAll("a")
        # boucle pour récup les liens dans le nav ET recomposer les liens
        for liens in nav:
            liens_nav[liens.text.strip()] = url_principale + liens["href"]
        return liens_nav


cathegories = recup_liens_cathegori_menu(url_principale)
for key in cathegories:
    urls_cathe = recup_url_cathegorie(cathegories[key])
    # print(urls_1_cathe)
    with open("donnees_scrapees/" + key + ".csv", "a", newline='') as donnees:
        donnees.write("product_page_url , title , product_description , image_url , upc  , product_type , price_exclu_tax  ,  price_including_tax  ,  number_available , review_rating" )
        for url in urls_cathe:
            info_livre = recup_livre(url) # product_page_url + title + product_description + image_url + upc + product_type + price_exclu_tax + price_including_tax + number_available + review_rating
            donnees.write(str(info_livre["product_page_url"]) + ',' + str(info_livre["title"]) + ',' + str(info_livre["product_description"]) + ',' + str(info_livre["image_url"]) + ',' + str(info_livre["upc"]) + ',' + str(info_livre["product_type"]) + ',' + str(info_livre["price_exclu_tax"]) + ',' + str(info_livre["price_including_tax"]) + ',' + str(info_livre["number_available"]) + ',' + str(info_livre["review_rating"]) + '\n')
            donnees.write(str(info_livre))

"""modificer fichier ET récuperer les images (et pas l'url)"""