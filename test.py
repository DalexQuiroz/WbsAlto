from flask import Flask, render_template
import threading
import time
from datetime import datetime  # Importar el módulo datetime
from zeep import Client


app = Flask(__name__)

class SOAPClient:
    def __init__(self, wsdl_url):
        self.client = Client(wsdl_url)

    def call_service(self, xml_data):
        return self.client.service.ProcessXML(xmlSerializado=xml_data)

# Lista para almacenar el historial de respuestas junto con la hora
response_history = []

def background_task():
    wsdl_url = 'http://ws4.altotrack.com/WSPosiciones_Chep/WSPosiciones_Chep.svc?singleWsdl'
    soap_client = SOAPClient(wsdl_url)
    
    while True:
        # Obtener la hora actual
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Llamar al método del servicio SOAP
        response = soap_client.call_service('<registro><movil><proveedor>Fulltime</proveedor><nombremovil>03AM8A</nombremovil><patente>03AM8A</patente><fecha>08-03-2024 09:40:00</fecha><latitud>19.499843</latitud><longitud>-99.234161</longitud><direccion>180</direccion><velocidad>60</velocidad><ignicion>1</ignicion><GPSLinea>1</GPSLinea><LOGGPS>0</LOGGPS><puerta1>0</puerta1><evento>0</evento></movil></registro>')
        
        # Imprimir la respuesta del servidor en la consola del servidor Flask junto con la hora
        print(f"{current_time}: {response}")

        # Agregar la respuesta junto con la hora al historial
        response_history.append((current_time, response))
        
        # Esperar 5 minutos antes de la próxima llamada
        time.sleep(60)  # 300 segundos = 5 minutos

@app.route('/')
def index():
    # Renderizar la plantilla HTML con el historial de respuestas y la hora
    return render_template('index.html', response_history=response_history)

if __name__ == '__main__':
    # Iniciar un hilo separado para ejecutar la tarea en segundo plano
    background_thread = threading.Thread(target=background_task)
    background_thread.daemon = True
    background_thread.start()

    # Ejecutar el servidor Flask
    app.run(debug=True)
