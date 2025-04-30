# 📊 Cargador de Datos para Red Social

Este proyecto permite **cargar, procesar y visualizar** datos de una red social a gran escala desde archivos de texto. Está optimizado para manejar millones de usuarios y sus conexiones de forma eficiente y legible.

---

## 📁 Estructura del Proyecto

- `CargadorRedSocial`: Clase que gestiona la carga de ubicaciones y conexiones.
- `graficar_tiempos`: Función para visualizar gráficamente los tiempos de carga.
- `main`: Función principal que ejecuta todo el flujo de trabajo.

---

## 🚀 Funcionalidades

### ✅ Carga de ubicaciones
- Lee un archivo de ubicaciones con formato `latitud,longitud` por línea.
- Almacena los datos en un diccionario:  
  `ubicaciones = {id_usuario: (lat, long)}`
- Reporta progreso cada cierto número de líneas.
- Uso eficiente de memoria con `gc.collect()`.

### ✅ Carga de conexiones
- Lee una lista de adyacencia por usuario (usuarios que sigue).
- Utiliza `defaultdict(list)` para almacenar automáticamente listas vacías si el usuario aún no ha sido agregado:
  ```python
  self.conexiones = defaultdict(list)
  ```
  Esto permite hacer cosas como:
  ```python
  self.conexiones[4].append(8)
  ```
  sin necesidad de verificar si el usuario 4 ya está en el diccionario.

- Estructura resultante:  
  `conexiones = {id_usuario: [usuarios_que_sigue]}`

### ✅ Resumen de datos
- Cantidad de usuarios con ubicación.
- Cantidad de usuarios con conexiones.
- Total de conexiones.
- Usuarios con datos completos.

### 📊 Visualización
- Muestra un gráfico de barras con los tiempos de carga para ubicaciones y conexiones usando `matplotlib`.

---

## 🔧 Dependencias

Este proyecto requiere:

```bash
matplotlib
```

Instálalo con:

```bash
pip install matplotlib
```

---

## 📂 Formato esperado de archivos

### `10_million_location.txt`
```
-12.048392, -77.042793
-12.048294, -77.042788
...
```

### `10_million_user.txt`
```
2, 45, 82
19, 56
...
```

---

## 🧠 Sobre `defaultdict(list)`

El uso de `defaultdict` permite ahorrar código y evitar errores como `KeyError`. En lugar de escribir:

```python
if usuario_id not in conexiones:
    conexiones[usuario_id] = []
conexiones[usuario_id].append(otro_usuario)
```

Solo escribimos:

```python
conexiones[usuario_id].append(otro_usuario)
```

Porque `defaultdict(list)` se encarga de inicializar automáticamente una lista vacía al acceder por primera vez a una clave.

---

## 🖥️ Ejecución

Asegúrate de que los archivos `10_million_location.txt` y `10_million_user.txt` estén en el mismo directorio.

Luego ejecuta:

```bash
python nombre_del_script.py
```

---

## 📝 Ejemplo de salida esperada

```
Cargando ubicaciones desde 10_million_location.txt...
Procesados 100,000 ubicaciones...
Ubicaciones cargadas: 1,000,000 en 12.35 segundos

Cargando conexiones desde 10_million_user.txt...
Procesados 100,000 usuarios con 1,400,000 conexiones...
Conexiones cargadas: 1,000,000 usuarios con 13,800,000 conexiones en 10.87 segundos

Carga de datos completada. Los datos están disponibles en:
- cargador.ubicaciones: Diccionario con ubicaciones {id_usuario: (lat, long)}
- cargador.conexiones: Diccionario con conexiones {id_usuario: [usuarios_que_sigue]}

--- RESUMEN DE DATOS CARGADOS ---
Usuarios con ubicación: 1,000,000
Usuarios con conexiones: 1,000,000
Total de conexiones: 13,800,000
Usuarios con datos completos: 999,985
```

---

## 🧼 Buenas prácticas aplicadas

- ✔️ Uso de `with open(...)` para evitar archivos abiertos innecesariamente.
- ✔️ Control de errores con `try/except` en cada línea.
- ✔️ Limpieza de memoria manual con `gc.collect()`.
- ✔️ Visualización clara del progreso de carga y tiempo de ejecución.

---

## 🐍 Autor
Este script fue diseñado con eficiencia y claridad para cargar redes sociales masivas, con herramientas estándar de Python y visualización con `matplotlib`.

---

¡Espero que este proyecto te ayude a manejar grandes volúmenes de datos de forma efectiva!
