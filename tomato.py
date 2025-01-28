import matplotlib.pyplot as plt
import psutil
import time
import subprocess

url_base = "/var/www/html/tomato/"
# url_base = "C:/xampp/htdocs/tomato/"

######################
## MÉTRICAS SISTEMA ##
######################

carga_cpu = psutil.cpu_percent(interval=1)
carga_ram = psutil.virtual_memory().percent
uso_disco = psutil.disk_usage('/').percent

# uso de red en intervalo
data_inicio = psutil.net_io_counters()
######################################
## INTERVÁLO CONFIGURADO: 1 segundo ##
time.sleep(1)  
######################################
data_final = psutil.net_io_counters()

descarga_mbps = (data_final.bytes_recv - data_inicio.bytes_recv) / (1024 * 1024)
subida_mbps = (data_final.bytes_sent - data_inicio.bytes_sent) / (1024 * 1024)

# temperatura
def obtener_temperaturas():
    try:
        sensores = subprocess.check_output(['sensors'], encoding='utf-8')
        for linea in sensores.splitlines():
            if 'Core' in linea:  # Filtrar para núcleos de CPU
                temp = float(linea.split()[1].strip('+').strip('°C'))
                yield temp
    except Exception as e:
        print(f"Error al obtener temperaturas: {e}")
        return []

temperaturas = list(obtener_temperaturas())
if not temperaturas:
    temperaturas = [0]

temperatura_promedio = sum(temperaturas) / len(temperaturas)

# número de conexiones
num_conexiones = len(psutil.net_connections())

########################################
## GUARDAR MÉTRICAS EN TXT: carga.txt ##
ruta_archivo = url_base + "carga.txt"
########################################
with open(ruta_archivo, 'a') as archivo:
    archivo.write(f"{carga_cpu},{carga_ram},{uso_disco},{descarga_mbps},{subida_mbps},{temperatura_promedio},{num_conexiones}\n")

# Leer y procesar el archivo para las gráficas
with open(ruta_archivo, 'r') as archivo:
    lineas = archivo.readlines()

datos_cpu, datos_ram, datos_disco = [], [], []
datos_descarga, datos_subida = [], []
datos_temperatura, datos_conexiones = [], []
for linea in lineas:
    linea = linea.strip()
    if linea:
        cpu, ram, disco, descarga, subida, temp, conexiones = map(float, linea.split(','))
        datos_cpu.append(cpu)
        datos_ram.append(ram)
        datos_disco.append(disco)
        datos_descarga.append(descarga)
        datos_subida.append(subida)
        datos_temperatura.append(temp)
        datos_conexiones.append(conexiones)
        
######################
## GENERAR GRÁFICAS ##
######################

# cpu
plt.figure(figsize=(10, 6))
plt.plot(datos_cpu, label='CPU', marker='o', color='blue')
plt.grid(True)
plt.ylim(0, 100)
plt.title('Uso de CPU')
plt.xlabel('Muestras')
plt.ylabel('Porcentaje de Uso')
plt.legend()
plt.savefig(url_base + "carga_cpu.jpg")
plt.close()

# ram
plt.figure(figsize=(10, 6))
plt.plot(datos_ram, label='RAM', marker='s', color='green')
plt.grid(True)
plt.ylim(0, 100)
plt.title('Uso de RAM')
plt.xlabel('Muestras')
plt.ylabel('Porcentaje de Uso')
plt.legend()
plt.savefig(url_base + "carga_ram.jpg")
plt.close()

# disco duro
plt.figure(figsize=(10, 6))
plt.plot(datos_disco, label='Disco', marker='^', color='red')
plt.grid(True)
plt.ylim(0, 100)
plt.title('Uso de Disco')
plt.xlabel('Muestras')
plt.ylabel('Porcentaje de Uso')
plt.legend()
plt.savefig(url_base + "carga_disco.jpg")
plt.close()

# red
plt.figure(figsize=(10, 6))
plt.plot(datos_descarga, label='Descarga (Mbps)', marker='o', color='purple')
plt.plot(datos_subida, label='Subida (Mbps)', marker='x', color='orange')
plt.grid(True)
plt.title('Uso de Red')
plt.xlabel('Muestras')
plt.ylabel('Velocidad (Mbps)')
plt.legend()
plt.savefig(url_base + "carga_red.jpg")
plt.close()

# temperatura
plt.figure(figsize=(10, 6))
plt.plot(datos_temperatura, label='Temperatura (°C)', marker='*', color='cyan')
plt.grid(True)
plt.title('Temperatura de los Componentes')
plt.xlabel('Muestras')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.savefig(url_base + "carga_temperatura.jpg")
plt.close()

# número de conexiones
plt.figure(figsize=(10, 6))
plt.plot(datos_conexiones, label='Conexiones Activas', marker='d', color='magenta')
plt.grid(True)
plt.title('Número de Conexiones Activas')
plt.xlabel('Muestras')
plt.ylabel('Conexiones')
plt.legend()
plt.savefig(url_base + "carga_conexiones.jpg")
plt.close()

print("Métricas guardadas y gráficas generadas correctamente.")
