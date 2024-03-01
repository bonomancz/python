
O projektu:
-----------
Aplikace slouží ke shromaždění a konsolidaci volebních výsledků z webu https://volby.cz
do výstupního .csv souboru


Spouštění aplikace:
-------------------
Jedná se o script spustitelný v interpretu python.
Aplikace vyžaduje nainstalovaný python interpret a dodatečně instalované moduly.
Seznam potřebných modulů je vypsán v souboru requirements.txt.
Aplikace vyžaduje 2 argumenty. 
První je cílové URL, odkud bude scrapovat data. 
Druhý argument je cesta k výstupnímu datovému souboru s výsledky.
Příklad spuštění
python webscraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"


Instalace potřebných souborů pro python:
----------------------------------------
pip3 install requests
pip3 install bs4
atd.
