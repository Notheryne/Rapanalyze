import requests
from bs4 import BeautifulSoup

"""page = requests.get("https://www.poeto.pl/list,1000,nev.html")
soup = BeautifulSoup(page.text, 'html.parser')
souph = soup.find_all("h1")
soupu = soup.find_all("li")
urls = []

for s in souph:
    try:
        urls.append(s.find("a", href=True)["href"])
    except TypeError:
        continue
urls = urls[1:]
#print(urls)
start = "https://www.poeto.pl"
urls = [start + url for url in urls]
print(urls)"""

page = requests.get("https://www.poeto.pl/wiersz/224187/Milosc")
soup = BeautifulSoup(page.text, 'html.parser')
soup = soup.find("p", {"class" : "essence"})
text = soup.get_text("\n").strip("\n").strip(" ").strip("\n").strip(" ")

index = text.find("Kategoria:")
meta = text[index:]
index2 = meta.find(":")
category = meta[index2+2:].strip("\n")

text = text[:text.find("Autor:")].strip("\n")


wiersze = [[text,category]]
print(wiersze[0][1])
#index = text.find("Kategoria:")
#meta = text[index:]
