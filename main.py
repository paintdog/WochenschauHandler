import datetime

import requests
from bs4 import BeautifulSoup

url = "https://www.wochenschau-verlag.de/Reihe/Methoden-historischen-Lernens?order=name-asc&p={page}"


def download2soup(url):
    """Downloads a webpage by its URL and returns it as a BeautifulSoup object."""
    html = requests.get(url)
    with open("dump.html", "w", encoding="utf-8") as f:
        f.write(html.text)
    # print("Dump abgespeichert...")
    # html2soup
    soup = BeautifulSoup(html.text, "html5lib")
    return soup

def beautify(string):
    """Cleans up strings"""
    return string.strip('\t\n\r ')

def get_authors(soup):
    """Extracts all author names from a product page’s HTML content."""
    authors = soup.find('dd')
    if authors is None:
        return ['N. N.']
    else:
        author_names = [beautify(author.text) for author in authors]
    return [author_name for author_name in author_names if author_name not in [",", ""]]

def get_edition(soup):
    """Extracts the edition from the product page's HTML content."""
    rows = soup.find_all('tr', class_='properties-row')
    for row in rows:
        if 'Auflage' in row.find('th', class_='properties-label').text:
            return row.find('td', class_='properties-value').text.split(".")[0]
    return "1"

def get_isbn(soup):
    """Extracts the ISBN from the product page's HTML content.
    <span class="product-detail-book_isbn">...</span>
    """
    isbn = beautify(soup.find("span", attrs={"class": "product-detail-book_isbn"}).text)
    if " FF" in isbn:
        isbn = isbn.replace(" FF", "")
    if " / " in isbn:
        one, two = isbn.split(" / ")
        if "(PDF)" in one:
            return one.replace(" (PDF)", "")
        if "(PDF)" in two:
            return two.replace(" (PDF)", "")
    else:
        return beautify(isbn).replace(" (PDF)", "")
    
def get_subtitle(soup):
    """Extracts the subtitle from the product page's HTML content.
    <h2 class="h4">...</h2>
    """
    subtitle = soup.find('h2', attrs={"class": "h4"})
    if subtitle is not None:
        subtitle = subtitle.text.strip('\t\n\r ')
    else:
        subtitle = None
    return subtitle

def get_title(soup):
    """Extracts the title from the product page's HTML content."""
    return soup.find('h1', attrs={"class": "product-detail-name h2"}).text.strip('\t\n\r ')

def get_year(soup):
    """Extracts the release year from the product page's HTML content."""
    rows = soup.find_all('tr', class_='properties-row')
    for row in rows:
        if 'Erscheinungsjahr' in row.find('th', class_='properties-label').text:
            return row.find('td', class_='properties-value').text
    return "o. J."

def output(authors, title, subtitle, ort, verlag, edition, year, reihe, isbn):
    """Creates a string with bibliographic information."""
    output_data = []
    # Authors
    if "N. N." in authors:
        output_data.append("N. N.:")
    else:
        output_data.append("[[" + "]] und [[".join(authors) + "]]:")
    # Title and subtitle
    if subtitle is not None:
        output_data.append(f"''{title}. {subtitle}''.")
    else:
        output_data.append(f"''{title}''.")
    # ort, verlag, edition, year, reihe, isbn
    if edition == "1":
        output_data.append(f"{ort}: {verlag} {year} ({reihe}). ISBN {isbn}")
    elif edition == "2":
        output_data.append(f"{ort}: {verlag} ²{year} ({reihe}). ISBN {isbn}")
    elif edition == "3":
        output_data.append(f"{ort}: {verlag} ³{year} ({reihe}). ISBN {isbn}")
    else:
        output_data.append(f"{ort}: {verlag} <sup>{edition}</sup>{year} ({reihe}). ISBN {isbn}")
    return " ".join(output_data)

def main():
    output_data = []
    print("************************************************************")
    for i in range(1, 2+1):
        url = f"https://www.wochenschau-verlag.de/Reihe/Methoden-historischen-Lernens?order=name-asc&p={i}"

        ort = "Frankfurt am Main"
        verlag = "Wochenschau Verlag"
        reihe = "Methoden historischen Lernens"
        
        # print(url)
        soup = download2soup(url)

        # Retrieve product informations
        product_infos = soup.find_all('div', attrs={"class": "product-info"})
        
        # Extracting product informations
        for item in product_infos:
            # print(item.text)

            # Produkttitel ermitteln und ausgeben - ich erhalte hier die URL zur Produktseite
            products = item.find_all("a", attrs={"class": "product-name"})
            for product in products:
                print(f"Handling: {product.text.strip('\t\n\r ')}...")
                print(f"URL: {product["href"]}\n")

                soup = download2soup(product["href"])
                title = get_title(soup)
                subtitle = get_subtitle(soup)
                authors = get_authors(soup)
                isbn = get_isbn(soup)    # only one isbn (pdf > book)!
                year = get_year(soup)
                edition = get_edition(soup)
                 
                print(f"Autoren:    {authors}")
                print(f"Titel:      {title}")             
                print(f"Untertitel: {subtitle}")
                print(f"Verlagsort: {ort}")  
                print(f"Verlag:     {verlag}")          
                print(f"Auflage:    {edition}")       
                print(f"Jahr:       {year}")     
                print(f"Reihe.      {reihe}")
                print(f"ISBN:       {isbn}")     

                output_data.append(output(authors, title, subtitle, ort, verlag, edition, year, reihe, isbn))
                                 
                print("************************************************************")
                print()
    # output
    for line in output_data:
        print("*", line)
    
if __name__ == "__main__":
    main()


