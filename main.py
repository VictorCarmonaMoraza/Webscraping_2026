import requests
from bs4 import BeautifulSoup
import re

url = "https://www.transfermarkt.es/antony/profil/spieler/602105#google_vignette"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

html = requests.get(url, headers=headers)
print(html)

# Creamos el objeto BeautifulSoup
soup = BeautifulSoup(html.content, "html.parser")


# Busca el enlace con la clase correcta
valores = soup.find_all("a", {"class": "data-header__market-value-wrapper"})

for v in valores:
    texto = v.get_text(strip=True)
    print("💰 Valor de mercado:", texto)

regex_valor = re.compile(r'\d+,\d+')

# 2️⃣ Buscamos el patrón
match = regex_valor.search(valores[0].get_text(strip=True))

if match:
    numero_str = match.group(0)              # Extrae el texto: "30,00"
    numero_float = float(numero_str.replace(",", "."))  # Convierte a 30.0
    print("💰 Valor numérico:", numero_float)
else:
    print("❌ No se encontró ningún número.")

# Obtenemos su equipo actual
equipoHTML = soup.find_all("span", {"class": "data-header__club"})
for equipo in equipoHTML:
    equipo_texto = equipo.get_text(strip=True)
    print("🏟️ Equipo actual:", equipo_texto)


#nameHTML = soup.find_all("h1", {"class ": "data-header__headline-wrapper"})

# Buscar el contenedor del nombre
nombre_tag = soup.find("h1", class_="data-header__headline-wrapper")

if nombre_tag:
    nombre = nombre_tag.find("strong").text.strip()  # Extrae el texto dentro del <strong>
    print("👤 Nombre del jugador:", nombre)
else:
    print("❌ No se encontró el nombre del jugador.")
