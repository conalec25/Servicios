import streamlit as st
import msal
import requests

# Configuración de la app registrada en Azure
CLIENT_ID = "c7b3c371-5474-4109-b266-be0e263848fd"
TENANT_ID = "2309395f-0c25-43ae-b51c-6d8572989c5a"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = "http://localhost"  # Cambiar por la URL de producción si estás en Streamlit Cloud
SCOPE = ["https://graph.microsoft.com/.default", "User.Read", "Sites.Read.All"]

st.set_page_config(page_title="Login Microsoft", page_icon="🔐")
st.title("🔐 Ingreso con cuenta Microsoft 365")

# Crear instancia de MSAL
session = msal.PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)

if "token_result" not in st.session_state:
    st.session_state["token_result"] = None

# Botón de inicio de sesión
if st.button("Iniciar sesión con Microsoft"):
    try:
        # Lanzar el navegador para iniciar sesión
        result = session.acquire_token_interactive(scopes=SCOPE, redirect_uri=REDIRECT_URI)
        st.session_state["token_result"] = result
    except Exception as e:
        st.error(f"Error en inicio de sesión: {e}")

# Mostrar resultado si se autenticó correctamente
if st.session_state["token_result"]:
    token_data = st.session_state["token_result"]
    st.success("✅ Autenticado con éxito.")
    st.code(token_data["access_token"][:200] + "...", language="text")

    # Intentar acceder al perfil del usuario
    headers = {
        "Authorization": f"Bearer {token_data['access_token']}"
    }
    graph_response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
    if graph_response.ok:
        user_info = graph_response.json()
        st.write("👤 Usuario autenticado:")
        st.json(user_info)
    else:
        st.warning("No se pudo obtener el perfil del usuario.")
