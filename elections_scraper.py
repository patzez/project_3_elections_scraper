"""
elections_scraper.py: Třetí projekt do Engeto Online Python Akademie

author: Patrik Zezulka
email: pat.zezulka@gmail.com
discord: patzez#8128
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Pro spuštění je potřeba zapsat argumenty v následujícím tvaru:",
              "elections_scraper.py 'URL' 'název_souboru.csv'",
              sep="\n")
    elif "volby.cz" not in sys.argv[1]:
        print("Špatně zadaná adresa webu!")
    elif ".csv" not in sys.argv[2]:
        print("Název souboru musí končit '.csv' (např. 'vysledky.csv')")
    else:
        zapis_do_csv(sys.argv[1], sys.argv[2])
    print("Ukončuji elections_scraper.py")


def zpracuj_odpoved_serveru(url):
    odpoved_url = requests.get(url)
    return BeautifulSoup(odpoved_url.text, "html.parser")


def najdi_mesta(url):
    soup = zpracuj_odpoved_serveru(url)
    mesta = soup.find_all("tr")
    return mesta


def zjisti_udaje_mesta(url):
    mesta = najdi_mesta(url)
    udaje_mesta = []
    for mesto in mesta:
        nazev_mesta = mesto.find("td", {"class": "overflow_name"})
        kod_mesta = mesto.find("td", {"class": "cislo"})
        if nazev_mesta:
            udaje_mesta.append([kod_mesta.text, nazev_mesta.text])
        else:
            continue
    return udaje_mesta


def zjisti_url_mesta(url):
    mesta = najdi_mesta(url)
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


def projdi_nazvy_stran(url_mesta):
    nazvy_stran = []
    soup_mesta = zpracuj_odpoved_serveru(url_mesta)
    tabulka_nazvy = soup_mesta.find_all("td", {"class": "overflow_name"})
    for nazev in tabulka_nazvy:
        nazvy_stran.append(nazev.text)
    return nazvy_stran


def vytvor_hlavicku_tabulky(url):
    url_mesta = zjisti_url_mesta(url)[0]
    hlavicka_tabulky = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné Hlasy"]
    nazvy_stran = projdi_nazvy_stran(url_mesta)
    hlavicka_tabulky.extend(nazvy_stran)
    return hlavicka_tabulky


def vytvor_vysledky_obce(url):
    url_mest = zjisti_url_mesta(url)
    vysledky_obce = zjisti_udaje_mesta(url)
    volici_mesta = projdi_jednotliva_mesta(url_mest)
    vysledky_stran = projdi_udaje_stran(url_mest)
    for i in range(len(vysledky_obce)):
        vysledky_obce[i].extend(volici_mesta[i])
    for j in range(len(vysledky_obce)):
        vysledky_obce[j].extend(vysledky_stran[j])
    return vysledky_obce


def zapis_do_csv(url, nazev_souboru):
    print(f"Stahuji data z url: {url}")
    vysledky_obce = vytvor_vysledky_obce(url)
    hlavicka_tabulky = vytvor_hlavicku_tabulky(url)
    print(f"Ukládám data do souboru: {nazev_souboru}")
    with open(nazev_souboru, "w", newline="") as f:
        thewriter = csv.writer(f)
        thewriter.writerow(hlavicka_tabulky)
        for radek in vysledky_obce:
            thewriter.writerow(radek)


if __name__ == "__main__":
    main()
