import streamlit as st


def show_footer():

    st.markdown("---")

    st.markdown(
        """
        <div style='text-align:center;color:gray;padding:15px;'>

        <b>FoodAI v1.0</b><br>

        Built with TensorFlow • EfficientNetB0 • Streamlit

        </div>
        """,
        unsafe_allow_html=True
    )