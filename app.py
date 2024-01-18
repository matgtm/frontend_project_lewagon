import streamlit as st
from PIL import Image
import requests
# from python-dotenv import load_dotenv
import os


# Set page tab display
st.set_page_config(
   page_title="PCB Defect Detection",
   page_icon= '🖼️',
   layout="wide",
   initial_sidebar_state="expanded",
)

# Example local Docker container URL
# url = 'http://api:8000'
# Example localhost development URL
#url = 'http://127.0.0.1:8000'
# load_dotenv()
#url = os.getenv('API_URL')

## Selecionar url de google cada uno (Diego, Mateo, Matias)
#url = 'https://docker-test-pcb-cfiqqvqtva-uc.a.run.app' #MATIAS: Imagen sin conf thres customizable
url = 'https://docker-test-pcb-cfiqqvqtva-uw.a.run.app'  #MATIAS con conf thres
#url = ''   #MATEO
#url = ''   #DIEGO

# Define the local CSS file location or the URL to the image
header_image = "https://lirp.cdn-website.com/a0bf26f7/dms3rep/multi/opt/shutterstock_1588316845-1920w.jpg"

# # Display the header image full-width
# st.image(header_image, use_column_width=True)

# # Add the title within the header section
# st.markdown(
#     f"<h1 style='text-align: center; color: #fff;'>{'Detección de defectos en tarjetas PCB'}</h1>",
#     unsafe_allow_html=True,
# )


# # Use Markdown to render your header HTML with the styles defined above
# st.markdown("""
# <div class="header" style=background-image=url("https://lirp.cdn-website.com/a0bf26f7/dms3rep/multi/opt/shutterstock_1588316845-1920w.jpg")>
#     <h1>Detección de defectos en tarjetas PCB</h1>
# </div>
# """, unsafe_allow_html=True)


# header_html = """
# h1 {
#     color: red;
# }
# .stApp {
#     background-image: url(https://lirp.cdn-website.com/a0bf26f7/dms3rep/multi/opt/shutterstock_1588316845-1920w.jpg);
#     background-size: 100% auto;
#     background: rgba(0, 0, 0, 0.2);
# }
# """

header_html = """
<style>
    .header {
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), url("https://lirp.cdn-website.com/a0bf26f7/dms3rep/multi/opt/shutterstock_1588316845-1920w.jpg");

        background-size: cover;
        background-position: center;
        height: 400px;
        position: relative;
        color: white;
        text-align: center;
    }

    .header::after {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        opacity: 0.6;
        background: rgba(0, 0, 0, 0.8); /* Black background with opacity */
        z-index: -1;
    }

    .header h1, .header p {
        position: relative;
        z-index: 1;
    }

    /* Streamlit container adjustments */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 0;
    }
</style>

<div class="header">
    <div style="padding: 190px 0;">
        <h1>Detección de defectos en tarjetas PCB</h1>
    </div>
    <div class="overlay"></div>
</div>
"""
# Inject CSS with Markdown
st.markdown(header_html, unsafe_allow_html=True)


# st.header('Detección de defectos en tarjetas PCB')





with st.container():



    st.subheader('Umbral de confianza')

    conf = st.slider('Seleccionar confianza del modelo: ',min_value=0.10,max_value=1.00,step=0.05,value=0.25)

    st.write('El modelo solo identificará aquellos defectos para los que tenga al menos un ',conf*100,'% de seguridad en sus predicciones.')

    ### Create a native Streamlit file upload input
    st.markdown("### Cargar la foto de la tarjeta")
    img_file_buffer = st.file_uploader('Cargar una imagen')

    if img_file_buffer is not None:




        ### Display the image user uploaded
        st.image(Image.open(img_file_buffer), caption="Here's the image you uploaded ☝️")


        with st.spinner("Wait for it..."):
            ### Get bytes from the file buffer
            img_bytes = img_file_buffer.getvalue()

            ### Make request to  API (stream=True to stream response as bytes)
            res = requests.post(url + "/upload_image", files={'img': img_bytes},params={'conf':conf})

            if res.status_code == 200:
                ### Display the image returned by the API
                st.image(res.content, caption="Imagen devuelta por API ☝️")
            else:
                st.markdown("**Oops**, something went wrong 😓 Please try again.")
                print(res.status_code, res.content)
