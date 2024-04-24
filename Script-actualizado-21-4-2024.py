import pandas as pd
import requests
from lxml import etree

# Asegúrate de que el archivo Excel está en el mismo directorio que este script o proporciona la ruta completa
archivo_excel = 'source_id_file.xlsx'
df = pd.read_excel(archivo_excel)

# Definir la URL base
base_url = "https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma="

# Definir el espacio de nombres
ns = {'default': 'http://www.leychile.cl/esquemas'}

def obtener_texto_norma(id_norma):
    url = base_url + str(id_norma)
    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = etree.fromstring(response.content)
        textos = tree.xpath('//default:EstructuraFuncional/default:Texto', namespaces=ns)
        textos_concatenados = ' '.join([texto.text for texto in textos if texto.text is not None])
        return textos_concatenados
    except Exception as e:
        return "Error: " + str(e)

# Aplicar la función a cada ID de norma y guardar los resultados en una nueva columna
df['Texto de la Norma'] = df['Identificación de la Norma'].apply(obtener_texto_norma)

# Guardar el DataFrame actualizado en un nuevo archivo CSV
csv_file_path = 'file.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8', sep="~")

