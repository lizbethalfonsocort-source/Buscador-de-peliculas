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
        ],
        "URL_Afiche": [
            "https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_vhs.jpg",
            "https://upload.wikimedia.org/wikipedia/en/0/03/Godfather_part_ii.jpg",
            "https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg",
            "https://upload.wikimedia.org/wikipedia/en/9/91/12_angry_men.jpg",
            "https://upload.wikimedia.org/wikipedia/en/3/38/Schindler%27s_List_movie.jpg",
            "https://upload.wikimedia.org/wikipedia/en/b/be/The_Lord_of_the_Rings_-_The_Return_of_the_King_%282003%29.jpg",
            "https://upload.wikimedia.org/wikipedia/en/3/3b/Pulp_Fiction_%281994%29_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/4/45/Good_the_bad_and_the_ugly_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/8/8a/The_Lord_of_the_Rings_The_Fellowship_of_the_Ring_%282001%29.jpg",
            "https://upload.wikimedia.org/wikipedia/en/3/3f/The_Empire_Strikes_Back_%281980_movie_poster%29.jpg",
            "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/5/53/Parasite_%282019_film%29.png",
            "https://upload.wikimedia.org/wikipedia/en/7/7b/Goodfellas.jpg",
            "https://upload.wikimedia.org/wikipedia/en/d/d8/The_Wolf_of_Wall_Street_%282013%29.png",
            "https://upload.wikimedia.org/wikipedia/en/6/68/Seven_%28movie%29_poster.jpg"
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
    
    st.write("---")
    
    # Mostrar cada película con su afiche y datos en una disposición limpia
    for _, fila in resultados_ordenados.iterrows():
        # Crear columnas para el diseño: una pequeña para la imagen, otra más grande para los datos
        col_img, col_datos = st.columns([1, 4]) 
        
        with col_img:
            # Mostrar la imagen
            st.image(fila["URL_Afiche"], use_container_width=True)
            
        with col_datos:
            # Mostrar los datos en texto
            st.subheader(fila["Título"])
            st.write(f"**Año:** {fila['Año']}")
            st.write(f"**Director:** {fila['Director']}")
            st.write(f"**Calificación:** ⭐ {fila['Calificación']}")
            st.write(f"**Género:** {fila['Género']}")
            
        st.write("---") # Separador visual entre películas
else:
    st.info("No se encontraron películas para los criterios seleccionados.")

# Nota al pie
st.markdown("---")
st.caption("Desarrollado por Lizbeth Alfonso asistido con IA.")
