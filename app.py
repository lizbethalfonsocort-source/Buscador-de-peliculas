import streamlit as st
import pandas as pd

# --- PARCHE PARA COMPATIBILIDAD CON PYTHON 3.14 ---
import pkgutil
if not hasattr(pkgutil, 'find_loader'):
    import importlib.util
    def find_loader(fullname):
        try:
            spec = importlib.util.find_spec(fullname)
            return spec.loader if spec else None
        except Exception:
            return None
    pkgutil.find_loader = find_loader

from imdb import Cinemagoer

# Configuración inicial de la página
st.set_page_config(
    page_title="Buscador de Películas",
    page_icon="🎬",
    layout="wide"
)

# --- CARGA DE DATOS DESDE IMDb ---

# Usamos cache para que la descarga desde internet solo ocurra la primera vez que se abre la app
@st.cache_data(show_spinner="Descargando datos en vivo desde IMDb... 🍿 (Esto tomará unos segundos)")
def cargar_datos_reales():
    # Definimos las columnas explícitamente para evitar KeyErrors si la lista llega vacía
    columnas = ["Título", "Año", "Director", "Calificación", "Género", "URL_Afiche"]
    datos = []
    
    try:
        ia = Cinemagoer()
        # Obtenemos la lista de las 250 mejores películas y tomamos las primeras 50
        top_movies = ia.get_top250_movies()[:50] 
        
        for movie in top_movies:
            # Obtenemos la información detallada de cada película
            ia.update(movie, info=['main'])
            
            # Extraer directores de forma segura
            directores = [d.get('name') for d in movie.get('directors', [])]
            director_str = ", ".join(directores) if directores else "Desconocido"
            
            # Extraer géneros
            generos = movie.get('genres', [])
            genero_str = "/".join(generos[:2]) if generos else "Desconocido"
            
            # Obtener la URL del afiche
            url_afiche = movie.get('full-size cover url') or movie.get('cover url', 'https://via.placeholder.com/300x450?text=Sin+Afiche')
            
            datos.append({
                "Título": movie.get('title'),
                "Año": movie.get('year'),
                "Director": director_str,
                "Calificación": movie.get('rating'),
                "Género": genero_str,
                "URL_Afiche": url_afiche
            })
    except Exception as e:
        # Si IMDb bloquea la conexión en la nube, evitamos que la app colapse
        print(f"No se pudo conectar con IMDb: {e}")
        pass
        
    # FALLBACK: Si la conexión falló o IMDb bloqueó la IP del servidor en la nube, cargamos datos de respaldo
    if not datos:
        datos = [
            {"Título": "Cadena Perpetua", "Año": 1994, "Director": "Frank Darabont", "Calificación": 9.3, "Género": "Drama", "URL_Afiche": "https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg"},
            {"Título": "El Padrino", "Año": 1972, "Director": "Francis Ford Coppola", "Calificación": 9.2, "Género": "Crimen/Drama", "URL_Afiche": "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_vhs.jpg"},
            {"Título": "El Caballero Oscuro", "Año": 2008, "Director": "Christopher Nolan", "Calificación": 9.0, "Género": "Acción/Crimen", "URL_Afiche": "https://upload.wikimedia.org/wikipedia/en/1/1c/The_Dark_Knight_%282008_film%29.jpg"},
            {"Título": "12 Hombres sin Piedad", "Año": 1957, "Director": "Sidney Lumet", "Calificación": 9.0, "Género": "Drama", "URL_Afiche": "https://upload.wikimedia.org/wikipedia/en/9/91/12_angry_men.jpg"},
            {"Título": "El Señor de los Anillos: El Retorno del Rey", "Año": 2003, "Director": "Peter Jackson", "Calificación": 9.0, "Género": "Aventura/Fantasía", "URL_Afiche": "https://upload.wikimedia.org/wikipedia/en/b/be/The_Lord_of_the_Rings_-_The_Return_of_the_King_%282003%29.jpg"}
        ]
        
    return pd.DataFrame(datos, columns=columnas)

# Cargar los datos reales en el DataFrame
df = cargar_datos_reales()

# --- INTERFAZ DE USUARIO ---

st.title("🎬 Buscador de Películas (Conectado a IMDb)")
st.markdown("**¡Guía de bolsillo para Cinéfilos!**
Encuentra las mejores películas filtrando por **Año** o por **Director**.")
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
    lista_anos = sorted(df["Año"].dropna().unique(), reverse=True)
    
    # Manejar los valores por defecto
    valores_defecto_ano = [lista_anos[0]] if len(lista_anos) > 0 else []
    
    anos_seleccionados = st.sidebar.multiselect(
        "Selecciona uno o más Años:", 
        lista_anos, 
        default=valores_defecto_ano
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
    
    valores_defecto_director = [lista_directores[0]] if len(lista_directores) > 0 else []
    
    directores_seleccionados = st.sidebar.multiselect(
        "Selecciona uno o más Directores:", 
        lista_directores, 
        default=valores_defecto_director
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
    
    # CSS con Media Queries para un diseño moderno, limpio y elegante
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
        border-radius: 16px; /* Bordes redondeados suaves */
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15); /* Sombra difuminada y elegante */
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    }
    .afiche-moderno:hover {
        transform: translateY(-10px) scale(1.02); /* Efecto de elevación (flotar) suave */
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25); /* Sombra más profunda al flotar */
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
            margin-bottom: 20px;
        }
        .afiche-moderno:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
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
st.caption("Desarrollado por Lizcort asistido por IA.")
