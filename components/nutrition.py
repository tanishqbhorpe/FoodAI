import streamlit as st


def show_nutrition(result):

    if result is None:
        return

    st.markdown("---")

    st.markdown("## 🥗 Nutrition Facts")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Calories",
            f"{result['calories']} kcal"
        )

        st.metric(
            "Serving",
            result["serving"]
        )

    with col2:

        st.metric(
            "AI Model",
            "EfficientNetB0"
        )

        st.metric(
            "Classes",
            "20"
        )

    st.info(
        result["description"]
    )