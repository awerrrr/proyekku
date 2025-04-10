import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard layout="wide")

st.sidebar.title("🛍️ E-Commerce Dashboard")
st.sidebar.markdown("Analisis penjualan berdasarkan data transaksi e-commerce.")
menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Filter Data"])

@st.cache_data
def load_data():
    orders = pd.read_csv("orders_cleaned.csv", parse_dates=["order_purchase_timestamp"])
    order_items = pd.read_csv("order_items_cleaned.csv")
    products = pd.read_csv("products_cleaned.csv")
    translation = pd.read_csv("product_category_cleaned.csv")
    payments = pd.read_csv("order_payments_cleaned.csv")
    return orders, order_items, products, translation, payments

orders, order_items, products, translation, payments = load_data()

products = products.merge(translation, on="product_category_name", how="left")

if menu == "Beranda":
    st.header("👋 Selamat Datang di Dashboard E-Commerce!")
    st.markdown("""
    Dashboard ini menyajikan visualisasi dan analisis dari data transaksi e-commerce.  
    - 📈 Tren penjualan
    - 🔥 Produk paling populer
    - 💳 Metode pembayaran yang paling sering digunakan

    """)

    st.info("Tip: Buka menu 'Filter Data' untuk mulai eksplorasi data!")

    st.subheader("📌 Ringkasan Dataset")
    total_orders = len(orders)
    total_products = products["product_id"].nunique()
    total_customers = orders["customer_id"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pesanan", f"{total_orders:,}")
    col2.metric("Jumlah Produk", f"{total_products:,}")
    col3.metric("Jumlah Pelanggan", f"{total_customers:,}")

if menu == "Filter Data":
    st.header("Filter Data E-Commerce")

    start_date, end_date = st.date_input(
        "Pilih Rentang Waktu",
        min_value=orders["order_purchase_timestamp"].min().date(),
        max_value=orders["order_purchase_timestamp"].max().date(),
        value=[
            orders["order_purchase_timestamp"].min().date(),
            orders["order_purchase_timestamp"].max().date()
        ]
    )

    # Filter data berdasarkan rentang waktu
    filtered_orders = orders[
        (orders["order_purchase_timestamp"].dt.date >= start_date) &
        (orders["order_purchase_timestamp"].dt.date <= end_date)
    ]
    filtered_order_items = order_items[order_items["order_id"].isin(filtered_orders["order_id"])]
    filtered_payments = payments[payments["order_id"].isin(filtered_orders["order_id"])]

    # ========================
    st.subheader("📈 Tren Penjualan Bulanan")
    trend = (
        filtered_orders
        .groupby(filtered_orders["order_purchase_timestamp"].dt.to_period("M"))
        .size()
        .reset_index(name='count')
    )
    trend["order_purchase_timestamp"] = trend["order_purchase_timestamp"].dt.to_timestamp()

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(trend["order_purchase_timestamp"].astype(str), trend["count"])
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("Jumlah Pesanan")
    ax1.set_title("Tren Penjualan Bulanan")
    ax1.tick_params(axis="x", rotation=45)
    st.pyplot(fig1)

    # ========================
    st.subheader("🔥 Tren Penjualan Produk Terpopuler per Bulan")

    filtered_order_items = filtered_order_items.merge(
        filtered_orders[["order_id", "order_purchase_timestamp"]], on="order_id", how="left")
    filtered_order_items = filtered_order_items.merge(products, on="product_id", how="left")
    filtered_order_items = filtered_order_items.dropna(subset=["product_category_name_english"])

    filtered_order_items["bulan"] = filtered_order_items["order_purchase_timestamp"].dt.to_period("M").astype(str)

    top_n = 3
    top_products = (
        filtered_order_items["product_id"]
        .value_counts()
        .head(top_n)
        .index.tolist()
    )

    top_data = filtered_order_items[filtered_order_items["product_id"].isin(top_products)]
    top_data["product_name"] = top_data["product_category_name_english"]

    monthly_trend = top_data.groupby(["product_name", "bulan"]).size().reset_index(name="jumlah_pembelian")
    pivot_df = monthly_trend.pivot(index="bulan", columns="product_name", values="jumlah_pembelian").fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))
    pivot_df.plot(kind="bar", ax=ax)
    ax.set_title("Tren Penjualan Bulanan Produk Terpopuler")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pembelian")
    ax.legend(title="Produk", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # ========================
    st.subheader("💳 Distribusi Metode Pembayaran")

    # Ambil waktu transaksi dari data order dan join dengan pembayaran
    payments_with_time = payments.merge(
        orders[["order_id", "order_purchase_timestamp"]], on="order_id", how="left"
    )
    payments_with_time = payments_with_time[
        (payments_with_time["order_purchase_timestamp"].dt.date >= start_date) &
        (payments_with_time["order_purchase_timestamp"].dt.date <= end_date)
    ]

    payment_counts = payments_with_time["payment_type"].value_counts()

    fig3, ax3 = plt.subplots()
    payment_counts.plot(kind="bar", ax=ax3)
    ax3.set_xlabel("Metode Pembayaran")
    ax3.set_ylabel("Jumlah Transaksi")
    ax3.set_title("Distribusi Metode Pembayaran")
    ax3.tick_params(axis="x", rotation=45)
    st.pyplot(fig3)
