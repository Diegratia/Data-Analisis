
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

st.title("Dashboard Analisis Penyewaan Sepeda (2011-2012)")

@st.cache_data  
def load_data():
    df_day = pd.read_csv('./data/day.csv')
    df_hour = pd.read_csv('./data/hour.csv')
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
    df_day['cnt'] = df_day['cnt'].fillna(df_day['cnt'].median())
    df_hour['cnt'] = df_hour['cnt'].fillna(df_hour['cnt'].median())
   
    df_hour['day_type'] = df_hour['weekday'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')
    return df_day, df_hour

df_day, df_hour = load_data()

# rata rata berdasarkan cuaca
st.subheader("Rata-rata Penyewaan Berdasarkan Cuaca")
weather_group = df_day.groupby('weathersit')['cnt'].mean().reset_index()
fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_group, palette='Blues_d', ax=ax1)
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Cuaca', fontsize=14)
plt.xlabel('Kondisi Cuaca\n(1: Cerah/Sedikit Berawan, 2: Kabut/Berawan, 3: Hujan)', fontsize=12)
plt.ylabel('Jumlah Penyewaan', fontsize=12)
st.pyplot(fig1)

# pola sewa perjam
st.subheader("Pola Penyewaan Sepeda per Jam")
hourly_group = df_hour.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hr', y='cnt', hue='day_type', data=hourly_group, palette='Set1', ax=ax2)
plt.title('Pola Penyewaan Sepeda per Jam', fontsize=14)
plt.xlabel('Jam', fontsize=12)
plt.ylabel('Jumlah Penyewaan', fontsize=12)
plt.legend(title='Tipe Hari')
st.pyplot(fig2)

# Kesimpulan
st.subheader("Kesimpulan")
st.write("""
1. Cuaca cerah/sedikit berawan (weathersit=1) memiliki rata-rata penyewaan tertinggi dibandingkan kondisi lainnya.
2. Pada hari kerja, puncak penyewaan terjadi di jam sibuk (pagi dan sore), sedangkan pada akhir pekan lebih merata.
""")