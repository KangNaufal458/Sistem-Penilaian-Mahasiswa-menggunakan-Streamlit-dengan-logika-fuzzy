import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sistem Penilaian Fuzzy", page_icon="🎓")

st.title("🎓 Sistem Penilaian Mahasiswa (Logika Fuzzy)")
st.write("Aplikasi untuk menentukan kategori nilai mahasiswa menggunakan Logika Fuzzy, lengkap dengan fungsi keanggotaan dan grafik.")

def hitung_derajat_keanggotaan(x):
    # Rendah
    if x <= 40:
        mu_rendah = 1.0
    elif 40 < x < 60:
        mu_rendah = (60 - x) / 20.0
    else:
        mu_rendah = 0.0

    # Sedang
    if x <= 40 or x >= 80:
        mu_sedang = 0.0
    elif 40 < x <= 60:
        mu_sedang = (x - 40) / 20.0
    elif 60 < x < 80:
        mu_sedang = (80 - x) / 20.0

    # Tinggi
    if x <= 60:
        mu_tinggi = 0.0
    elif 60 < x < 80:
        mu_tinggi = (x - 60) / 20.0
    else:
        mu_tinggi = 1.0

    return mu_rendah, mu_sedang, mu_tinggi

# Input nilai
st.sidebar.header("Input Parameter")
nilai = st.sidebar.number_input("Masukkan Nilai Mahasiswa (0-100):", min_value=0.0, max_value=100.0, value=70.0, step=1.0)

mu_r, mu_s, mu_t = hitung_derajat_keanggotaan(nilai)

# 1. Fungsi Keanggotaan
st.header("1. Fungsi Keanggotaan")
st.write("Berikut adalah rumus matematis fungsi keanggotaan yang digunakan:")

st.latex(r'''
\mu_{Rendah}(x) = 
\begin{cases} 
1, & x \le 40 \\
\frac{60 - x}{20}, & 40 < x < 60 \\
0, & x \ge 60 
\end{cases}
''')

st.latex(r'''
\mu_{Sedang}(x) = 
\begin{cases} 
0, & x \le 40 \text{ atau } x \ge 80 \\
\frac{x - 40}{20}, & 40 < x \le 60 \\
\frac{80 - x}{20}, & 60 < x < 80 
\end{cases}
''')

st.latex(r'''
\mu_{Tinggi}(x) = 
\begin{cases} 
0, & x \le 60 \\
\frac{x - 60}{20}, & 60 < x < 80 \\
1, & x \ge 80 
\end{cases}
''')

st.markdown("---")

# 2. Perhitungan Derajat Keanggotaan
st.header("2. Perhitungan Derajat Keanggotaan")
st.write(f"Berdasarkan nilai yang dimasukkan (**x = {nilai}**), berikut adalah nilai derajat keanggotaannya:")

col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**Rendah:**\n\n $\mu = {mu_r:.2f}$")
with col2:
    st.warning(f"**Sedang:**\n\n $\mu = {mu_s:.2f}$")
with col3:
    st.success(f"**Tinggi:**\n\n $\mu = {mu_t:.2f}$")

st.markdown("---")

# 3. Grafik Himpunan Fuzzy
st.header("3. Grafik Himpunan Fuzzy")

fig, ax = plt.subplots(figsize=(10, 5))

x = np.linspace(0, 100, 500)
y_rendah = np.piecewise(x, [x <= 40, (x > 40) & (x < 60), x >= 60], [1, lambda x: (60 - x)/20, 0])
y_sedang = np.piecewise(x, [x <= 40, (x > 40) & (x <= 60), (x > 60) & (x < 80), x >= 80], [0, lambda x: (x - 40)/20, lambda x: (80 - x)/20, 0])
y_tinggi = np.piecewise(x, [x <= 60, (x > 60) & (x < 80), x >= 80], [0, lambda x: (x - 60)/20, 1])

ax.plot(x, y_rendah, 'r', label='Rendah')
ax.plot(x, y_sedang, 'g', label='Sedang')
ax.plot(x, y_tinggi, 'b', label='Tinggi')

# Garis input nilai
ax.axvline(x=nilai, color='k', linestyle='--', label=f'Input Nilai: {nilai}')

# Titik perpotongan
if mu_r > 0: ax.plot(nilai, mu_r, 'ro', markersize=8)
if mu_s > 0: ax.plot(nilai, mu_s, 'go', markersize=8)
if mu_t > 0: ax.plot(nilai, mu_t, 'bo', markersize=8)

ax.set_title('Fungsi Keanggotaan Himpunan Fuzzy Penilaian')
ax.set_xlabel('Nilai')
ax.set_ylabel('Derajat Keanggotaan ($\mu$)')
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.markdown("---")

# 4. Interpretasi Hasil
st.header("4. Interpretasi Hasil")

# Cari nilai mu maksimum
kategori_dict = {"Rendah": mu_r, "Sedang": mu_s, "Tinggi": mu_t}
max_kategori = max(kategori_dict, key=kategori_dict.get)
max_mu = kategori_dict[max_kategori]

st.write(f"Berdasarkan analisis logika fuzzy dari input nilai **{nilai}**:")

if max_mu > 0:
    st.write(f"Mahasiswa ini paling dominan masuk ke dalam kategori **{max_kategori.upper()}** dengan derajat keanggotaan tertinggi sebesar **{max_mu:.2f}**.")
    
    # Detail tambahan jika masuk ke dua kategori (irisan)
    kategori_lain = {k: v for k, v in kategori_dict.items() if v > 0 and k != max_kategori}
    for k, v in kategori_lain.items():
        st.write(f"Namun juga memiliki kecenderungan masuk ke kategori **{k}** dengan derajat **{v:.2f}**.")
    
    st.write("### Kesimpulan")
    if max_kategori == "Rendah":
        st.error("💡 Interpretasi: Performa mahasiswa berada pada tingkat bawah. Sangat disarankan untuk memberikan bimbingan intensif dan mengikuti perbaikan (remedial).")
    elif max_kategori == "Sedang":
        st.warning("💡 Interpretasi: Performa mahasiswa cukup baik. Mahasiswa memiliki pemahaman menengah namun memerlukan dorongan belajar ekstra untuk mencapai hasil maksimal.")
    else:
        st.success("💡 Interpretasi: Performa mahasiswa sangat baik dan memuaskan. Pertahankan prestasi dan metode pembelajaran yang digunakan saat ini.")
else:
    st.warning("Nilai tidak masuk dalam kategori mana pun.")
