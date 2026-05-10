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
    # Base de datos simulada ampliada (incluye películas hasta la actualidad)
    datos = {
        "Título": [
            "Cadena Perpetua", "El Padrino", "El Padrino 2", "El Caballero Oscuro", 
            "12 Hombres sin Piedad", "La Lista de Schindler", "El Señor de los Anillos: El Retorno del Rey", 
            "Pulp Fiction", "El Bueno, el Feo y el Malo", "Forrest Gump",
            "Matrix", "Origen", "El Señor de los Anillos: La Comunidad del Anillo", 
            "Star Wars: Episodio V", "Interstellar", "Parásitos",
            "Uno de los nuestros", "El lobo de Wall Street", "Seven",
            "Oppenheimer", "Dune: Parte Dos", "Spider-Man: Cruzando el Multiverso",
            "Top Gun: Maverick", "La Sociedad de la Nieve", "Todo a la vez en todas partes"
        ],
        "Año": [
            1994, 1972, 1974, 2008, 
            1957, 1993, 2003, 
            1994, 1966, 1994,
            1999, 2010, 2001, 
            1980, 2014, 2019,
            1990, 2013, 1995,
            2023, 2024, 2023,
            2022, 2023, 2022
        ],
        "Director": [
            "Frank Darabont", "Francis Ford Coppola", "Francis Ford Coppola", "Christopher Nolan",
            "Sidney Lumet", "Steven Spielberg", "Peter Jackson",
            "Quentin Tarantino", "Sergio Leone", "Robert Zemeckis",
            "Lana Wachowski, Lilly Wachowski", "Christopher Nolan", "Peter Jackson",
            "Irvin Kershner", "Christopher Nolan", "Bong Joon Ho",
            "Martin Scorsese", "Martin Scorsese", "David Fincher",
            "Christopher Nolan", "Denis Villeneuve", "Joaquim Dos Santos",
            "Joseph Kosinski", "J.A. Bayona", "Daniel Kwan, Daniel Scheinert"
        ],
        "Calificación": [
            9.3, 9.2, 9.0, 9.0, 
            9.0, 9.0, 9.0, 
            8.9, 8.8, 8.8,
            8.7, 8.8, 8.8, 
            8.7, 8.6, 8.5,
            8.7, 8.2, 8.6,
            8.4, 8.6, 8.6,
            8.3, 7.9, 7.8
        ],
        "Género": [
            "Drama", "Crimen/Drama", "Crimen/Drama", "Acción/Crimen",
            "Drama", "Biografía/Drama", "Aventura/Fantasía",
            "Crimen/Drama", "Western", "Drama/Romance",
            "Ciencia Ficción/Acción", "Ciencia Ficción/Acción", "Aventura/Fantasía",
            "Ciencia Ficción/Aventura", "Ciencia Ficción/Drama", "Thriller/Comedia",
            "Crimen/Drama", "Biografía/Comedia", "Crimen/Misterio",
            "Biografía/Drama", "Ciencia Ficción/Aventura", "Animación/Acción",
            "Acción/Drama", "Supervivencia/Drama", "Ciencia Ficción/Aventura"
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
            "https://upload.wikimedia.org/wikipedia/en/6/68/Seven_%28movie%29_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/4/4a/Oppenheimer_%28film%29.jpg",
            "https://upload.wikimedia.org/wikipedia/en/5/52/Dune_Part_Two_poster.jpeg",
            "https://upload.wikimedia.org/wikipedia/en/b/b4/Spider-Man-_Across_the_Spider-Verse_poster.jpeg",
            "https://upload.wikimedia.org/wikipedia/en/1/13/Top_Gun_Maverick_Poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/9/91/Society_of_the_Snow_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/1/1e/Everything_Everywhere_All_at_Once.jpg"
        ]
    }
    return pd.DataFrame(datos)

# Cargar los datos en un DataFrame de pandas
df = cargar_datos()

# --- INTERFAZ DE USUARIO ---

