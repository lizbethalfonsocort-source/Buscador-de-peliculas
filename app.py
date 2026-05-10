import streamlit as st
import pandas as pd
import urllib.parse

# Función para crear un póster garantizado que no depende de internet (SVG en Data URI)
def generar_afiche_seguro(titulo):
    # Limita la longitud del título para que no desborde en el dibujo
    titulo_corto = titulo[:25] + "..." if len(titulo) > 25 else titulo
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="300" height="450" viewBox="0 0 300 450">
        <rect width="100%" height="100%" fill="#1f1f2e"/>
        <text x="50%" y="45%" dominant-baseline="middle" text-anchor="middle" fill="#ffffff" font-family="Arial, sans-serif" font-size="22" font-weight="bold">{titulo_corto}</text>
        <text x="50%" y="60%" dominant-baseline="middle" text-anchor="middle" font-size="50">🎬</text>
    </svg>
    """
    # Convierte el dibujo en una URL incrustable que nunca falla
    return "data:image/svg+xml;charset=utf-8," + urllib.parse.quote(svg)

# Configuración inicial de la página
st.set_page_config(
    page_title="Buscador de Películas",
    page_icon="🎬",
    layout="wide"
)

# --- CARGA DE DATOS SIMULADOS ---

@st.cache_data
def cargar_datos():
    # 1. Lista base de películas con afiches reales de Amazon IMDb confirmados
    peliculas_base = [
        {"Título": "Cadena Perpetua", "Año": 1994, "Director": "Frank Darabont", "Calificación": 9.3, "Género": "Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "El Padrino", "Año": 1972, "Director": "Francis Ford Coppola", "Calificación": 9.2, "Género": "Crimen/Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "El Caballero Oscuro", "Año": 2008, "Director": "Christopher Nolan", "Calificación": 9.0, "Género": "Acción/Crimen", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "12 Hombres sin Piedad", "Año": 1957, "Director": "Sidney Lumet", "Calificación": 9.0, "Género": "Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "El Señor de los Anillos: El Retorno del Rey", "Año": 2003, "Director": "Peter Jackson", "Calificación": 9.0, "Género": "Aventura/Fantasía", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BNzA5ZDNlZWMtM2NhNC00MzgzLWE0MDItMjkzY2M1NzkzMzUhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Pulp Fiction", "Año": 1994, "Director": "Quentin Tarantino", "Calificación": 8.9, "Género": "Crimen/Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTItNDJhNi00MzhkLWEzODQtZjU5NWFlZDZkMTNhXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Forrest Gump", "Año": 1994, "Director": "Robert Zemeckis", "Calificación": 8.8, "Género": "Drama/Romance", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Matrix", "Año": 1999, "Director": "Lana Wachowski, Lilly Wachowski", "Calificación": 8.7, "Género": "Ciencia Ficción/Acción", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Origen", "Año": 2010, "Director": "Christopher Nolan", "Calificación": 8.8, "Género": "Ciencia Ficción/Acción", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Interstellar", "Año": 2014, "Director": "Christopher Nolan", "Calificación": 8.6, "Género": "Ciencia Ficción/Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDItN2IxOS00ZmJlLTgwZTItZ2FkYmI2OGJjYjZmM2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Parásitos", "Año": 2019, "Director": "Bong Joon Ho", "Calificación": 8.5, "Género": "Thriller/Comedia", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "El lobo de Wall Street", "Año": 2013, "Director": "Martin Scorsese", "Calificación": 8.2, "Género": "Biografía/Comedia", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BMjIxMjgxNTk0MF5BMl5BanBnXkFtZTgwNjIyOTg2MDE@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Oppenheimer", "Año": 2023, "Director": "Christopher Nolan", "Calificación": 8.4, "Género": "Biografía/Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjUtN2M1MS00MTQ2LTk2ODktNzc2NDRjZjU0YjhiXkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Dune: Parte Dos", "Año": 2024, "Director": "Denis Villeneuve", "Calificación": 8.6, "Género": "Ciencia Ficción/Aventura", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BN2QyZGU4ZDctOWMzMy00NTc5LThlOGItNjIyZTVhNDM4N2UxXkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Spider-Man: Cruzando el Multiverso", "Año": 2023, "Director": "Joaquim Dos Santos", "Calificación": 8.6, "Género": "Animación/Acción", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BMzI0NmVkMjEtYmY4MS00ZTFjLWE0ZWEtZGUxNmJmMTE1NDkwXkEyXkFqcGdeQXVyMzQ0MzA0NTM@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Top Gun: Maverick", "Año": 2022, "Director": "Joseph Kosinski", "Calificación": 8.3, "Género": "Acción/Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BZWYzOGEwNTgtNWU3NS00ZTQ0LWJkODUtMmVhMjIwMjA1ZmQwXkEyXkFqcGdeQXVyMjkwOTAyMTE@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "La Sociedad de la Nieve", "Año": 2023, "Director": "J.A. Bayona", "Calificación": 7.9, "Género": "Supervivencia/Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BMDk2YzdkMTctYmY1YS00ZWE1LTg5ODAtOTU4MGI4YzM2M2NjXkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Todo a la vez en todas partes", "Año": 2022, "Director": "Daniel Kwan, Daniel Scheinert", "Calificación": 7.8, "Género": "Ciencia Ficción/Aventura", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BYTdiOTIyZTQtNmQ1OS00NjZlLWIyMTgtYzk5Y2M3ZDVmMDk1XkEyXkFqcGdeQXVyMTAzMDg4NzU0._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Furiosa: De la saga Mad Max", "Año": 2024, "Director": "George Miller", "Calificación": 7.9, "Género": "Acción/Aventura", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BZDcwNmMzY2UtMjFlZS00Zjc1LTg4MjEtMjhhY2U2ZWQwOWJkXkEyXkFqcGdeQXVyMDM2NDM2MQ@@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Intensa Mente 2", "Año": 2024, "Director": "Kelsey Mann", "Calificación": 8.0, "Género": "Animación/Aventura", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BYWFmYWE0ZWMtMDQ2NS00NjVhLWE2MDYtOWI2NDk4Nzk1N2M1XkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Pobres Criaturas", "Año": 2023, "Director": "Yorgos Lanthimos", "Calificación": 8.0, "Género": "Comedia/Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BNGIyYWMzNjktNDE3MC00YWQyLWEyMmEtN2ZmNzZhZDk3NGJlXkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Django Desencadenado", "Año": 2012, "Director": "Quentin Tarantino", "Calificación": 8.4, "Género": "Western/Drama", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BMjIyNTQ5NjQ1OV5BMl5BanBnXkFtZTcwODg1MDU4OA@@._V1_FMjpg_UX1000_.jpg"},
        {"Título": "Kill Bill: Volumen 1", "Año": 2003, "Director": "Quentin Tarantino", "Calificación": 8.2, "Género": "Acción/Crimen", "URL_Afiche": "https://m.media-amazon.com/images/M/MV5BNzM3NDFhYTAtYmU5Mi00NGRmLTljYjgtMDkyODQ4MjNkMGY2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg"}
    ]

    # 2. Filmografía completa (sin afiche asignado, se generará dinámicamente)
    filmografias_completas = [
        # === QUENTIN TARANTINO ===
        {"Título": "Reservoir Dogs", "Año": 1992, "Director": "Quentin Tarantino", "Calificación": 8.3, "Género": "Crimen/Suspense"},
        {"Título": "Jackie Brown", "Año": 1997, "Director": "Quentin Tarantino", "Calificación": 7.5, "Género": "Crimen/Drama"},
        {"Título": "Kill Bill: Volumen 2", "Año": 2004, "Director": "Quentin Tarantino", "Calificación": 8.0, "Género": "Acción/Crimen"},
        {"Título": "Death Proof", "Año": 2007, "Director": "Quentin Tarantino", "Calificación": 7.0, "Género": "Acción/Suspense"},
        {"Título": "Malditos Bastardos", "Año": 2009, "Director": "Quentin Tarantino", "Calificación": 8.3, "Género": "Bélico/Acción"},
        {"Título": "Los Odiosos Ocho", "Año": 2015, "Director": "Quentin Tarantino", "Calificación": 7.8, "Género": "Western/Misterio"},
        {"Título": "Érase una vez en Hollywood", "Año": 2019, "Director": "Quentin Tarantino", "Calificación": 7.6, "Género": "Comedia/Drama"},
        
        # === CHRISTOPHER NOLAN ===
        {"Título": "Following", "Año": 1998, "Director": "Christopher Nolan", "Calificación": 7.5, "Género": "Misterio/Crimen"},
        {"Título": "Memento", "Año": 2000, "Director": "Christopher Nolan", "Calificación": 8.4, "Género": "Misterio/Suspense"},
        {"Título": "Insomnia", "Año": 2002, "Director": "Christopher Nolan", "Calificación": 7.2, "Género": "Misterio/Suspense"},
        {"Título": "Batman Begins", "Año": 2005, "Director": "Christopher Nolan", "Calificación": 8.2, "Género": "Acción/Aventura"},
        {"Título": "El Truco Final (El Prestigio)", "Año": 2006, "Director": "Christopher Nolan", "Calificación": 8.5, "Género": "Drama/Misterio"},
        {"Título": "El Caballero Oscuro: La Leyenda Renace", "Año": 2012, "Director": "Christopher Nolan", "Calificación": 8.4, "Género": "Acción/Suspense"},
        {"Título": "Dunkerque", "Año": 2017, "Director": "Christopher Nolan", "Calificación": 7.8, "Género": "Bélico/Acción"},
        {"Título": "Tenet", "Año": 2020, "Director": "Christopher Nolan", "Calificación": 7.3, "Género": "Ciencia Ficción/Acción"},

        # === DENIS VILLENEUVE ===
        {"Título": "Incendies", "Año": 2010, "Director": "Denis Villeneuve", "Calificación": 8.3, "Género": "Drama/Guerra"},
        {"Título": "Prisioneros", "Año": 2013, "Director": "Denis Villeneuve", "Calificación": 8.1, "Género": "Crimen/Drama"},
        {"Título": "Enemy", "Año": 2013, "Director": "Denis Villeneuve", "Calificación": 6.9, "Género": "Misterio/Suspense"},
        {"Título": "Sicario", "Año": 2015, "Director": "Denis Villeneuve", "Calificación": 7.6, "Género": "Acción/Crimen"},
        {"Título": "La Llegada (Arrival)", "Año": 2016, "Director": "Denis Villeneuve", "Calificación": 7.9, "Género": "Ciencia Ficción/Drama"},
        {"Título": "Blade Runner 2049", "Año": 2017, "Director": "Denis Villeneuve", "Calificación": 8.0, "Género": "Ciencia Ficción/Misterio"},
        {"Título": "Dune", "Año": 2021, "Director": "Denis Villeneuve", "Calificación": 8.0, "Género": "Ciencia Ficción/Aventura"},
        
        # === MARTIN SCORSESE ===
        {"Título": "Taxi Driver", "Año": 1976, "Director": "Martin Scorsese", "Calificación": 8.2, "Género": "Crimen/Drama"},
        {"Título": "Toro Salvaje", "Año": 1980, "Director": "Martin Scorsese", "Calificación": 8.1, "Género": "Biografía/Deporte"},
        {"Título": "Uno de los nuestros", "Año": 1990, "Director": "Martin Scorsese", "Calificación": 8.7, "Género": "Crimen/Drama"},
        {"Título": "Casino", "Año": 1995, "Director": "Martin Scorsese", "Calificación": 8.2, "Género": "Crimen/Drama"},
        {"Título": "Infiltrados", "Año": 2006, "Director": "Martin Scorsese", "Calificación": 8.5, "Género": "Crimen/Drama"},
        {"Título": "Shutter Island", "Año": 2010, "Director": "Martin Scorsese", "Calificación": 8.2, "Género": "Misterio/Suspense"},
        {"Título": "El Irlandés", "Año": 2019, "Director": "Martin Scorsese", "Calificación": 7.8, "Género": "Crimen/Drama"},
        {"Título": "Los asesinos de la luna", "Año": 2023, "Director": "Martin Scorsese", "Calificación": 7.6, "Género": "Crimen/Drama"}
    ]

    # Procesar automáticamente imágenes de las películas adicionales usando una imagen generada internamente
    for p in filmografias_completas:
        p["URL_Afiche"] = generar_afiche_seguro(p["Título"])
        
    # Unir ambas listas
    todas_las_peliculas = peliculas_base + filmografias_completas
    return pd.DataFrame(todas_las_peliculas)

# Cargar los datos en el DataFrame
df = cargar_datos()

# --- INTERFAZ DE USUARIO ---

st.title("🎬 Buscador de Películas Mejor Calificadas")
st.markdown("**¡Guía de bolsillo para Cinéfilos!** Encuentra las mejores películas filtrando por **Año** o por **Director** los resultados se mostrarán ordenados por su calificación.")
st.divider(
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
    if opcion_busqueda == "Por Año":
        lista_anos = sorted(df["Año"].dropna().unique(), reverse=True)
        anos_seleccionados = st.multiselect(
            "Selecciona uno o más Años:", 
            lista_anos, 
            default=[] 
        )
        if anos_seleccionados:
            resultados = df[df["Año"].isin(anos_seleccionados)]
            criterio_mostrado = "los años seleccionados"
            hay_seleccion = True
        else:
            resultados = pd.DataFrame(columns=df.columns) 
            criterio_mostrado = "esperando tu búsqueda..."
    
    elif opcion_busqueda == "Por Director":
        lista_directores = sorted(df["Director"].dropna().astype(str).unique())
        directores_seleccionados = st.multiselect(
            "Selecciona uno o más Directores:", 
            lista_directores, 
            default=[] 
        )
        if directores_seleccionados:
            resultados = df[df["Director"].isin(directores_seleccionados)]
            criterio_mostrado = "los directores seleccionados"
            hay_seleccion = True
        else:
            resultados = pd.DataFrame(columns=df.columns) 
            criterio_mostrado = "esperando tu búsqueda..."

st.divider()

resultados_ordenados = resultados.sort_values(by="Año", ascending=False) # Ordenadas por año (más reciente primero) para mejor lectura de filmografía

# --- MOSTRAR RESULTADOS ---

st.subheader(f"Resultados para {criterio_mostrado}")

if not resultados_ordenados.empty:
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
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    }
    .afiche-moderno:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.20);
        z-index: 10;
    }
    .contenedor-datos {
        padding: 10px 20px;
    }
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
        
        # Generar un afiche de respaldo garantizado con el título por si el enlace original se rompe
        afiche_respaldo = generar_afiche_seguro(fila["Título"])
        
        with col_img:
            st.markdown(f'''
                <div class="contenedor-afiche">
                    <img class="afiche-moderno" src="{fila["URL_Afiche"]}" alt="Afiche de {fila["Título"]}" onerror="this.onerror=null; this.src='{afiche_respaldo}';">
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
    if not hay_seleccion:
        st.info("👆 Por favor, selecciona un Año o un Director en el buscador de arriba para comenzar a ver las películas.")
    else:
        st.warning("No se encontraron películas para los criterios seleccionados.")

st.markdown("---")
st.caption("Desarrollado por Lizcort asistido con IA.")
