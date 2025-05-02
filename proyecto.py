import time
import gc
import os
from collections import defaultdict
import matplotlib.pyplot as plt



class CargadorRedSocial:
    def __init__(self):
        """Inicializa las estructuras para almacenar los datos de la red social"""
        self.ubicaciones = {}  # {id_usuario: (lat, long)}
        self.conexiones = defaultdict(list)  # {id_usuario: [usuarios_que_sigue]}
        # defaultdic Es especialmente útil para las conexiones porque podemos agregar usuarios seguidos
        #  sin verificar primero si el usuario ya existe en el diccionario. esto sirve para todas las conexiones que pertenecen a un usuario
        # y no se a cargado ese usuario conectado
    
    def cargar_ubicaciones(self, archivo, tamano_lote=100000):
        """
        Carga eficientemente las ubicaciones de los usuarios desde un archivo.
        Formato esperado: lat_i, long_i en cada línea
        
        Args:
            archivo: Ruta al archivo de ubicaciones
            tamano_lote: Tamaño del lote para reportar progreso, cada 100000 se estara imprimiendo
        """
        
        print(f"Cargando ubicaciones desde {archivo}...")
        inicio = time.time()
        
        contador = 0
        with open(archivo, 'r') as f:# abrimos el archivo, asignamos el objeto archivo a la var f
            for i, linea in enumerate(f, start=1):  # La indexación comienza en 1, recorremos cada línea del archivo
                            # convierte al archivo en una iterable en una secuencia de pares(indece, val), comenzaremos desde 1 y 
                    # "linea" contendra el texto de cada linea del archivo
                try:
                    # Parsear latitud y longitud
                    partes = linea.strip().split(',')
                    if len(partes) == 2:
                        lat = float(partes[0].strip())
                        long = float(partes[1].strip())
                        self.ubicaciones[i] = (lat, long)# actualizamos el diccionario, i = id. Para obtener los datos usar self.ubicaciones[i]
                        contador += 1
                        
                        # Reportar progreso
                        if contador % tamano_lote == 0:
                            print(f"Procesados {contador:,} ubicaciones...")
                            # Forzar liberación de memoria cada cierto número de lotes
                            if contador % (tamano_lote * 10) == 0:
                                gc.collect()
                except Exception as e:
                    print(f"Error al procesar ubicación en línea {i}: {e}")
        
        tiempo_total = time.time() - inicio
        print(f"Ubicaciones cargadas: {contador:,} en {tiempo_total:.2f} segundos")
        print(f"Tamaño del diccionario de ubicaciones: {len(self.ubicaciones):,} usuarios")
    
    def cargar_conexiones(self, archivo, tamano_lote=100000):
        """
        Carga eficientemente las conexiones de los usuarios desde un archivo.
        Formato esperado: una lista de adyacencia por línea
        
        Args:
            archivo: Ruta al archivo de conexiones
            tamano_lote: Tamaño del lote para reportar progreso
        """
        print(f"Cargando conexiones desde {archivo}...")
        inicio = time.time()
        
        contador_usuarios = 0
        contador_conexiones = 0
        
        with open(archivo, 'r') as f: # abrimos el archivo con with para que el archivo se cierre cuando se termina de usar,
                                     # evitamos que el archivo se mantenga abierto despues de usarlo                 
            for i, linea in enumerate(f, start=1):  # La indexación comienza en 1
                try:
                    # Parsear la lista de adyacencia
                    partes = linea.strip().split(',')# separamos por coma y saltamos espacios
                    usuarios_seguidos = [int(id_usuario.strip()) for id_usuario in partes if id_usuario.strip()]# recorre cada elemento de lista 
                        # "partes" con strip eleiminasmos espacios en blanco y con el if id_usuario.strip verificamos que el resultado no este vacio
                        # con int (..) convierte el valor en entero
                    
                    # Guardar conexiones
                    self.conexiones[i] = usuarios_seguidos
                    contador_usuarios += 1
                    contador_conexiones += len(usuarios_seguidos) # contamos la SOLO la cantidad de conexiones que tiene cada usuario
                    
                    # Reportar progreso
                    if contador_usuarios % tamano_lote == 0:
                        print(f"Procesados {contador_usuarios:,} usuarios con {contador_conexiones:,} conexiones...")
                        # Forzar liberación de memoria cada cierto número de lotes
                        if contador_usuarios % (tamano_lote * 10) == 0:
                            gc.collect()# LIBERAMOS LA MEMORIA
                except Exception as e:
                    print(f"Error al procesar conexiones en línea {i}: {e}")
        
        tiempo_total = time.time() - inicio
        print(f"Conexiones cargadas: {contador_usuarios:,} usuarios con {contador_conexiones:,} conexiones en {tiempo_total:.2f} segundos")
        print(f"Promedio de conexiones por usuario: {contador_conexiones/contador_usuarios:.2f}")
    
    def resumen_datos(self):
        """Muestra un resumen de los datos cargados"""
        print("\n--- RESUMEN DE DATOS CARGADOS ---")
        print(f"Usuarios con ubicación: {len(self.ubicaciones):,}")
        print(f"Usuarios con conexiones: {len(self.conexiones):,}")
        
        # Calcular total de conexiones
        total_conexiones = sum(len(conexiones) for conexiones in self.conexiones.values())
        print(f"Total de conexiones: {total_conexiones:,}")
        
        # Verificar integridad básica
        usuarios_en_ambos = set(self.ubicaciones.keys()) & set(self.conexiones.keys())
        print(f"Usuarios con datos completos: {len(usuarios_en_ambos):,}")

