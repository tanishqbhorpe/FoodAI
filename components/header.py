import streamlit as st
from pathlib import Path

ASSETS = Path(__file__).parent.parent / "assets"
LOGO_PATH = ASSETS / "logo.png"


def show_header():

    st.markdown(
        """
        <div style="text-align:center;">
        """,
        unsafe_allow_html=True
    )

    _, center, _ = st.columns([3, 2, 3])

    with center:
        st.image(str(LOGO_PATH), use_container_width=True)

    st.markdown(
        """
        <p style="
            text-align:center;
            font-size:20px;
            color:#9CA3AF;
            margin-top:10px;
            margin-bottom:25px;
            font-weight:500;">
            AI Powered Food Recognition & Calorie Estimator
        </p>
        """,
        unsafe_allow_html=True
    )