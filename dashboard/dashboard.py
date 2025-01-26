import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Peminjaman Sepeda", page_icon="🚴", layout="wide")

hour_df = pd.read_csv('dashboard/hour_data.csv')
day_df = pd.read_csv('dashboard/day_data.csv')

weekday_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
day_df['weekday'] = pd.Categorical(day_df['weekday'], categories=weekday_order, ordered=True)

st.sidebar.header("Filter Data")

min_date = pd.to_datetime(day_df['dteday'].min()).date()
max_date = pd.to_datetime(day_df['dteday'].max()).date()

# Filter berdasarkan range tanggal
start_date = st.sidebar.date_input("Pilih Tanggal Awal", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", value=max_date, min_value=start_date, max_value=max_date)

filtered_day_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]

# **1. Rata-rata Pemakaian Sepeda per Hari dalam Seminggu**
daily_avg = filtered_day_df.groupby('weekday')['cnt'].mean()

# **2. Rata-rata Pemakaian Sepeda per Jam berdasarkan Tanggal yang Dipilih**
filtered_hour_df = hour_df[(hour_df['dteday'] >= str(start_date)) & (hour_df['dteday'] <= str(end_date))]
hourly_avg = filtered_hour_df.groupby('hr')['cnt'].mean()

# **Header**
st.title("Dashboard Analisis Peminjaman Sepeda")
st.markdown("""### Analisis Pemakaian Sepeda Sepanjang Minggu dan Per Jam
Menganalisis pola peminjaman sepeda sepanjang minggu dan rata-rata pemakaian sepeda per jam dalam sehari.""")

st.markdown(f"##### Data Filtered: Tanggal {start_date} sampai {end_date}")

# **Grafik 1: Rata-rata Peminjaman Sepeda per Hari**
fig1, ax1 = plt.subplots(figsize=(12, 7))
sns.barplot(
    x=daily_avg.index,
    y=daily_avg.values,
    palette='Blues_d',
    edgecolor='black',
    ax=ax1
)

ax1.set_title('Rata-rata Peminjaman Sepeda per Hari dalam Seminggu', fontsize=16, fontweight='bold')
ax1.set_xlabel('Hari dalam Seminggu', fontsize=14)
ax1.set_ylabel('Rata-rata Jumlah Peminjaman', fontsize=14)
ax1.set_xticklabels(daily_avg.index, fontsize=12, rotation=0)
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.tick_params(axis='both', labelsize=12)

plt.tight_layout()
st.pyplot(fig1)

# Insight pola peminjaman sepeda sepanjang minggu
max_borrowing_day = daily_avg.idxmax()
max_borrowing_day_value = daily_avg.max()

min_borrowing_day = daily_avg.idxmin()
min_borrowing_day_value = daily_avg.min()

st.markdown(f"""### Insight Rata-rata Pemakaian Sepeda Sepanjang Minggu:
- **Hari {max_borrowing_day}** adalah hari dengan jumlah rata-rata peminjaman sepeda tertinggi, yaitu sebanyak {max_borrowing_day_value:.0f} peminjaman.
- **Hari {min_borrowing_day}** adalah hari dengan jumlah rata-rata peminjaman sepeda terendah, yaitu sebanyak {min_borrowing_day_value:.0f} peminjaman.
""")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# **Grafik 2: Rata-rata Pemakaian Sepeda per Jam**
fig2, ax2 = plt.subplots(figsize=(12, 7))
sns.lineplot(data=hourly_avg, marker='o', color='royalblue', ax=ax2, linewidth=3, markersize=8)
ax2.set_title('Rata-rata Pemakaian Sepeda per Jam pada Rentang Tanggal', fontsize=16, fontweight='bold')
ax2.set_xlabel('Jam', fontsize=14)
ax2.set_ylabel('Jumlah Peminjaman', fontsize=14)
ax2.set_xticks(range(24))
ax2.grid(True)
ax2.tick_params(axis='both', labelsize=12)
st.pyplot(fig2)

# Insight pola peminjaman sepeda per jam
max_borrowing_hour = hourly_avg.idxmax()
max_borrowing_value = hourly_avg.max()

min_borrowing_hour = hourly_avg.idxmin()
min_borrowing_value = hourly_avg.min()

st.markdown(f"""
### Insight Rata-rata Pemakaian Sepeda per Jam:
- **Jam {max_borrowing_hour}** adalah jam dengan jumlah peminjaman sepeda tertinggi, yaitu sebanyak {max_borrowing_value:.0f} peminjaman.
- **Jam {min_borrowing_hour}** adalah jam dengan jumlah peminjaman sepeda terendah, yaitu sebanyak {min_borrowing_value:.0f} peminjaman.
""")

# **Footer**
st.markdown("""<hr><div style="text-align: center; font-size: 14px; color: #555;">
    <p>Created by <strong>Bimo</strong> - Peminjaman Sepeda</p></div>""", unsafe_allow_html=True)

st.markdown("""<style>
    .reportview-container .main .block-container { padding: 2rem; }
    .title { font-size: 30px; font-weight: bold; }
    .markdown-text-container { font-size: 18px; color: #333; line-height: 1.6; }
</style>""", unsafe_allow_html=True)
