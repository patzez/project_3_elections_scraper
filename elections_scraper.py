"""
elections_scraper.py: Třetí projekt do Engeto Online Python Akademie

author: Patrik Zezulka
email: pat.zezulka@gmail.com
discord: patzez#8128
"""

import requests
from bs4 import BeautifulSoup


def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=7&xnumnuts=5104"
    soup = zpracuj_odpoved_serveru(url)
    mesta = najdi_mesta(soup)
    udaje_mesta = zjisti_udaje_mesta(mesta)
    for udaj in udaje_mesta:
        print(udaj)
    print(len(zjisti_udaje_mesta(mesta)))
    #print(mesta)
    # for mesto in najdi_mesta(soup):
    #     print(mesto.prettify())
    #     odkaz = mesto.find("a", href=True)["href"]
    #     print(odkaz)


def zpracuj_odpoved_serveru(url):
    odpoved_url = requests.get(url)
    return BeautifulSoup(odpoved_url.text, "html.parser")


def najdi_mesta(soup):
    mesta = soup.find_all("tr")
    return mesta


def zjisti_udaje_mesta(mesta):
    udaje_mesta = []
    for mesto in mesta:
        nazev_mesta = mesto.find("td", {"class": "overflow_name"})
        kod_mesta = mesto.find("td", {"class": "cislo"})
        url_mesta = mesto.find("a", href=True)
        if nazev_mesta is None:
            continue
        else:
            udaje_mesta.append([kod_mesta.text, nazev_mesta.text, url_mesta["href"]])
    return udaje_mesta



if __name__ == "__main__":
    main()

#format vysledne csv tabulky:
#kod obce, nazev obce, volici v seznamu, vydane obalky, platne hlasy, kandidujici strany