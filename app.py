import streamlit as st
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="Buscador de Películas",
    page_icon="🎬",
    layout="wide"
)

# Función para cargar los datos (usamos cache para no recargar en cada interacción)
@st.cache_data
def cargar_datos():
    # Base de datos simulada para el ejemplo
    datos = {
        "Título": [
            "Cadena Perpetua", "El Padrino", "El Padrino 2", "El Caballero Oscuro", 
            "12 Hombres sin Piedad", "La Lista de Schindler", "El Señor de los Anillos: El Retorno del Rey", 
            "Pulp Fiction", "El Bueno, el Feo y el Malo", "Forrest Gump",
            "Matrix", "Origen", "El Señor de los Anillos: La Comunidad del Anillo", 
            "Star Wars: Episodio V", "Interstellar", "Parásitos",
            "Uno de los nuestros", "El lobo de Wall Street", "Seven"
        ],
        "Año": [
            1994, 1972, 1974, 2008, 
            1957, 1993, 2003, 
            1994, 1966, 1994,
            1999, 2010, 2001, 
            1980, 2014, 2019,
            1990, 2013, 1995
        ],
        "Director": [
            "Frank Darabont", "Francis Ford Coppola", "Francis Ford Coppola", "Christopher Nolan",
            "Sidney Lumet", "Steven Spielberg", "Peter Jackson",
            "Quentin Tarantino", "Sergio Leone", "Robert Zemeckis",
            "Lana Wachowski, Lilly Wachowski", "Christopher Nolan", "Peter Jackson",
            "Irvin Kershner", "Christopher Nolan", "Bong Joon Ho",
            "Martin Scorsese", "Martin Scorsese", "David Fincher"
        ],
        "Calificación": [
            9.3, 9.2, 9.0, 9.0, 
            9.0, 9.0, 9.0, 
            8.9, 8.8, 8.8,
            8.7, 8.8, 8.8, 
            8.7, 8.6, 8.5,
            8.7, 8.2, 8.6
        ],
        "Género": [
            "Drama", "Crimen/Drama", "Crimen/Drama", "Acción/Crimen",
            "Drama", "Biografía/Drama", "Aventura/Fantasía",
            "Crimen/Drama", "Western", "Drama/Romance",
            "Ciencia Ficción/Acción", "Ciencia Ficción/Acción", "Aventura/Fantasía",
            "Ciencia Ficción/Aventura", "Ciencia Ficción/Drama", "Thriller/Comedia",
            "Crimen/Drama", "Biografía/Comedia", "Crimen/Misterio"
        ]
    }
    return pd.DataFrame(datos)

# Cargar los datos en un DataFrame de pandas
df = cargar_datos()

# --- INTERFAZ DE USUARIO ---

st.title("🎬 Buscador de Películas Mejor Calificadas")
st.markdown("Encuentra las mejores películas filtrando por **Año** o por **Director**. Los resultados se mostrarán ordenados por su calificación.")
st.divider()

# Menú lateral para los filtros
st.sidebar.header("🔍 Opciones de Búsqueda")
opcion_busqueda = st.sidebar.radio(
    "¿Cómo deseas buscar?",
    ("Por Año", "Por Director")
)

# Lógica de filtrado basada en la selección
if opcion_busqueda == "Por Año":
    # Obtener lista de años únicos ordenados de mayor a menor
    lista_anos = sorted(df["Año"].unique(), reverse=True)
    ano_seleccionado = st.sidebar.selectbox("Selecciona un Año:", lista_anos)
    
    # Filtrar el DataFrame
    resultados = df[df["Año"] == ano_seleccionado]
    criterio_mostrado = f"el año {ano_seleccionado}"

elif opcion_busqueda == "Por Director":
    # Obtener lista de directores únicos ordenados alfabéticamente
    lista_directores = sorted(df["Director"].unique())
    director_seleccionado = st.sidebar.selectbox("Selecciona un Director:", lista_directores)
    
    # Filtrar el DataFrame
    resultados = df[df["Director"] == director_seleccionado]
    criterio_mostrado = f"el director {director_seleccionado}"

# Ordenar los resultados por calificación de mayor a menor
resultados_ordenados = resultados.sort_values(by="Calificación", ascending=False)

# --- MOSTRAR RESULTADOS ---

st.subheader(f"Resultados para {criterio_mostrado}")

# Verificar si hay resultados
if not resultados_ordenados.empty:
    # Mostrar métricas rápidas
    col1, col2 = st.columns(2)
    col1.metric("Películas encontradas", len(resultados_ordenados))
    col2.metric("Calificación promedio", round(resultados_ordenados["Calificación"].mean(), 2))
    
    # Mostrar la tabla de datos
    st.dataframe(
        resultados_ordenados,
        use_container_width=True,
        hide_index=True # Oculta el número de fila para una vista más limpia
    )
else:
    st.info("No se encontraron películas para los criterios seleccionados.")

# Nota al pie
st.markdown("---")
st.caption("Desarrollado con ❤️ usando Streamlit y Pandas.")