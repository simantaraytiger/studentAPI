import streamlit as st
import requests
import pandas as pd
import math
import altair as alt

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


all_products = fetch_products()

# Sidebar filter
st.sidebar.header("Filter")
if all_products:
    prices = [p["price"] for p in all_products]
    min_price, max_price = st.sidebar.slider(
        "Select price range:",
        min_value=float(min(prices)) - 10,
        max_value=float(max(prices)) + 10,
        value=(float(min(prices)), float(max(prices))),
        step=.5,
    )
else:
    min_price, max_price = (0.0, 0.0)

# Apply filter
products = [p for p in all_products if min_price <= p["price"] <= max_price]  # type: ignore

# List all products
st.subheader("Products")
PAGE_SIZE = 5
total_products = len(products)
total_pages = math.ceil(total_products / PAGE_SIZE)

# Initialize current page in session state
if "product_page" not in st.session_state:
    st.session_state.product_page = 1

st.caption(f"Page {st.session_state.product_page} of {total_pages}")

# Get products for current page
start = (st.session_state.product_page - 1) * PAGE_SIZE
end = start + PAGE_SIZE
current_products = products[start:end]

# Display paginated products
if current_products:
    for product in current_products:
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
    st.warning("No products in selected price range or page is empty.")

prev_col, next_col = st.columns([1, 1])
with prev_col:
    if st.button("Prev", disabled=st.session_state.product_page <= 1):
        st.session_state.product_page -= 1
with next_col:
    if st.button("Next", disabled=st.session_state.product_page > total_pages):
        st.session_state.product_page += 1


# Edit product
st.subheader("Edit Product")
if "edit_id" in st.session_state:
    with st.form("edit_product_form"):
        name = st.text_input("Product Name", value=st.session_state.edit_name)
        price = st.number_input(
            "Price", value=st.session_state.edit_price, min_value=0.0
        )
        description = st.text_input(
            "Description", value=st.session_state.edit_description
        )
        submitted = st.form_submit_button("Update")

        if submitted:
            payload = {"name": name, "price": price, "description": description}
            res = requests.put(
                f"{API_URL}/product/{st.session_state.edit_id}", json=payload
            )
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
    name = st.text_input("Product Name")
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

st.subheader("📊 Interactive Price Chart")
if products:
    df_chart = pd.DataFrame(products)
    chart = (
        alt.Chart(df_chart)
        .mark_bar()
        .encode(
            x=alt.X("name:N", title="Product Name"),
            y=alt.Y("price:Q", title="Price (₹)"),
            tooltip=["name", "price", "description"]
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No products to show in chart.")