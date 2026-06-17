import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sistem Kemacetan Fuzzy", page_icon="🚗")

st.title("🚗 Sistem Tingkat Kemacetan (Logika Fuzzy)")
st.write("Aplikasi untuk menentukan kategori tingkat kemacetan berdasarkan jumlah kendaraan menggunakan Logika Fuzzy.")

def hitung_derajat_keanggotaan(x):
    # Lancar
    if x <= 400:
        mu_lancar = 1.0
    elif 400 < x < 600:
        mu_lancar = (600 - x) / 200.0
    else:
        mu_lancar = 0.0

    # Padat
    if x <= 400 or x >= 800:
        mu_padat = 0.0
    elif 400 < x <= 600:
        mu_padat = (x - 400) / 200.0
    elif 600 < x < 800:
        mu_padat = (800 - x) / 200.0

    # Macet
    if x <= 600:
        mu_macet = 0.0
    elif 600 < x < 800:
        mu_macet = (x - 600) / 200.0
    else:
        mu_macet = 1.0

    return mu_lancar, mu_padat, mu_macet

# Input nilai
st.sidebar.header("Input Parameter")
nilai = st.sidebar.number_input("Masukkan Jumlah Kendaraan (0-1000):", min_value=0.0, max_value=1000.0, value=500.0, step=10.0)

mu_l, mu_p, mu_m = hitung_derajat_keanggotaan(nilai)

# 1. Derajat Keanggotaan Input
st.header("1. Derajat Keanggotaan Input")
st.write(f"Berikut adalah proses perhitungan derajat keanggotaan untuk input jumlah kendaraan **x = {nilai}**:")

# Kalkulasi LaTeX dinamis untuk Lancar
if nilai <= 400:
    calc_l = "1"
elif 400 < nilai < 600:
    calc_l = f"\\frac{{600 - {nilai}}}{{200}} = {mu_l:.2f}"
else:
    calc_l = "0"

st.latex(rf'''
\mu_{{Lancar}}({nilai}) = {calc_l}
''')

# Kalkulasi LaTeX dinamis untuk Padat
if nilai <= 400 or nilai >= 800:
    calc_p = "0"
elif 400 < nilai <= 600:
    calc_p = f"\\frac{{{nilai} - 400}}{{200}} = {mu_p:.2f}"
elif 600 < nilai < 800:
    calc_p = f"\\frac{{800 - {nilai}}}{{200}} = {mu_p:.2f}"

st.latex(rf'''
\mu_{{Padat}}({nilai}) = {calc_p}
''')

# Kalkulasi LaTeX dinamis untuk Macet
if nilai <= 600:
    calc_m = "0"
elif 600 < nilai < 800:
    calc_m = f"\\frac{{{nilai} - 600}}{{200}} = {mu_m:.2f}"
else:
    calc_m = "1"

st.latex(rf'''
\mu_{{Macet}}({nilai}) = {calc_m}
''')

st.markdown("---")

# 2. Tabel Derajat Keanggotaan
st.header("2. Tabel Derajat Keanggotaan")
st.write(f"Berdasarkan jumlah kendaraan yang dimasukkan (**x = {nilai}**), berikut adalah nilai derajat keanggotaannya:")

data_derajat = [
    {"Kategori Kemacetan": "Lancar", "Derajat Keanggotaan (μ)": f"{mu_l:.2f}"},
    {"Kategori Kemacetan": "Padat", "Derajat Keanggotaan (μ)": f"{mu_p:.2f}"},
    {"Kategori Kemacetan": "Macet", "Derajat Keanggotaan (μ)": f"{mu_m:.2f}"}
]

st.table(data_derajat)

st.markdown("---")

# 3. Grafik Himpunan Fuzzy
st.header("3. Grafik Himpunan Fuzzy")

fig, ax = plt.subplots(figsize=(10, 5))

x = np.linspace(0, 1000, 1000)
y_lancar = np.piecewise(x, [x <= 400, (x > 400) & (x < 600), x >= 600], [1, lambda x: (600 - x)/200, 0])
y_padat = np.piecewise(x, [x <= 400, (x > 400) & (x <= 600), (x > 600) & (x < 800), x >= 800], [0, lambda x: (x - 400)/200, lambda x: (800 - x)/200, 0])
y_macet = np.piecewise(x, [x <= 600, (x > 600) & (x < 800), x >= 800], [0, lambda x: (x - 600)/200, 1])

ax.plot(x, y_lancar, 'g', label='Lancar')
ax.plot(x, y_padat, 'y', label='Padat')
ax.plot(x, y_macet, 'r', label='Macet')

# Garis input nilai
ax.axvline(x=nilai, color='k', linestyle='--', label=f'Input: {nilai}')

# Titik perpotongan
if mu_l > 0: ax.plot(nilai, mu_l, 'go', markersize=8)
if mu_p > 0: ax.plot(nilai, mu_p, 'yo', markersize=8)
if mu_m > 0: ax.plot(nilai, mu_m, 'ro', markersize=8)

ax.set_title('Fungsi Keanggotaan Himpunan Tingkat Kemacetan')
ax.set_xlabel('Jumlah Kendaraan')
ax.set_ylabel(r'Derajat Keanggotaan ($\mu$)')
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.markdown("---")

# 4. Interpretasi Hasil
st.header("4. Interpretasi Hasil")

# Cari nilai mu maksimum
kategori_dict = {"Lancar": mu_l, "Padat": mu_p, "Macet": mu_m}
max_kategori = max(kategori_dict, key=kategori_dict.get)
max_mu = kategori_dict[max_kategori]

st.write(f"Berdasarkan analisis logika fuzzy dari input jumlah kendaraan **{nilai}**:")

if max_mu > 0:
    st.write(f"Kondisi jalan raya paling dominan masuk ke dalam kategori **{max_kategori.upper()}** dengan derajat keanggotaan tertinggi sebesar **{max_mu:.2f}**.")
    
    # Detail tambahan jika masuk ke dua kategori (irisan)
    kategori_lain = {k: v for k, v in kategori_dict.items() if v > 0 and k != max_kategori}
    for k, v in kategori_lain.items():
        st.write(f"Namun juga memiliki sedikit kecenderungan masuk ke kategori **{k}** dengan derajat **{v:.2f}**.")
    
    st.write("### Kesimpulan")
    if max_kategori == "Lancar":
        st.success("💡 Interpretasi: Kondisi lalu lintas sangat baik dan lancar. Kendaraan dapat melaju dengan kecepatan normal.")
    elif max_kategori == "Padat":
        st.warning("💡 Interpretasi: Kondisi lalu lintas mulai padat. Arus kendaraan tersendat dan pengemudi diimbau untuk berhati-hati serta menjaga jarak aman.")
    else:
        st.error("💡 Interpretasi: Kondisi lalu lintas macet parah. Diperlukan intervensi penguraian lalu lintas atau pengendara disarankan mencari rute alternatif.")
else:
    st.warning("Jumlah kendaraan tidak masuk dalam kategori mana pun.")
