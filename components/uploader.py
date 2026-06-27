import streamlit as st
from PIL import Image


def image_uploader():

    st.markdown("## 📤 Upload Food Image")

    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"]
    )

    image = None

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            use_container_width=True
        )

    return image