"""
elections_scraper.py: Třetí projekt do Engeto Online Python Akademie

author: Patrik Zezulka
email: pat.zezulka@gmail.com
discord: patzez#8128
"""

import requests
from bs4 import BeautifulSoup


def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7204"
    soup = zpracuj_odpoved_serveru(url)
    mesta = najdi_mesta(soup)
    info_mesta = projdi_jednotliva_mesta(mesta)
    print(info_mesta)


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
        if nazev_mesta:
            udaje_mesta.append([kod_mesta.text, nazev_mesta.text])
        else:
            continue
    return udaje_mesta


def zjisti_url_mesta(mesta):
    url_mest = []
    for mesto in mesta:
        url_mesta = mesto.find("a", href=True)
        if url_mesta:
            url_mest.append("https://volby.cz/pls/ps2017nss/" + url_mesta["href"])
        else:
            continue
    return url_mest


def projdi_jednotliva_mesta(mesta):
    udaje_mesta = zjisti_udaje_mesta(mesta)
    url_mest = zjisti_url_mesta(mesta)

    for i, url in enumerate(url_mest):
        soup_mesta = zpracuj_odpoved_serveru(url)
        volici = soup_mesta.find("table", {"class": "table"})
        volici_v_seznamu = volici.find_all("td", {"class": "cislo"})[3].text.replace("\xa0", "")
        vydane_obalky = volici.find_all("td", {"class": "cislo"})[4].text.replace("\xa0", "")
        platne_hlasy = volici.find_all("td", {"class": "cislo"})[7].text.replace("\xa0", "")
        udaje_mesta[i].extend((volici_v_seznamu, vydane_obalky, platne_hlasy))

    return udaje_mesta










if __name__ == "__main__":
    main()

#format vysledne csv tabulky:
#kod obce, nazev obce, volici v seznamu, vydane obalky, platne hlasy, kandidujici strany