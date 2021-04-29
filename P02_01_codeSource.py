import requests
from bs4 import BeautifulSoup
import os

url_principale = 'http://books.toscrape.com/'
os.mkdir("données_scrapées")

def recup_info_1livre(url):
    res = requests.get(url)
    if res.ok:
        soup = BeautifulSoup(res.text, 'lxml')
        retour_info_un_livre = {}
        retour_info_un_livre["product_page_url"] = url
        retour_info_un_livre["title"] = soup.find("h1").text
        retour_info_un_livre["product_description"] = soup.select("#product_description+p")
        retour_info_un_livre["image_url"] = 'http://books.toscrape.com/' + soup.find('img')['src']
        tds = soup.findAll("td")
        retour_info_un_livre["upc"] = tds[0].text
        retour_info_un_livre["product_type"] = tds[1].text
        retour_info_un_livre["price_exclu_tax"] = tds[2].text
        retour_info_un_livre["price_including_tax"] = tds[3].text
        retour_info_un_livre["number_available"] = tds[5].text
        retour_info_un_livre["review_rating"] = soup.find("p", {"class": "star-rating"})["class"]
        # retour_info_un_livre["image"] = urllib.request.urlretrieve(image_url)
        return retour_info_un_livre # retour dans fichier csv



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
    urls_1_cathe = recup_url_1cathegorie(cathegories[key])
    # print(urls_1_cathe)
    with open("données_scrapées/" + key + ".csv", "a", newline='') as données:
        données.write("product_page_url , title , product_description , image_url , upc  , product_type , price_exclu_tax  ,  price_including_tax  ,  number_available , review_rating" )
        for url in urls_1_cathe:
            info_livre = recup_info_1livre(url) # product_page_url + title + product_description + image_url + upc + product_type + price_exclu_tax + price_including_tax + number_available + review_rating
            données.write(str(info_livre["product_page_url"]) + ',' + str(info_livre["title"]) + ',' + str(info_livre["product_description"]) + ',' + str(info_livre["image_url"]) + ',' + str(info_livre["upc"]) + ',' + str(info_livre["product_type"]) + ',' + str(info_livre["price_exclu_tax"]) + ',' + str(info_livre["price_including_tax"]) + ',' + str(info_livre["number_available"]) + ',' + str(info_livre["review_rating"]) + '\n')
            données.write(str(info_livre))

"""modificer fichier ET récuperer les images (et pas l'url)"""