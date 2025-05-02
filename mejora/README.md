
# 📊 Cargador y Visualizador de Red Social

Este proyecto permite **cargar grandes cantidades de datos** (millones de registros) sobre usuarios y sus conexiones sociales, optimizando la lectura con la biblioteca **Polars** y ofreciendo un **resumen visual** de tiempos de carga.

## 🛠 Tecnologías utilizadas

- **Python 3.x**
- [Polars](https://pola.rs/)
- [Matplotlib](https://matplotlib.org/)
- `collections.defaultdict`
- `time`, `os`

---

## 📂 Estructura de archivos esperada

- **`10_million_location.txt`**  
  Formato:  
  ```
  -12.345,-76.543
  -12.346,-76.544
  ...
  ```
  ➔ Cada línea representa la latitud y longitud (en formato float, negativos).

- **`10_million_user.txt`**  
  Formato:  
  ```
  1,2,3,4
  2,5,6
  ...
  ```
  ➔ Cada línea comienza con un ID de usuario, seguido de IDs de usuarios con los que está conectado.

---

## 🚀 ¿Qué hace el código?

1. **Carga ubicaciones**:  
   Utiliza `polars` para cargar millones de coordenadas en segundos, asignando automáticamente un ID a cada ubicación.

2. **Carga conexiones**:  
   Lee las relaciones de amistad de cada usuario y las almacena en un `defaultdict`.

3. **Resumen**:  
   Muestra cuántos datos fueron cargados, la cantidad de usuarios con ubicaciones y conexiones, y un ejemplo práctico.

4. **Visualización**:  
   Grafica un diagrama de barras que compara los tiempos de carga de ambos archivos.

---

## 🖥 ¿Cómo ejecutar?

1️⃣ **Instala las dependencias:**

```bash
pip install polars matplotlib
```

2️⃣ **Verifica los archivos:**

Asegúrate de tener en la misma carpeta:

- `10_million_location.txt`
- `10_million_user.txt`

3️⃣ **Ejecuta el script:**

```bash
python nombre_del_script.py
```

✅ Si todo está bien, verás mensajes como:

```
Cargando ubicaciones desde 10_million_location.txt...
[POLARS] 10,000,000 ubicaciones cargadas en 2.35s

Cargando conexiones desde 10_million_user.txt...
10,000,000 usuarios con 50,000,000 conexiones cargadas en 12.45s
```

Y un **gráfico de barras** mostrando los tiempos de carga.

---

## 🔎 Estructura del código

- **`CargadorRedSocial`**
  - `cargar_ubicaciones()`: Lee y guarda ubicaciones (latitud/longitud) con IDs.
  - `cargar_conexiones()`: Lee y guarda listas de conexiones para cada usuario.
  - `resumen_datos()`: Imprime estadísticas útiles de los datos cargados.

- **`graficar_tiempos()`**
  ➔ Grafica los tiempos de carga en un diagrama de barras.

- **`main()`**
  ➔ Orquesta la carga de datos, imprime los tiempos y muestra la gráfica final.

---

## 🛠 ¿Qué pasa si hay errores en los archivos?

- ❗ Si alguna línea de ubicación no sigue el formato correcto (por ejemplo, texto en lugar de números), **se mostrará un mensaje de error** y esa línea será ignorada.
- ❗ Si alguna línea de conexiones no puede convertirse en enteros, también se mostrará un mensaje y se saltará.

---

## 👥 Integrantes

- Diego Nova
- Angélica Castillo
