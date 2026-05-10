import streamlit as st
import pandas as pd

# Configuración inicial de la página
st.set_page_config(
    page_title="Buscador de Películas",
    page_icon="🎬",
    layout="wide"
)

# --- CARGA DE DATOS SIMULADOS ---

@st.cache_data
def cargar_datos():
    # Base de datos simulada con películas clásicas y recientes
    datos = {
        "Título": [
            "Cadena Perpetua", "El Padrino", "El Caballero Oscuro", 
            "12 Hombres sin Piedad", "El Señor de los Anillos: El Retorno del Rey", 
            "Pulp Fiction", "Forrest Gump", "Matrix", "Origen", 
            "Interstellar", "Parásitos", "El lobo de Wall Street", 
            "Oppenheimer", "Dune: Parte Dos", "Spider-Man: Cruzando el Multiverso",
            "Top Gun: Maverick", "La Sociedad de la Nieve", "Todo a la vez en todas partes",
            "Furiosa: De la saga Mad Max", "Intensa Mente 2", "Pobres Criaturas"
        ],
        "Año": [
            1994, 1972, 2008, 
            1957, 2003, 
            1994, 1994, 1999, 2010, 
            2014, 2019, 2013, 
            2023, 2024, 2023,
            2022, 2023, 2022,
            2024, 2024, 2023
        ],
        "Director": [
            "Frank Darabont", "Francis Ford Coppola", "Christopher Nolan",
            "Sidney Lumet", "Peter Jackson",
            "Quentin Tarantino", "Robert Zemeckis", "Lana Wachowski, Lilly Wachowski", "Christopher Nolan",
            "Christopher Nolan", "Bong Joon Ho", "Martin Scorsese",
            "Christopher Nolan", "Denis Villeneuve", "Joaquim Dos Santos",
            "Joseph Kosinski", "J.A. Bayona", "Daniel Kwan, Daniel Scheinert",
            "George Miller", "Kelsey Mann", "Yorgos Lanthimos"
        ],
        "Calificación": [
            9.3, 9.2, 9.0, 
            9.0, 9.0, 
            8.9, 8.8, 8.7, 8.8, 
            8.6, 8.5, 8.2, 
            8.4, 8.6, 8.6,
            8.3, 7.9, 7.8,
            7.9, 8.0, 8.0
        ],
        "Género": [
            "Drama", "Crimen/Drama", "Acción/Crimen",
            "Drama", "Aventura/Fantasía",
            "Crimen/Drama", "Drama/Romance", "Ciencia Ficción/Acción", "Ciencia Ficción/Acción",
            "Ciencia Ficción/Drama", "Thriller/Comedia", "Biografía/Comedia",
            "Biografía/Drama", "Ciencia Ficción/Aventura", "Animación/Acción",
            "Acción/Drama", "Supervivencia/Drama", "Ciencia Ficción/Aventura",
            "Acción/Aventura", "Animación/Aventura", "Comedia/Drama"
        ],
        "URL_Afiche": [
            "https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_vhs.jpg",
            "https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg",
            "https://upload.wikimedia.org/wikipedia/en/9/91/12_angry_men.jpg",
            "https://upload.wikimedia.org/wikipedia/en/b/be/The_Lord_of_the_Rings_-_The_Return_of_the_King_%282003%29.jpg",
            "https://upload.wikimedia.org/wikipedia/en/3/3b/Pulp_Fiction_%281994%29_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/2/2e/Inception_%282010%29_theatrical_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/5/53/Parasite_%282019_film%29.png",
            "https://upload.wikimedia.org/wikipedia/en/d/d8/The_Wolf_of_Wall_Street_%282013%29.png",
            "https://upload.wikimedia.org/wikipedia/en/4/4a/Oppenheimer_%28film%29.jpg",
            "https://upload.wikimedia.org/wikipedia/en/5/52/Dune_Part_Two_poster.jpeg",
            "https://upload.wikimedia.org/wikipedia/en/b/b4/Spider-Man-_Across_the_Spider-Verse_poster.jpeg",
            "https://upload.wikimedia.org/wikipedia/en/1/13/Top_Gun_Maverick_Poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/9/91/Society_of_the_Snow_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/1/1e/Everything_Everywhere_All_at_Once.jpg",
            "https://upload.wikimedia.org/wikipedia/en/6/6c/Furiosa_A_Mad_Max_Saga_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/f/f7/Inside_Out_2_poster.jpg",
            "https://upload.wikimedia.org/wikipedia/en/b/b5/Poor_Things_poster.jpg"
        ]
    }
    return pd.DataFrame(datos)

