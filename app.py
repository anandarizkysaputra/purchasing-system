
import streamlit as st
import pandas as pd

# Simulasi data purchasing
DATA_FILE = 'data.csv'

# Fungsi untuk memuat data
@st.cache
def load_data():
    try:
        data = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Item', 'Quantity', 'Price', 'Total'])
    return data

# Fungsi untuk menyimpan data
def save_data(data):
    data.to_csv(DATA_FILE, index=False)

# Aplikasi Streamlit
st.title("Sistem Purchasing Barang")

# Load data
data = load_data()

# Form input
with st.form("purchase_form"):
    item = st.text_input("Nama Barang")
    quantity = st.number_input("Jumlah", min_value=1)
    price = st.number_input("Harga per Barang", min_value=0.0)
    submitted = st.form_submit_button("Tambah")

    if submitted:
        total = quantity * price
        new_row = {'Item': item, 'Quantity': quantity, 'Price': price, 'Total': total}
        data = data.append(new_row, ignore_index=True)
        save_data(data)
        st.success("Barang berhasil ditambahkan!")

# Tampilkan data
st.subheader("Data Purchasing")
st.dataframe(data)

# Total belanja
st.subheader("Total Belanja")
st.write(f"Rp {data['Total'].sum():,.2f}")
