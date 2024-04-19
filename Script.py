import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

df = pd.read_excel('df/directory.xlsx')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

urls_fallidas = []

for url in df['Url']:
    if pd.notna(url):
        try:
            driver.get(url) 
            time.sleep(random.randint(2, 3))  # Esperar entre 2 y 3 segundos
            
            download_button = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-flat.btn-h[rel='noopener'][target='_blank'][title='Descargar PDF de esta norma']")
            download_button.click()
            time.sleep(random.randint(3, 4))  # Esperar entre 3 y 4 segundos
        except Exception as e:
            print(f"No se encontró el botón de descarga para la URL {url}: {e}")
            urls_fallidas.append(url)
            
with open('urls_fallidas.txt', 'w') as file:
    for url in urls_fallidas:
        file.write(url + '\n')

driver.quit()
