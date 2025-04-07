import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard", page_icon="", layout="wide")

@st.cache_data
def load_data():
    orders = pd.read_csv("orders_cleaned.csv")
    order_items = pd.read_csv("order_items_cleaned.csv")
    payments = pd.read_csv("order_payments_cleaned.csv")
    translation = pd.read_csv("product_category_cleaned.csv")
    products = pd.read_csv("products_cleaned.csv")
    return orders, order_items, payments, translation, products

orders, order_items, payments, translation, products = load_data()

with st.sidebar:
    selected = option_menu(
        menu_title="Dashboard Navigation",
        options=["Filter Data", "Tren Penjualan", "Produk Populer", "Metode Pembayaran"],
        icons=["filter", "graph-up", "cart", "credit-card"],
        menu_icon="cast",
        default_index=0
    )

if selected == "Filter Data":
    st.title("Filter Data E-Commerce")
    st.subheader("Pilih Rentang Waktu dan Kategori Produk")
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    min_date = orders["order_purchase_timestamp"].min()
    max_date = orders["order_purchase_timestamp"].max()

    start_date, end_date = st.date_input(
        label="Pilih Rentang Waktu", 
        min_value=min_date, max_value=max_date, 
        value=[min_date, max_date]
    )
    
    categories = translation["product_category_name_english"].unique()
    selected_category = st.selectbox("Pilih Kategori Produk", ["All"] + list(categories))
    

elif selected == "Tren Penjualan":
    st.title("Tren Penjualan dari Waktu ke Waktu")
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    sales_trend = orders.groupby(orders["order_purchase_timestamp"].dt.to_period("M")).size()
    
    fig, ax = plt.subplots()
    sales_trend.plot(kind='line', ax=ax)
    ax.set_title("Tren Penjualan")
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Jumlah Pesanan")
    st.pyplot(fig)

elif selected == "Produk Populer":
    st.title("Produk yang Paling Sering Dibeli")
    top_products = order_items["product_id"].value_counts().head(10).reset_index()
    top_products.columns = ["product_id", "count"]
    top_products = top_products.merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
    top_products = top_products.merge(translation, on="product_category_name", how="left")
    
    st.dataframe(top_products[["product_category_name_english", "count"]])

elif selected == "Metode Pembayaran":
    st.title("Metode Pembayaran Paling Populer")
    payment_counts = payments["payment_type"].value_counts()
    
    fig, ax = plt.subplots()
    payment_counts.plot(kind='bar', ax=ax)
    ax.set_title("Distribusi Metode Pembayaran")
    ax.set_xlabel("Tipe Pembayaran")
    ax.set_ylabel("Jumlah Transaksi")
    st.pyplot(fig)
