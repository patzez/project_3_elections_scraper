# project_3_elections_scraper

Třetí projekt do Engeto Python online akademie.

## Popis projektu

Projekt slouží k extrahování výsledků parlamentních voleb z roku 2017. 
Odkaz k prohlédnutí naleznete [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Instalace knihoven

Všechny potřebné knihovny použity v projektu jsou uložené v souboru ```requirements.txt```. 
Pro instalaci doporučuji vytvořit nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

```
$ pip3 --verison                    # ověření verze manageru
$ pip3 install -r requirements.txt  # nainstalování knihoven
```

## Spouštení projektu

Spuštění souboru ```elections_scraper.py``` v rámci příkazového řádku požaduje dva povinné argumenty.

```python elections_scraper.py "odkaz_uzemniho_celku" "vysledny_soubor.csv"```

Následné se vám stáhnou výsledky jako soubor s příponou ```.csv```.

## Ukázka projektu

Ukázka projektu pro okres Vsetín:

1. argument ```https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7203```
2. argument ```vysledky_vsetin.csv```

Spuštění programu:

```python elections_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7203" "vysledky_vsetin.csv"```

Průběh programu:

```
Stahuji data z url: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7203
Ukládám data do souboru: vysledky_vsetin.csv
Ukončuji elections_scraper.py
```

Částečný výstup:

```
Kód obce,Název obce,Voliči v seznamu,Vydané obálky,Platné Hlasy,Občanská demokratická strana,...
541648,Branky,771,455,453,25,0,0,18,0,14,42,6,4,4,0,0,51,0,21,156,0,1,37,1,5,0,67,1
541711,Bystřička,814,549,543,76,2,0,35,1,26,20,10,5,6,0,1,57,1,21,181,0,1,32,1,3,1,61,2
541800,Dolní Bečva,1551,945,942,88,0,0,75,0,37,54,7,7,10,0,2,79,0,29,257,1,1,171,6,1,2,113,2
542644,Francova Lhota,1305,761,757,67,0,0,42,0,43,39,10,10,21,1,2,67,0,18,174,1,1,151,2,1,2,98,7
...
```

