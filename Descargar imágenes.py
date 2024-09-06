import requests
from bs4 import BeautifulSoup
import html5lib
import os

# URL a la página web
url = 'https://www.animeallstar20.com/2024/07/jujutsu-kaisen-manga-265-espanol.html?m=1'

# Hacer la solicitud a la página
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html5lib')

# Obtener todas las etiquetas <img>
imgHtmlList = soup.find_all("img")

# Crear la carpeta "JJK 267" si no existe
folder_name = "JJK 265"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Inicializar contador para el índice
index = 1

# Lista de fragmentos de nombres de imágenes que no se deben descargar
excluded_keywords = [
    "LogoAllStar2023v2_PNG",
    "Jujutsu_jpg",
    "animationff_gif",
    "face_png"
]

# Bucle para descargar imágenes
for i in imgHtmlList:
    imgUrl = i.get('data-src') or i.get('src')  # Verificar tanto data-src como src
    if imgUrl:
        try:
            # Hacer la solicitud de la imagen
            img = requests.get(imgUrl)
            img.raise_for_status()  # Verificar que la solicitud sea exitosa

            # Obtener el nombre de la imagen desde el URL
            name = imgUrl.split("/")[-1].split("?")[0]  # Limpiar el nombre del archivo

            # Sanear el nombre del archivo
            safe_name = "".join([c if c.isalnum() else "_" for c in name])

            # Crear el nombre del archivo con índice
            file_name = f"{index}_{safe_name}.png"

            # Verificar si el nombre de la imagen contiene alguna palabra clave a excluir
            if not any(keyword in safe_name for keyword in excluded_keywords):
                # Guardar la imagen en la carpeta "JJK 267"
                with open(os.path.join(folder_name, file_name), 'wb') as f:
                    f.write(img.content)
                print(f'Descargando: {file_name}')
                index += 1  # Incrementar el índice para la siguiente imagen
            else:
                print(f'Se omite la descarga de: {file_name} (contiene una palabra clave excluida)')

        except requests.exceptions.RequestException as e:
            print(f"Error al descargar la imagen: {e}")
    else:
        print("No se encontró URL de imagen")
