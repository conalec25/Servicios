import streamlit as st
import pandas as pd
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

# Configuración SharePoint actualizada
site_url = "https://netorgft16679613.sharepoint.com/sites/Facturacion"
client_id = "c7b3c371-5474-4109-b266-be0e263848fd"
client_secret = "HSt8Q~R-dGcayNSsNdqOkN4azw6i1sqBRGu.ZcH-"
list_name = "RegUsuarios"
columna_correo = "UsuarioCorreo"

# Función con manejo de errores
@st.cache_data(ttl=600)
def obtener_usuarios_sharepoint():
    try:
        credentials = ClientCredential(client_id, client_secret)
        ctx = ClientContext(site_url).with_credentials(credentials)
        lista = ctx.web.lists.get_by_title(list_name)
        items = lista.items.top(200).get().execute_query()
        registros = [item.properties for item in items]
        df = pd.DataFrame(registros)
        df[columna_correo] = df[columna_correo].str.strip().str.lower()
        return df
    except Exception as e:
        raise RuntimeError(f"Error accediendo a SharePoint: {e}")

# Interfaz Streamlit
st.set_page_config(page_title="Acceso Servicios CONALEC", page_icon="🔐")
st.title("🔐 Acceso a la plataforma de servicios")

correo_input = st.text_input("Ingresa tu correo institucional", placeholder="usuario@conalec.com")

if st.button("Ingresar"):
    with st.spinner("Verificando acceso en SharePoint..."):
        try:
            usuarios_df = obtener_usuarios_sharepoint()
            correo = correo_input.strip().lower()
            usuario = usuarios_df[
                (usuarios_df[columna_correo] == correo) &
                (usuarios_df["Activo"] == 1)
            ]
            if not usuario.empty:
                nombre = usuario.iloc[0].get("FullName", "Usuario")
                rol = usuario.iloc[0].get("Rol", "Sin rol")
                st.success(f"Bienvenido {nombre} ({rol})")
                st.write("✅ Acceso autorizado.")
            else:
                st.error("⛔ Acceso denegado. Usuario no registrado o inactivo.")
        except Exception as e:
            st.error(f"⚠️ Error al conectar con SharePoint: {e}")
