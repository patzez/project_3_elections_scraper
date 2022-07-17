"""
elections_scraper.py: Třetí projekt do Engeto Online Python Akademie

author: Patrik Zezulka
email: pat.zezulka@gmail.com
discord: patzez#8128
"""

import requests
from bs4 import BeautifulSoup


def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7203"
    soup = zpracuj_odpoved_serveru(url)
    mesta = najdi_mesta(soup)
    url_mest = zjisti_url_mesta(mesta)
    udaje_mesta = zjisti_udaje_mesta(mesta)
    volici_mesta = projdi_jednotliva_mesta(url_mest)
    udaje_stran = projdi_udaje_stran(url_mest)
    nazvy_stran = projdi_nazvy_stran(url_mest[0])
    print(len(nazvy_stran))
    # print(udaje_stran)
    print(udaje_mesta[0], volici_mesta[0], len(udaje_stran[0]))
    # for i in range(len(udaje_mesta)):
    #     print(udaje_mesta[i], volici_mesta[i], url_mest[i], udaje_stran[i])


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


def projdi_jednotliva_mesta(url_mest):
    volici_mesta = []

    for url in url_mest:
        soup_mesta = zpracuj_odpoved_serveru(url)
        volici = soup_mesta.find("table", {"class": "table"})
        volici_v_seznamu = volici.find_all("td", {"class": "cislo"})[3].text.replace("\xa0", "")
        vydane_obalky = volici.find_all("td", {"class": "cislo"})[4].text.replace("\xa0", "")
        platne_hlasy = volici.find_all("td", {"class": "cislo"})[7].text.replace("\xa0", "")
        volici_mesta.append([volici_v_seznamu, vydane_obalky, platne_hlasy])

    return volici_mesta


def projdi_udaje_stran(url_mest):
    hlasy_stran = []
    for url in url_mest:
        soup_mesta = zpracuj_odpoved_serveru(url)
        tabulka_hlasy = soup_mesta.find_all("div", {"class": "t2_470"})
        celkova_tabulka = []
        radky_tabulky = []
        celkem_hlasu_mesta = []
        for hlas in tabulka_hlasy:
            radky = hlas.find_all("tr")
            celkova_tabulka.extend(radky)

        for celek in celkova_tabulka:
            radek = celek.find_all("td", {"class": "cislo"})
            if radek:
                radky_tabulky.append(radek)
            else:
                continue

        for radek in radky_tabulky:
            celkem_hlasu_mesta.append(radek[1].text.replace("\xa0", ""))
        hlasy_stran.append(celkem_hlasu_mesta)
    return hlasy_stran


def projdi_nazvy_stran(url):
    nazvy_stran = []
    soup_mesta = zpracuj_odpoved_serveru(url)
    tabulka_nazvy = soup_mesta.find_all("td", {"class": "overflow_name"})
    for nazev in tabulka_nazvy:
        nazvy_stran.append((nazev).text)
    return nazvy_stran


if __name__ == "__main__":
    main()

#format vysledne csv tabulky:
#kod obce, nazev obce, volici v seznamu, vydane obalky, platne hlasy, kandidujici strany