st.title("🎬 Buscador de Películas Mejor Calificadas")
st.markdown("¡Guia de bolsillo para Cinefilos! Encuentra las mejores películas filtrando por **Año** o por **Director**. Los resultados se mostrarán ordenados por su calificación y la vista se adapta a tu pantalla.")
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
    
    anos_seleccionados = st.sidebar.multiselect(
        "Selecciona uno o más Años:", 
        lista_anos, 
        default=[lista_anos[0], 2023, 1994] # Muestra el año más reciente por defecto junto con otros
    )
    
    # Filtrar el DataFrame
    if anos_seleccionados:
        resultados = df[df["Año"].isin(anos_seleccionados)]
        criterio_mostrado = "los años seleccionados"
    else:
        resultados = df 
        criterio_mostrado = "todos los años (sin filtro)"

elif opcion_busqueda == "Por Director":
    # Obtener lista de directores únicos ordenados alfabéticamente
    lista_directores = sorted(df["Director"].unique())
    
    directores_seleccionados = st.sidebar.multiselect(
        "Selecciona uno o más Directores:", 
        lista_directores, 
        default=["Christopher Nolan", "Denis Villeneuve"]
    )
    
    # Filtrar el DataFrame
    if directores_seleccionados:
        resultados = df[df["Director"].isin(directores_seleccionados)]
        criterio_mostrado = "los directores seleccionados"
    else:
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
    
    # CSS con Media Queries para hacer la app totalmente responsiva (Mobile-Friendly)
    estilo_css = """
    <style>
    .contenedor-afiche {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .afiche-artistico {
        width: 100%;
        max-width: 280px;
        border: 4px solid #000000; /* Borde negro grueso tipo cómic */
        border-radius: 0px; /* Bordes cuadrados */
        box-shadow: 12px 12px 0px #ff007f; /* Sombra sólida rosa neón típica del Pop Art */
        filter: contrast(160%) saturate(250%); /* Colores súper saturados y alto contraste */
        transition: all 0.3s ease-in-out;
    }
    .afiche-artistico:hover {
        transform: translate(-5px, -5px); /* Movimiento diagonal */
        box-shadow: 17px 17px 0px #00e5ff; /* La sombra cambia a cian neón al pasar el cursor */
        filter: contrast(180%) saturate(300%) hue-rotate(15deg); /* Los colores vibran y cambian ligeramente */
        z-index: 10;
    }
    
    /* Reglas para pantallas de teléfonos móviles */
    @media (max-width: 768px) {
        .afiche-artistico {
            max-width: 200px; /* Hace la imagen más pequeña en celulares */
            box-shadow: 8px 8px 0px #ff007f; /* Sombras adaptadas a móvil */
            margin-bottom: 15px; /* Da espacio entre la imagen y el texto */
        }
        .afiche-artistico:hover {
            box-shadow: 12px 12px 0px #00e5ff;
        }
        .contenedor-datos {
            text-align: center; /* Centra el texto en móviles */
        }
    }
    </style>
    """
    st.markdown(estilo_css, unsafe_allow_html=True)
    
    # Mostrar cada película con su afiche y datos
    for _, fila in resultados_ordenados.iterrows():
        # Streamlit apila estas columnas automáticamente en pantallas pequeñas
        col_img, col_datos = st.columns([1, 4]) 
        
        with col_img:
            # Envolvemos la imagen en un div para controlar su centrado responsivo
            st.markdown(f'''
                <div class="contenedor-afiche">
                    <img class="afiche-artistico" src="{fila["URL_Afiche"]}" alt="Afiche de {fila["Título"]}">
                </div>
            ''', unsafe_allow_html=True)
            
        with col_datos:
            # Usamos un contenedor para poder aplicar alineación de texto en móviles
            st.markdown(f'''
                <div class="contenedor-datos">
                    <h3>{fila["Título"]}</h3>
                    <p><strong>Año:</strong> {fila['Año']}<br>
                    <strong>Director:</strong> {fila['Director']}<br>
                    <strong>Calificación:</strong> ⭐ {fila['Calificación']}<br>
                    <strong>Género:</strong> {fila['Género']}</p>
                </div>
            ''', unsafe_allow_html=True)
            
        st.write("---") # Separador visual entre películas
else:
    st.info("No se encontraron películas para los criterios seleccionados.")

# Nota al pie
st.markdown("---")
st.caption("Desarrollado por Lizbeth Alfonso asistido con IA. Optimizado para web y móvil.")
