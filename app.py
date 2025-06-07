import streamlit as st
import msal
import requests

# Configuración de la app registrada
CLIENT_ID = "c7b3c371-5474-4109-b266-be0e263848fd"
TENANT_ID = "2309395f-0c25-43ae-b51c-6d8572989c5a"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read", "Sites.Read.All"]

st.set_page_config(page_title="Login Microsoft Device Flow", page_icon="🔐")
st.title("🔐 Acceso con cuenta Microsoft (Device Flow)")

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if st.button("Iniciar sesión con Microsoft"):
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    flow = app.initiate_device_flow(scopes=SCOPE)

    if "user_code" in flow:
        st.info("🔗 Ve a [https://microsoft.com/devicelogin](https://microsoft.com/devicelogin) e ingresa este código:")
        st.code(flow["user_code"], language="text")
        st.write("Esperando autenticación...")

        result = app.acquire_token_by_device_flow(flow)

        if "access_token" in result:
            st.success("✅ Sesión iniciada correctamente")
            st.session_state.access_token = result["access_token"]
        else:
            st.error("❌ Error al obtener el token.")
    else:
        st.error("No se pudo iniciar el flujo de dispositivo.")

# Mostrar perfil si autenticado
if st.session_state.access_token:
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
    if response.status_code == 200:
        user = response.json()
        st.markdown("### 👤 Usuario autenticado:")
        st.json(user)
    else:
        st.warning("No se pudo obtener el perfil del usuario.")
