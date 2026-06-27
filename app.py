import streamlit as st

from components.header import show_header
from components.uploader import image_uploader
from components.prediction import show_prediction
from components.nutrition import show_nutrition
from components.footer import show_footer

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="FoodAI",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)
with st.sidebar:

    st.title("🍽 FoodAI")

    st.markdown("---")

    st.markdown("### AI Model")

    st.write("EfficientNetB0")

    st.markdown("### Classes")

    st.write("20 Food Categories")

    st.markdown("### Validation Accuracy")

    st.write("85.28%")

    st.markdown("### Framework")

    st.write("TensorFlow + Streamlit")
# ----------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{
padding-top:2rem;
padding-left:4rem;
padding-right:4rem;
padding-bottom:2rem;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

show_header()

# ----------------------------------------------------
# MAIN LAYOUT
# ----------------------------------------------------

left, right = st.columns([1, 1.2], gap="large")

with left:

    image = image_uploader()

with right:

    result = show_prediction(image)
with st.expander("ℹ️ Model Information"):

    st.markdown("""
### Supported Food Categories

FoodAI is trained on **20 specific food categories** using **EfficientNetB0**.

**Supported Classes:**

- Baklava
- Cheesecake
- Donuts
- French Fries
- Fried Rice
- Garlic Bread
- Grilled Cheese Sandwich
- Hot & Sour Soup
- Ice Cream
- Nachos
- Onion Rings
- Pancakes
- Pizza
- Ramen
- Red Velvet Cake
- Samosa
- Spring Rolls
- Sushi
- Tacos
- Waffles

---

**Important Note**

This model is a **closed-set classifier**, meaning it can only recognize the food categories it was trained on.

If you upload an image outside these categories (for example: Burger, Biryani, Coffee, Pasta, Sandwiches, etc.), the model will still predict the **closest supported class**. In such cases, the prediction may have **low confidence** and should not be considered accurate.
""")
# ----------------------------------------------------
# NUTRITION
# ----------------------------------------------------

show_nutrition(result)

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

show_footer()