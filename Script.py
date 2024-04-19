import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Cargar el DataFrame
df = pd.read_excel('df/directory.xlsx')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Lista para guardar URLs que no se pudieron descargar
urls_fallidas = []

# Iterar sobre cada URL en la columna 'V' del DataFrame
for url in df['Url']:
    if pd.notna(url):  # Checar si la URL no es NaN
        try:
            driver.get(url)  # Abrir la URL con Selenium
            time.sleep(random.randint(2, 3))  # Esperar entre 2 y 3 segundos
            
            # Intentar encontrar y hacer clic en el botón de descarga
            download_button = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-flat.btn-h[rel='noopener'][target='_blank'][title='Descargar PDF de esta norma']")
            download_button.click()
            time.sleep(random.randint(3, 4))  # Esperar entre 3 y 4 segundos
        except Exception as e:
            print(f"No se encontró el botón de descarga para la URL {url}: {e}")
            urls_fallidas.append(url)  # Agregar la URL fallida a la lista

# Guardar las URLs fallidas en un archivo de texto plano
with open('urls_fallidas.txt', 'w') as file:
    for url in urls_fallidas:
        file.write(url + '\n')

# Cerrar el navegador una vez que todas las URLs han sido procesadas
driver.quit()