# PARA GENERAR GRÁFICOS

def graficar_tiempos(tiempos):
    """
    Genera un gráfico de barras con los tiempos de carga de archivos.
    
    Args:
        tiempos: Diccionario con etiquetas y tiempos de carga. Ejemplo: {'Ubicaciones': 12.3, 'Conexiones': 8.7}
    """
    etiquetas = list(tiempos.keys())
    valores = list(tiempos.values())
    
    plt.figure(figsize=(8, 5))
    plt.bar(etiquetas, valores, color=['blue', 'red'])
    plt.title("Tiempo de carga de archivos")
    plt.ylabel("Tiempo (segundos)")
    plt.xlabel("Tipo de archivo")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for i, v in enumerate(valores):
        plt.text(i, v + 0.2, f"{v:.2f}s", ha='center', fontsize=10)
    plt.tight_layout()
    plt.show()


def main():
    # Crear instancia del cargador
    cargador = CargadorRedSocial()
    
    # Rutas de los archivos (ajustar según corresponda)
    archivo_ubicaciones = "10_million_location.txt"
    archivo_conexiones = "10_million_user.txt"
    
    # Verificar si los archivos existen
    if not os.path.exists(archivo_ubicaciones):
        print(f"Error: No se encuentra el archivo {archivo_ubicaciones}")
        return
    
    if not os.path.exists(archivo_conexiones):
        print(f"Error: No se encuentra el archivo {archivo_conexiones}")
        return
    
    tiempos = {}

    # Cargar datos
    t_inicio = time.time()
    cargador.cargar_ubicaciones(archivo_ubicaciones)
    tiempos['ubicaciones'] = time.time() - t_inicio
    
    t_inicio = time.time()
    cargador.cargar_conexiones(archivo_conexiones)
    tiempos['Conexiones'] = time.time() - t_inicio
    
    print (cargador.ubicaciones[4])
    print (cargador.conexiones[4])
    # Mostrar resumen       
    
    
    print("\nCarga de datos completada. Los datos están disponibles en:")
    print("- cargador.ubicaciones: Diccionario con ubicaciones {id_usuario: (lat, long)}")
    print("- cargador.conexiones: Diccionario con conexiones {id_usuario: [usuarios_que_sigue]}")

    cargador.resumen_datos()
    graficar_tiempos(tiempos)


if __name__ == "__main__":#Esta condición se cumple solo si el archivo actual se ejecuta directamente
    inicio_total = time.time()# registramos desde el tiempo actual
    main()
    tiempo_total = time.time() - inicio_total # Calcula el tiempo transcurrido restando el tiempo actual del tiempo de inicio.
    print(f"\nTiempo total de ejecución: {tiempo_total:.2f} segundos")