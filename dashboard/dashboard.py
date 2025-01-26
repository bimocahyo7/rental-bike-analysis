import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

hour_df = pd.read_csv('dashboard/hour_data.csv')
day_df = pd.read_csv('dashboard/day_data.csv')

hour_df.replace([np.inf, -np.inf], np.nan, inplace=True)
hour_df.fillna(0, inplace=True)

day_df.replace([np.inf, -np.inf], np.nan, inplace=True)
day_df.fillna(0, inplace=True)

weekday_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
day_df['weekday'] = pd.Categorical(day_df['weekday'], categories=weekday_order, ordered=True)

# 1. Rata-rata Pemakaian Sepeda per Jam (hour_df)
hourly_avg = hour_df.groupby('hr')['cnt'].mean()

# 2. Rata-rata Pemakaian Sepeda per Hari dalam Seminggu (day_df)
daily_avg = day_df.groupby('weekday')['cnt'].mean()

# Menampilkan Header di Streamlit
st.set_page_config(page_title="Dashboard Peminjaman Sepeda", page_icon="🚴", layout="wide")
st.title("Dashboard Analisis Peminjaman Sepeda")
st.markdown("""### Analisis Pemakaian Sepeda Sepanjang Minggu dan Per Jam
Menganalisis pola peminjaman sepeda sepanjang minggu dan rata-rata pemakaian sepeda per jam dalam sehari.""")

# **Grafik 1: Rata-rata Pemakaian Sepeda per Hari dalam Seminggu**
fig1, ax1 = plt.subplots(figsize=(12, 7))
sns.lineplot(data=daily_avg, marker='o', color='mediumseagreen', ax=ax1, linewidth=3, markersize=8)
ax1.set_title('Rata-rata Pemakaian Sepeda per Hari dalam Seminggu', fontsize=16, fontweight='bold')
ax1.set_xlabel('Hari dalam Seminggu', fontsize=14)
ax1.set_ylabel('Jumlah Peminjaman', fontsize=14)
ax1.set_xticks(range(7))
ax1.set_xticklabels(weekday_order, fontsize=12)
ax1.grid(True)
ax1.tick_params(axis='both', labelsize=12)
st.pyplot(fig1)

# Insight pola peminjaman sepeda sepanjang minggu
st.markdown("""### Insight Rata-rata Pemakaian Sepeda Sepanjang Minggu:
- Perbedaan antara hari-hari dalam seminggu tidak terlalu mencolok, yang menunjukkan bahwa sepeda cukup digunakan sepanjang minggu, baik untuk keperluan kerja atau rekreasi.
- Peminjaman sepeda pada hari kerja (Senin hingga Jumat) menunjukkan rata-rata peminjaman yang lebih tinggi dibandingkan dengan akhir pekan (Sabtu dan Minggu).
""")

# **Grafik 2: Rata-rata Pemakaian Sepeda per Jam dalam Sehari**
fig2, ax2 = plt.subplots(figsize=(12, 7))
sns.lineplot(data=hourly_avg, marker='o', color='royalblue', ax=ax2, linewidth=3, markersize=8)
ax2.set_title('Rata-rata Pemakaian Sepeda per Jam dalam Sehari', fontsize=16, fontweight='bold')
ax2.set_xlabel('Jam', fontsize=14)
ax2.set_ylabel('Jumlah Peminjaman', fontsize=14)
ax2.set_xticks(range(24))
ax2.grid(True)
ax2.tick_params(axis='both', labelsize=12)
st.pyplot(fig2)

# Insight pola peminjaman sepeda per jam
max_borrowing_hour = hourly_avg.idxmax()
max_borrowing_value = hourly_avg.max()

st.markdown(f"""
### Insight Rata-rata Pemakaian Sepeda per Jam dalam Sehari:
- Jam {max_borrowing_hour} adalah jam dengan jumlah peminjaman sepeda tertinggi, yaitu sebanyak {max_borrowing_value:.0f} peminjaman.
- Pemakaian sepeda cenderung lebih tinggi pada jam-jam sibuk, seperti pagi hari (sekitar jam 7-9) dan sore hari (sekitar jam 17-19), yang mungkin berhubungan dengan penggunaan sepeda untuk pergi bekerja atau pulang kerja.
""")

# **Footer**
st.markdown("""<hr><div style="text-align: center; font-size: 14px; color: #555;">
    <p>Created by <strong>Bimo</strong> - Peminjaman Sepeda</p></div>""", unsafe_allow_html=True)

st.markdown("""<style>
    .reportview-container .main .block-container { padding: 2rem; }
    .title { font-size: 30px; font-weight: bold; }
    .markdown-text-container { font-size: 18px; color: #333; line-height: 1.6; }
</style>""", unsafe_allow_html=True)
