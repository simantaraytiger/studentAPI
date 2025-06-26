import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.title("Product Managemen")

# Fetch products
def fetch_products():
    try:
        res = requests.get(f"{API_URL}/product")
        if res.status_code == 200:
            return res.json().get("data", [])
    except Exception:
        return []

products = fetch_products()

# List all products
st.subheader("Products")

if products:
    for product in products:
        cols = st.columns([1, 3, 2, 3, 2, 2])
        cols[0].markdown(f"**ID:** {product['id']}")
        cols[1].markdown(f"**Name:** {product['name']}")
        cols[2].markdown(f"**Rs:** ₹{product['price']}")
        cols[3].markdown(f"**Desc:** {product.get('description', '')}")

        if cols[4].button("Edit", key=f"edit-{product['id']}"):
            st.session_state.edit_id = product["id"]
            st.session_state.edit_name = product["name"]
            st.session_state.edit_price = product["price"]
            st.session_state.edit_description = product.get("description", "")

        if cols[5].button("Delete", key=f"delete-{product['id']}"):
            del_res = requests.delete(f"{API_URL}/product/{product['id']}")
            if del_res.status_code == 200:
                st.success(f"Deleted product ID {product['id']}")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Delete failed")
else:
    st.warning("No products found or API error.")

# Edit product
st.subheader("Edit Product")
if "edit_id" in st.session_state:
    with st.form("edit_product_form"):
        name = st.text_input("Product Name", value=st.session_state.edit_name)
        price = st.number_input("Price", value=st.session_state.edit_price, min_value=0.0)
        description = st.text_input("Description", value=st.session_state.edit_description)
        submitted = st.form_submit_button("Update")

        if submitted:
            payload = {"name": name, "price": price, "description": description}
            res = requests.put(f"{API_URL}/product/{st.session_state.edit_id}", json=payload)
            if res.status_code == 200:
                st.success("Product updated!")
                st.cache_data.clear()
                del st.session_state.edit_id
                st.rerun()
            else:
                st.error("Failed to update product")
else:
    st.info("Select a product to edit.")

# Add new product
st.subheader("Add New Product")
with st.form("add_product"):
    name = st.text_input("Name")
    price = st.number_input("Price", min_value=0.0)
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Product")

    if submitted:
        payload = {"name": name, "price": price, "description": description}
        res = requests.post(f"{API_URL}/product", json=payload)
        if res.status_code == 200:
            st.success("Product added!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("Failed to add product")

# Show product price chart
st.subheader("Price Chart")
if products:
    df = pd.DataFrame(products)
    st.bar_chart(df.set_index("name")["price"])
else:
    st.info("No products to show in chart.")
