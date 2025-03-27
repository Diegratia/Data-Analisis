import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_day = pd.read_csv('./data/day.csv')
df_hour = pd.read_csv('./data/hour.csv')

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
df_day['cnt'] = df_day['cnt'].fillna(df_day['cnt'].median())
df_hour['cnt'] = df_hour['cnt'].fillna(df_hour['cnt'].median())
weather_map = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Ringan', 4: 'Hujan Berat'}
df_day['weather_desc'] = df_day['weathersit'].map(weather_map)
df_hour['day_type'] = df_hour['weekday'].apply(lambda x: 'Weekday' if x < 5 else 'Weekend')

# Dashboard
st.title("Dashboard Penyewaan Sepeda")

st.sidebar.header("Filter Data")
date_range = st.sidebar.date_input("Pilih rentang tanggal", [df_day['dteday'].min(), df_day['dteday'].max()])
start_date, end_date = date_range
filtered_df_day = df_day[(df_day['dteday'] >= pd.to_datetime(start_date)) & (df_day['dteday'] <= pd.to_datetime(end_date))]

# visualisasi 1
st.subheader("Pengaruh Cuaca terhadap Rata-rata Penyewaan Harian")
weather_group = filtered_df_day.groupby('weather_desc')['cnt'].mean().reset_index()
fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.barplot(x='weather_desc', y='cnt', data=weather_group, palette='Blues_d', ax=ax1)
ax1.set_title('Pengaruh Cuaca terhadap Rata-rata Penyewaan Harian')
ax1.set_xlabel('Kondisi Cuaca')
ax1.set_ylabel('Rata-rata Penyewaan Harian')
plt.xticks(rotation=45)
st.pyplot(fig1)

# visualisasi 2
st.subheader("Puncak Penyewaan per Jam: Hari Kerja vs Akhir Pekan")
hourly_group = df_hour.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hr', y='cnt', hue='day_type', data=hourly_group, marker='o', ax=ax2)
ax2.set_title('Pola Penyewaan Sepeda per Jam')
ax2.set_xlabel('Jam (0-23)')
ax2.set_ylabel('Rata-rata Penyewaan')
ax2.set_xticks(range(0, 24))
ax2.legend(title='Tipe Hari')
st.pyplot(fig2)