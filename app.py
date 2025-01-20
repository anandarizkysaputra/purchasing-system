import streamlit as st
import pandas as pd

# Simulasi data purchasing
DATA_FILE = 'data.csv'

# Fungsi untuk memuat data dari file CSV
@st.cache_data
def load_data():
    try:
        data = pd.read_csv(DATA_FILE)
        # Pastikan kolom sudah lengkap
        expected_columns = ['ID', 'Item', 'Quantity', 'Price', 'Total']
        for col in expected_columns:
            if col not in data.columns:
                data[col] = "" if col in ['ID', 'Item'] else 0
    except FileNotFoundError:
        data = pd.DataFrame(columns=['ID', 'Item', 'Quantity', 'Price', 'Total'])
    return data

# Fungsi untuk menyimpan data ke file CSV
def save_data(data):
    column_order = ['ID', 'Item', 'Quantity', 'Price', 'Total']
    data = data[column_order]
    data.to_csv(DATA_FILE, index=False)

# Fungsi untuk membuat ID unik berdasarkan nama barang
def generate_item_id(item_name, data):
    initials = ''.join(word[0].upper() for word in item_name.split())
    count = sum(data['ID'].str.startswith(initials)) if not data.empty else 0
    return f"{initials}-{count + 1:03d}"

# Inisialisasi data di session_state jika belum ada
if 'data' not in st.session_state:
    st.session_state['data'] = load_data()

# Aplikasi Streamlit
st.title("Sistem Purchasing Barang dengan ID Unik")

# Form input untuk menambahkan barang
st.subheader("Tambah Barang")
with st.form("purchase_form"):
    item = st.text_input("Nama Barang", key="item_input")
    quantity = st.number_input("Jumlah", min_value=1, step=1, key="quantity_input")
    price = st.number_input("Harga per Barang", min_value=0.0, step=0.01, key="price_input")
    submitted = st.form_submit_button("Tambah")

    if submitted:
        if not item.strip():
            st.error("Nama barang tidak boleh kosong!")
        else:
            total = quantity * price
            item_id = generate_item_id(item, st.session_state['data'])  # Buat ID barang
            new_row = {'ID': item_id, 'Item': item, 'Quantity': quantity, 'Price': price, 'Total': total}
            st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Barang dengan ID {item_id} berhasil ditambahkan!")

# Tombol untuk menyimpan data ke file
if st.button("Simpan Data ke File"):
    save_data(st.session_state['data'])
    st.success("Data berhasil disimpan ke file!")

# Tampilkan data purchasing
st.subheader("Data Purchasing")
st.dataframe(st.session_state['data'])

# Total belanja
st.subheader("Total Belanja")
st.write(f"Rp {st.session_state['data']['Total'].sum():,.2f}")
