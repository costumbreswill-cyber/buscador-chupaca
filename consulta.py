import streamlit as st
import pandas as pd
import os

# 1. Configuracion de la pagina
st.set_page_config(page_title="Buscador de Papeletas Chupaca", page_icon="car")

# 2. Titulo y Logo
st.title("Buscador de Papeletas - Chupaca")

# Si tienes un archivo llamado logo.png en tu carpeta, aparecera aqui
if os.path.exists("logo.png"):
    st.image("logo.png", width=150)

st.markdown("Ingrese el numero de placa para consultar infracciones en tiempo real.")

# 3. Funcion para cargar datos desde Google Sheets
@st.cache_data(ttl=600) # Se actualiza cada 10 minutos
def cargar_datos():
    # REEMPLAZA EL LINK DE ABAJO POR EL TUYO DE GOOGLE SHEETS
    google_sheet_url = "https://docs.google.com/spreadsheets/d/1oey-Vd2OJWTRE-wkHidh1oU2d9RHXYDv23QR4Y0b174/edit?usp=sharing"
    
    # Transformamos el link para que sea descargable por Python
    csv_url = google_sheet_url.replace('/edit?usp=sharing', '/export?format=csv')
    
    try:
        # Leemos los datos desde la nube
        df = pd.read_csv(csv_url)
        # Limpiamos espacios en los nombres de columnas
        df.columns = df.columns.str.strip()
        
        if 'Placa' in df.columns:
            df['Placa'] = df['Placa'].astype(str).str.upper().str.strip()
            return df
        else:
            st.error("Error: No se encontro la columna 'Placa' en el Google Sheets.")
            return None
    except Exception as e:
        st.error("Error al conectar con Google Sheets: " + str(e))
        return None

# Ejecutamos la carga de datos
df = cargar_datos()

# 4. Interfaz de Busqueda
if df is not None:
    placa_usuario = st.text_input("Escriba la placa (Ej: W8C-857):").upper().strip()

    if st.button("Consultar"):
        if placa_usuario:
            # Buscamos la placa en la base de datos
            resultado = df[df['Placa'] == placa_usuario]

            if not resultado.empty:
                st.success("Se encontraron " + str(len(resultado)) + " papeleta(s) para esta placa.")
                
                # Mostramos cada infraccion encontrada
                for i, row in resultado.iterrows():
                    with st.expander("Detalle de Papeleta - Fecha: " + str(row.get('Fecha', 'No registra'))):
                        st.write("**Propietario:** " + str(row.get('Propietario', 'No registra')))
                        st.write("**Infraccion:** " + str(row.get('Infraccion', 'No registra')))
                        st.write("**Monto:** S/ " + str(row.get('Monto', '0.00')))
                        st.write("**Estado:** " + str(row.get('Estado', 'Pendiente')))
            else:
                st.warning("No se encontraron papeletas registradas para la placa: " + placa_usuario)
        else:
            st.info("Por favor, ingrese un numero de placa para iniciar la busqueda.")

st.divider()
st.caption("Municipalidad de Chupaca - Sistema de Control de Infracciones")
