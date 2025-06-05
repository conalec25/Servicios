import streamlit as st
import pandas as pd
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext

# Configuración de la app registrada en Azure
site_url = "https://netorgft16679613.sharepoint.com/sites/Facturacion"
client_id = "cea2887b-233f-4485-806e-a1ad688680b2"
client_secret = "HSt8Q~R-dGcayNSsNdqOkN4azw6i1sqBRGu.ZcH-"
tenant_id = "2309395f-0c25-4a3e-b51c-6d8572989c5a"
list_name = "RegUsuarios"
columna_correo = "UsuarioCorreo"

# Función para conectar a SharePoint y traer usuarios
@st.cache_data(ttl=600)
def obtener_usuarios_sharepoint():
    cred = ClientCredential(client_id, client_secret)
    ctx = ClientContext(site_url).with_credentials(cred)
    lista = ctx.web.lists.get_by_title(list_name)
    items = lista.items.top(200).get().execute_query()
    registros = [item.properties for item in items]
    df = pd.DataFrame(registros)
    df[columna_correo] = df[columna_correo].str.strip().str.lower()
    return df

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
