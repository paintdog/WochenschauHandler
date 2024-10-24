import requests
from bs4 import BeautifulSoup

url = "https://www.wochenschau-verlag.de/Reihe/Methoden-historischen-Lernens?order=name-asc&p={page}"


def download2soup(url):
    html = requests.get(url)
    with open("dump.html", "w", encoding="utf-8") as f:
        f.write(html.text)
    # print("Dump abgespeichert...")
    # html2soup
    soup = BeautifulSoup(html.text, "html5lib")
    return soup
    


for i in range(1, 2+1):
    url = f"https://www.wochenschau-verlag.de/Reihe/Methoden-historischen-Lernens?order=name-asc&p={i}"
    
    # print(url)
    # Abruf der einzelnen Seite
    soup = download2soup(url)

    # Produktinformationen ermitteln
    product_infos = soup.find_all('div', attrs={"class": "product-info"})
    
    # Produktinformationen auswerten
    for item in product_infos:
         # print(item.text)

         # Produkttitel ermitteln und ausgeben
         products = item.find_all("a", attrs={"class": "product-name"})
         for product in products:
             print(f"Handling: {product.text.strip("\t\n\r ")}...")
             
             print(f"URL: {product["href"]}\n")
             
         
