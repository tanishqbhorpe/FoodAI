import streamlit as st
from predict_food import predict_food


def show_prediction(image):

    if image is None:

        st.info("👈 Upload a food image to begin.")

        return

    with st.spinner("Analyzing image..."):

        result = predict_food(image)

    confidence = result["confidence"]
    # ------------------------------
# Unsupported Food Warning
# ------------------------------

    if confidence < 60:
         st.warning(
        "⚠️ This image may not belong to one of the 20 supported food categories. "
        "FoodAI is trained on only 20 food classes and predicts the closest matching class for unknown foods."
    )
    # ------------------------------
    # Confidence Badge
    # ------------------------------

    if confidence >= 90:
        st.success("🟢 HIGH CONFIDENCE")

    elif confidence >= 75:
        st.warning("🟡 MEDIUM CONFIDENCE")

    else:
        st.error("🔴 LOW CONFIDENCE")

    # ------------------------------
    # Food Name
    # ------------------------------

    st.markdown(
        f"""
        <h1 style="
            color:#4CAF50;
            font-size:52px;
            margin-bottom:10px;">
            {result['food']}
        </h1>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------

    st.progress(confidence / 100)

    # ------------------------------
    # Metrics
    # ------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

    with col2:

        st.metric(
            "Calories",
            f"{result['calories']} kcal"
        )

    st.metric(
        "Serving Size",
        result["serving"]
    )

    # ------------------------------

    st.markdown("### Description")

    st.info(result["description"])

    # ------------------------------

    st.markdown("### 🏆 Top 3 Predictions")

    for food in result["top3"]:

        st.write(f"**{food['food']}**")

        st.progress(food["confidence"] / 100)

        st.caption(
            f"{food['confidence']:.2f}% confidence"
        )
# ------------------------------
# Download Report
# ------------------------------

    report = f"""
    FoodAI Prediction Report
    ========================

    Prediction : {result['food']}

    Confidence : {confidence:.2f} %

    Calories : {result['calories']} kcal

    Serving : {result['serving']}

    Description :
    {result['description']}

    Top 3 Predictions
    -----------------

    """

    for item in result["top3"]:

     report += f"{item['food']} : {item['confidence']:.2f}%\n"

    
    return result