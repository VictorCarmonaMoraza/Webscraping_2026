import requests
from bs4 import BeautifulSoup
import re

url = "https://www.transfermarkt.es/antony/profil/spieler/602105#google_vignette"
url2 = "https://www.transfermarkt.es/kylian-mbappe/profil/spieler/342229#google_vignette"
url3 = "https://www.transfermarkt.es/cristiano-ronaldo/profil/spieler/8198"
url4 = "https://www.transfermarkt.es/lionel-messi/profil/spieler/28003"
'''headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}'''

'''html = requests.get(url2, headers=headers)
print(html)'''
equipos = []
estimacion_mercado = []

def create_object_beatifulSoup(url):
    soup = BeautifulSoup(url.content, "html.parser")

    # Creamos el objeto BeautifulSoup
    ##soup = BeautifulSoup(html.content, "html.parser")

    # Busca el enlace con la clase correcta
    valores = soup.find_all("a", {"class": "data-header__market-value-wrapper"})

    for v in valores:
        texto = v.get_text(strip=True)
        ##print("💰 Valor de mercado:", texto)

    regex_valor = re.compile(r'\d+,\d+')

    # 2️⃣ Buscamos el patrón
    match = regex_valor.search(valores[0].get_text(strip=True))

    if match:
        numero_str = match.group(0)
        numero_float = float(numero_str.replace(",", "."))
        print("💰 Valor numérico:", numero_float)
        estimacion_mercado.append(numero_float)
    else:
        print("❌ No se encontró ningún número.")

    # Obtenemos su equipo actual
    equipoHTML = soup.find_all("span", {"class": "data-header__club"})
    for equipo in equipoHTML:
        equipo_texto = equipo.get_text(strip=True)
        print("🏟️ Equipo actual:", equipo_texto)
        equipos.append(equipo_texto)

    # nameHTML = soup.find_all("h1", {"class ": "data-header__headline-wrapper"})

    # Buscar el contenedor del nombre
    nombre_tag = soup.find("h1", class_="data-header__headline-wrapper")

    if nombre_tag:
        nombre = nombre_tag.find("strong").text.strip()  # Extrae el texto dentro del <strong>
        print("👤 Nombre del jugador:", nombre)
    else:
        print("❌ No se encontró el nombre del jugador.")


url_jugadores = {
    'Antony': url,
    'Mbappe': url2,
    'Cristiano_Ronaldo': url3,
    'Lionel_Messi': url4
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.3"
}




for jugador in url_jugadores.keys():
    url = url_jugadores[jugador]
    headers = headers
    html = requests.get(url, headers=headers)
    create_object_beatifulSoup(html)
    print(equipos)
    print(estimacion_mercado)
