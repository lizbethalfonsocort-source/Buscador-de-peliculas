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
st.markdown("Esta es la guia de bolsillo para los cinefilos. Encuentra las mejores películas filtrando por **Año** o por **Director**. Los resultados se mostrarán ordenados por su calificación.")
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
    # Cambiamos selectbox por multiselect para permitir múltiples selecciones
    anos_seleccionados = st.sidebar.multiselect(
        "Selecciona uno o más Años:", 
        lista_anos, 
        default=[1994, 2008] # Valores por defecto para mostrar algo al inicio
    )
    
    # Filtrar el DataFrame
    if anos_seleccionados:
        resultados = df[df["Año"].isin(anos_seleccionados)]
        criterio_mostrado = "los años seleccionados"
    else:
        # Si no hay ninguno seleccionado, mostramos todas las películas
        resultados = df 
        criterio_mostrado = "todos los años (sin filtro)"

elif opcion_busqueda == "Por Director":
    # Obtener lista de directores únicos ordenados alfabéticamente
    lista_directores = sorted(df["Director"].unique())
    # Cambiamos selectbox por multiselect
    directores_seleccionados = st.sidebar.multiselect(
        "Selecciona uno o más Directores:", 
        lista_directores, 
        default=["Christopher Nolan", "Martin Scorsese"]
    )
    
    # Filtrar el DataFrame
    if directores_seleccionados:
        resultados = df[df["Director"].isin(directores_seleccionados)]
        criterio_mostrado = "los directores seleccionados"
    else:
        # Si no hay ninguno seleccionado, mostramos todas las películas
        resultados = df
        criterio_mostrado = "todos los directores (sin filtro)"

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
    
    # Definir CSS para el estilo artístico de las imágenes
    estilo_css = """
    <style>
    .afiche-artistico {
        width: 100%;
        border-radius: 10px;
        box-shadow: 8px 8px 15px rgba(0, 0, 0, 0.4);
        filter: sepia(50%) contrast(1.2) brightness(0.9);
        border: 3px solid #f0f2f6;
        transition: all 0.4s ease;
    }
    .afiche-artistico:hover {
        transform: scale(1.05) rotate(2deg);
        filter: sepia(0%) contrast(1.1) brightness(1.0);
        box-shadow: 12px 12px 20px rgba(0, 0, 0, 0.6);
        z-index: 10;
    }
    </style>
    """
    st.markdown(estilo_css, unsafe_allow_html=True)
    
    # Mostrar cada película con su afiche y datos en una disposición limpia
    for _, fila in resultados_ordenados.iterrows():
        # Crear columnas para el diseño: una pequeña para la imagen, otra más grande para los datos
        col_img, col_datos = st.columns([1, 4]) 
        
        with col_img:
            # Mostrar la imagen usando HTML personalizado para aplicar el CSS artístico
            st.markdown(f'<img class="afiche-artistico" src="{fila["URL_Afiche"]}" alt="Afiche de {fila["Título"]}">', unsafe_allow_html=True)
            
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