# Cargar los datos en el DataFrame
df = cargar_datos()

# --- INTERFAZ DE USUARIO ---

st.title("🎬 Buscador de Películas Mejor Calificadas")
st.markdown("**¡Guía de bolsillo para Cinéfilos!**. Encuentra las mejores películas filtrando por **Año** o por **Director**. Los resultados se mostrarán ordenados por su calificación y la vista se adapta a tu pantalla.")
st.divider()

# --- CONTROLES DE BÚSQUEDA CENTRALES ---
st.subheader("🔍 Opciones de Búsqueda")

# Usamos columnas para darle un mejor aspecto al buscador en el centro
col_radio, col_filtro = st.columns([1, 3])

with col_radio:
    opcion_busqueda = st.radio(
        "¿Cómo deseas buscar?",
        ("Por Año", "Por Director")
    )

with col_filtro:
    # Lógica de filtrado basada en la selección (sin selecciones por defecto)
    if opcion_busqueda == "Por Año":
        # Obtener lista de años únicos ordenados de mayor a menor
        lista_anos = sorted(df["Año"].dropna().unique(), reverse=True)
        
        anos_seleccionados = st.multiselect(
            "Selecciona uno o más Años:", 
            lista_anos, 
            default=[] # Ningún año seleccionado al iniciar
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
        lista_directores = sorted(df["Director"].dropna().astype(str).unique())
        
        directores_seleccionados = st.multiselect(
            "Selecciona uno o más Directores:", 
            lista_directores, 
            default=[] # Ningún director seleccionado al iniciar
        )
        
        # Filtrar el DataFrame
        if directores_seleccionados:
            resultados = df[df["Director"].isin(directores_seleccionados)]
            criterio_mostrado = "los directores seleccionados"
        else:
            resultados = df
            criterio_mostrado = "todos los directores (sin filtro)"

st.divider()

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
    
    # CSS con Media Queries para un diseño moderno, limpio y serio
    estilo_css = """
    <style>
    .contenedor-afiche {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }
    .afiche-moderno {
        width: 100%;
        max-width: 260px;
        border-radius: 12px; /* Bordes redondeados suaves, muy profesional */
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15); /* Sombra difuminada y elegante */
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    }
    .afiche-moderno:hover {
        transform: translateY(-8px); /* Efecto de elevación sutil (flotar) */
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.20); /* Sombra más profunda al flotar */
        z-index: 10;
    }
    
    .contenedor-datos {
        padding: 10px 20px;
    }
    
    /* Reglas para pantallas de teléfonos móviles */
    @media (max-width: 768px) {
        .afiche-moderno {
            max-width: 200px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
            margin-bottom: 15px;
        }
        .afiche-moderno:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
        }
        .contenedor-datos {
            text-align: center;
            padding: 0;
        }
    }
    </style>
    """
    st.markdown(estilo_css, unsafe_allow_html=True)
    
    # Mostrar cada película con su afiche y datos
    for _, fila in resultados_ordenados.iterrows():
        col_img, col_datos = st.columns([1, 4]) 
        
        with col_img:
            st.markdown(f'''
                <div class="contenedor-afiche">
                    <img class="afiche-moderno" src="{fila["URL_Afiche"]}" alt="Afiche de {fila["Título"]}">
                </div>
            ''', unsafe_allow_html=True)
            
        with col_datos:
            st.markdown(f'''
                <div class="contenedor-datos">
                    <h3 style="margin-top: 0; font-weight: 600;">{fila["Título"]}</h3>
                    <p style="color: #555; font-size: 1.05rem;">
                        <strong>Año:</strong> {int(fila['Año'])}<br>
                        <strong>Director:</strong> {fila['Director']}<br>
                        <strong>Calificación:</strong> ⭐ {fila['Calificación']}<br>
                        <strong>Género:</strong> {fila['Género']}
                    </p>
                </div>
            ''', unsafe_allow_html=True)
            
        st.write("---") 
else:
    st.info("No se encontraron películas para los criterios seleccionados.")

# Nota al pie
st.markdown("---")
st.caption("Desarrollado por Lizcort asístido con IA.")
