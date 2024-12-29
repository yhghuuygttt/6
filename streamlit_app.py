import streamlit as st
import requests
from bs4 import BeautifulSoup

# URL de la página web con la lista de archivos MP3
url = "https://archive.org/download/LaOrejaDeVanGogh-discografia_ALBUM001"

# Crear una carpeta para guardar los archivos descargados
output_folder = "descargas_mp3"
os.makedirs(output_folder, exist_ok=True)

try:
    # Obtener el contenido HTML de la página
    response = requests.get(url)
    response.raise_for_status()  # Verifica si hay errores en la solicitud
    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar todos los enlaces en la página
    links = soup.find_all("a", href=True)

    # Filtrar los enlaces que terminan en .mp3
    mp3_links = [link["href"] for link in links if link["href"].endswith(".mp3")]

    # Descargar cada archivo MP3
    for i, mp3_link in enumerate(mp3_links, start=1):
        file_name = os.path.join(output_folder, os.path.basename(mp3_link))
        
        # Manejar enlaces relativos
        if not mp3_link.startswith("http"):
            mp3_link = requests.compat.urljoin(url, mp3_link)
        
        print(f"Descargando {mp3_link}...")
        mp3_response = requests.get(mp3_link)
        mp3_response.raise_for_status()
        
        with open(file_name, "wb") as file:
            file.write(mp3_response.content)
        print(f"{i}/{len(mp3_links)} - Archivo guardado como: {file_name}")

    print("¡Descarga completada!")

except requests.RequestException as e:
    print(f"Error al acceder a la página o descargar archivos: {e}")
except Exception as e:
    print(f"Error general: {e}")