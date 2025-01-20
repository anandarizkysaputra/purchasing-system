import streamlit as st
import pandas as pd

# Simulasi data purchasing
DATA_FILE = 'data.csv'

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        data = pd.DataFrame(columns=['ID', 'Item', 'Quantity', 'Price', 'Total'])
    return data

# Fungsi untuk menyimpan data
def save_data(data):
    data.to_csv(DATA_FILE, index=False)

# Fungsi untuk membuat ID barang
def generate_item_id(item_name, data):
    # Ambil huruf pertama dari setiap kata pada nama barang
    initials = ''.join(word[0].upper() for word in item_name.split())
    # Hitung jumlah barang dengan inisial yang sama untuk menentukan nomor urut
    count = sum(data['ID'].str.startswith(initials)) if not data.empty else 0
    return f"{initials}-{count + 1:03d}"

# Aplikasi Streamlit
st.title("Sistem Purchasing Barang dengan ID Unik")

# Load data
data = load_data()

# Form input
with st.form("purchase_form"):
    item = st.text_input("Nama Barang")
    quantity = st.number_input("Jumlah", min_value=1, step=1)
    price = st.number_input("Harga per Barang", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Tambah")

    if submitted:
        if not item.strip():
            st.error("Nama barang tidak boleh kosong!")
        else:
            total = quantity * price
            item_id = generate_item_id(item, data)  # Buat ID barang
            new_row = {'ID': item_id, 'Item': item, 'Quantity': quantity, 'Price': price, 'Total': total}
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)  # Tambahkan data baru
            save_data(data)
            st.success(f"Barang dengan ID {item_id} berhasil ditambahkan!")

# Tampilkan data
st.subheader("Data Purchasing")
st.dataframe(data)

# Total belanja
st.subheader("Total Belanja")
st.write(f"Rp {data['Total'].sum():,.2f}")
