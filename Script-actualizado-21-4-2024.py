import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

df = pd.read_excel('.xlsx')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

urls_fallidas = []

def esperar_descarga(driver, selector, timeout=10):
    """Espera hasta que el botón de descarga sea clickeable o hasta que el timeout expire"""
    for i in range(timeout):
        try:
            download_button = driver.find_element(By.CSS_SELECTOR, selector)
            if download_button:
                download_button.click()
                return True
        except:
            time.sleep(2)
    return False

for url in df['Url']:
    if pd.notna(url):
        try:
            driver.get(url)
            success = esperar_descarga(driver, "a.btn.btn-flat.btn-h[rel='noopener'][target='_blank'][title='Descargar PDF de esta norma']")
            if not success:
                raise Exception("Botón de descarga no encontrado")
        except Exception as e:
            print(f"No se encontró el botón de descarga para la URL {url}: {e}")
            urls_fallidas.append(url)

with open('urls_fallidas.txt', 'w') as file:
    for url in urls_fallidas:
        file.write(url + '\n')

driver.quit()
