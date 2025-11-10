import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import openpyxl

# URLs de jugadores
url_jugadores = {
    'Antony': "https://www.transfermarkt.es/antony/profil/spieler/602105",
    'Mbappe': "https://www.transfermarkt.es/kylian-mbappe/profil/spieler/342229",
    'Cristiano_Ronaldo': "https://www.transfermarkt.es/cristiano-ronaldo/profil/spieler/8198",
    'Lionel_Messi': "https://www.transfermarkt.es/lionel-messi/profil/spieler/28003"
}

# Encabezados HTTP (para evitar bloqueos)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.3"
}

# Listas globales
equipos = []
estimacion_mercado = []

def create_object_beautifulSoup(url):
    """Extrae información de un jugador usando find_all()"""
    global equipos, estimacion_mercado

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # 🔹 Valor de mercado
    valores = soup.find_all("a", {"class": "data-header__market-value-wrapper"})
    valor = None
    if valores:  # si hay al menos un resultado
        texto = valores[0].get_text(strip=True)
        regex_valor = re.compile(r'\d+,\d+')
        match = regex_valor.search(texto)
        if match:
            valor = float(match.group(0).replace(",", "."))
            print("💰 Valor numérico:", valor)
        else:
            print("❌ No se encontró valor numérico dentro del texto.")
    else:
        print("❌ No se encontró etiqueta de valor.")

    # 🔹 Equipo actual
    equipos_html = soup.find_all("span", {"class": "data-header__club"})
    if equipos_html:
        equipo = equipos_html[0].get_text(strip=True)
        print("🏟️ Equipo actual:", equipo)
    else:
        equipo = None
        print("❌ No se encontró el equipo.")

    # 🔹 Nombre del jugador
    nombres = soup.find_all("h1", {"class": "data-header__headline-wrapper"})
    if nombres:
        strongs = nombres[0].find_all("strong")
        if strongs:
            nombre = strongs[0].get_text(strip=True)
            print("👤 Nombre del jugador:", nombre)
        else:
            nombre = "Desconocido"
    else:
        nombre = "Desconocido"
        print("❌ No se encontró el nombre.")

    # Guardamos en las listas globales
    equipos.append(equipo)
    estimacion_mercado.append(valor)
    print("-" * 40)


def create_data_frame():
    """Crea el DataFrame con los datos obtenidos."""
    data = {
        'Jugador': list(url_jugadores.keys()),
        'Equipo': equipos,
        'Estimacion_Mercado_Millones_Euros': estimacion_mercado
    }
    df_data = pd.DataFrame(data)
    print("\n📊 DataFrame generado:\n")
    print(df_data)
    return df_data


# 🔁 Recorremos todos los jugadores
for jugador, url in url_jugadores.items():
    print(f"Procesando {jugador}...")
    create_object_beautifulSoup(url)

# 📊 Creamos el DataFrame al final
df = create_data_frame()

#exportar datframe a excel
df.to_excel("jugadores_valor_mercado.xlsx", index=False)


