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
            "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
            "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg",
            "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            "https://image.tmdb.org/t/p/w500/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg",
            "https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5OUcvAWM.jpg",
            "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
            "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
            "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
            "https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg",
            "https://image.tmdb.org/t/p/w500/gEU2QlsUUHXjNpeVD8kU5N0U820.jpg",
            "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
            "https://image.tmdb.org/t/p/w500/jTL2EaL10p7pEaX1X1PIfA2qV5A.jpg",
            "https://image.tmdb.org/t/p/w500/ptpr0kGAckfQkJeJVNfau8S3jfl.jpg",
            "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2JGjjc91p.jpg",
            "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg",
            "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg",
            "https://image.tmdb.org/t/p/w500/7zB1E4o56J11x6r9y0r0lqE4q8T.jpg",
            "https://image.tmdb.org/t/p/w500/w3LxiVYdWWRvEVdn5RYq6jIqkb1.jpg",
            "https://image.tmdb.org/t/p/w500/iADOJ8Zymht2JPMoy3R7xceZprc.jpg",
            "https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzRxAcDseS1.jpg",
            "https://image.tmdb.org/t/p/w500/kCGlIMHnOm8PhwovC18j9k6M2vK.jpg"
        ]
    }
    return pd.DataFrame(datos)

# Cargar los datos en el DataFrame
df = cargar_datos()

# --- INTERFAZ DE USUARIO ---

st.title("🎬 Buscador de Películas Mejor Calificadas")
st.markdown("**¡Guía de bolsillo para cinéfilos!** Encuentra las mejores películas filtrando por **Año** o por **Director**. Los resultados se mostrarán ordenados por su calificación.")
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

# Variable para identificar si el usuario ya hizo una búsqueda
hay_seleccion = False

with col_filtro:
    # Lógica de filtrado basada en la selección (sin selecciones por defecto y mostrando vacío inicialmente)
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
            hay_seleccion = True
        else:
            resultados = pd.DataFrame(columns=df.columns) # DataFrame vacío
            criterio_mostrado = "esperando tu búsqueda..."
    
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
            hay_seleccion = True
        else:
            resultados = pd.DataFrame(columns=df.columns) # DataFrame vacío
            criterio_mostrado = "esperando tu búsqueda..."

st.divider()

# Ordenar los resultados por calificación de mayor a menor
resultados_ordenados = resultados.sort_values(by="Calificación", ascending=False)

# --- MOSTRAR RESULTADOS ---

st.subheader(f"Resultados para {criterio_mostrado}")

# Verificar si hay resultados o si apenas entramos a la app
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
    # Mensajes amigables dependiendo de si no se ha buscado o si no se encontró nada
    if not hay_seleccion:
        st.info("👆 Por favor, selecciona un Año o un Director en el buscador de arriba para comenzar a ver las películas.")
    else:
        st.warning("No se encontraron películas para los criterios seleccionados.")

# Nota al pie
st.markdown("---")
st.caption("Desarrollado por Lizcort asistido con IA.")
