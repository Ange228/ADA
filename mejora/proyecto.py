import time
import os
import polars as pl
from collections import defaultdict
import matplotlib.pyplot as plt

class CargadorRedSocial:
    def __init__(self):
        self.ubicaciones = {}  # {id: (lat, lon)}
        self.conexiones = defaultdict(list)  # {id: [conexiones]}
    
    def cargar_ubicaciones(self, archivo):
        """Carga ubicaciones desde archivo con formato: lat,lon (float negativos)"""
        print(f"\nCargando ubicaciones desde {archivo}...")
        inicio = time.time()
        
        try:
            # cargar el txt con polar
            df = pl.read_csv(
                archivo,
                has_header=False,
                separator=',',
                new_columns=['lat', 'lon'],
                dtypes={'lat': pl.Float64, 'lon': pl.Float64}
            )
            
            # Asignar IDs automáticamente (1-based)
            self.ubicaciones = {
                idx + 1: (row['lat'], row['lon'])
                for idx, row in enumerate(df.iter_rows(named=True))
            }
            
            print(f"[POLARS] {len(self.ubicaciones):,} ubicaciones cargadas en {time.time() - inicio:.2f}s")
            
        except Exception as e:
            print(f"Error con carga ubi: {e}\n") 
 
    def cargar_conexiones(self, archivo, lote=100000):
        """Carga conexiones desde archivo con formato: id,id1,id2,..."""
        print(f"\nCargando conexiones desde {archivo}...")
        inicio = time.time()
        contador = total_conex = 0
        
        try:
            with open(archivo, 'r') as f:
                for line_num, linea in enumerate(f, 1):
                    try:
                        ids = list(map(int, filter(None, linea.strip().split(','))))
                        if ids:
                            self.conexiones[ids[0]] = ids[1:]
                            contador += 1
                            total_conex += len(ids[1:])
                            
                            #if contador % lote == 0:
                            #    print(f"Procesados {contador:,} usuarios ({total_conex:,} conexiones)...")
                    except Exception as e:
                        print(f"Línea {line_num}: Error - {e}")
        
        except Exception as e:
            print(f"Error con conexiones: {e}")
        
        print(f"{contador:,} usuarios con {total_conex:,} conexiones cargadas en {time.time() - inicio:.2f}s")
        print(f"Promedio: {total_conex/contador:.1f} conexiones/usuario")

    def resumen_datos(self):
        """Muestra estadísticas de los datos cargados"""
        print("\n" + "="*50)
        print("RESUMEN DE DATOS".center(50))
        print("="*50)
        
        print(f"\n● Ubicaciones cargadas: {len(self.ubicaciones):,}")
        #print(f"● Usuarios con conexiones: {len(self.conexiones):,}") el tamaño de conexiones
        print(f"● Total conexiones: {sum(len(v) for v in self.conexiones.values()):,}")
        
        if self.ubicaciones and self.conexiones:
            comunes = set(self.ubicaciones) & set(self.conexiones)
            print(f"\n● Usuarios completos (ubicación + conexiones): {len(comunes):,}")
            
            # Ejemplo de datos
            ej_id = next(iter(comunes), 1)
            print(f"\nEjemplo usuario {ej_id}:")
            print(f"  Ubicación: {self.ubicaciones.get(ej_id)}")
            print(f"  Conexiones: {self.conexiones.get(ej_id)[:5]} [...] (total: {len(self.conexiones.get(ej_id, []))})")


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
    cargador = CargadorRedSocial()
    
    # Configuración
    archivos = {
        'ubicaciones': "10_million_location.txt",
        'conexiones': "10_million_user.txt"
    }
    
    # Verificar archivos
    for tipo, archivo in archivos.items():
        if not os.path.exists(archivo):
            print(f"ERROR: No se encuentra {archivo}")
            return
    
    # Carga de datos
    tiempos = {}
    
    print("\n" + "="*50)
    print("INICIANDO CARGA DE DATOS".center(50))
    print("="*50)
    
    inicio = time.time()
    cargador.cargar_ubicaciones(archivos['ubicaciones'])
    tiempos['ubicaciones'] = time.time() - inicio
    
    inicio = time.time()
    cargador.cargar_conexiones(archivos['conexiones'])
    tiempos['conexiones'] = time.time() - inicio
    
    # Resultados
    cargador.resumen_datos()
    
    print("\n" + "="*50)
    print("TIEMPOS DE EJECUCIÓN".center(50))
    print("="*50)
    for k, v in tiempos.items():
        print(f"  {k.upper():<12}: {v:.2f} segundos")
    print(f"\n  TOTAL       : {sum(tiempos.values()):.2f} segundos")


    graficar_tiempos(tiempos)

if __name__ == "__main__":
    main()