import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#judul streamlit
st.title("Analisis Data Bike Sharing 🚲✨")

#sidebar
dataset_option = st.sidebar.selectbox("Pilih Dataset:", ["Day", "Hour"])

#membaca dataset
day = pd.read_csv('dashboard/day_clean.csv')
hour = pd.read_csv('dashboard/hour_clean.csv')

data = day if dataset_option == "Day" else hour

#menampilkan dataset di streamlit
st.subheader("Menampilkan Dataset")
st.dataframe(data)

keterangan = {
    "Kolom": ["instant", "dteday", "season", "hr", "holiday", "weekday", "workingday", "weathersit",
              "temp", "atemp", "hum", "windspeed", "casual", "registered", "cnt"],
    "Deskripsi": [
        "Indeks unik untuk setiap entri data",
        "Tanggal dalam format YYYY-MM-DD",
        "Musim",
        "Jam dalam format 24 jam (0-23)",
        "Hari libur / tanggal merah",
        "Hari dalam seminggu",
        "Hari kerja",
        "Kondisi cuaca",
        "Suhu aktual dalam skala normalisasi (0-1)",
        "Temperatur yang terasa dalam skala normalisasi (0-1)",
        "Kelembapan dalam skala normalisasi (0-1)",
        "Kecepatan angin dalam skala normalisasi (0-1)",
        "Jumlah pengguna sepeda yang tidak terdaftar",
        "Jumlah pengguna sepeda yang terdaftar",
        "Total jumlah penggunaan sepeda (casual + registered)"
    ]
}

data_keterangan = pd.DataFrame(keterangan)
st.write("**Keterangan Kolom dalam Dataset:**")
st.dataframe(data_keterangan)

#visualisasi pertanyaan 1
st.subheader("Tren Penggunaan Sepeda Sepanjang Hari")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hour, x='hr', y='cnt', estimator='mean', ci=None, marker='o', ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Pengguna Sepeda")
ax.set_title("Tren Penggunaan Sepeda Sepanjang Hari")
ax.set_xticks(range(0, 24))
ax.grid()
st.pyplot(fig)

#keterangan pertanyaan 1
st.write("### ⏰ Tren Penggunaan Sepeda Sepanjang Hari")

st.write("""
Hasil analisis menunjukkan bahwa terdapat jam-jam tertentu di mana penggunaan sepeda meningkat secara signifikan, yaitu:  

- **08:00** → Jam berangkat kerja/sekolah  
- **17:00 - 18:00** → Jam pulang kerja/sekolah  

📌 **Kesimpulan:**  
Dengan mengetahui bahwa permintaan penggunaan sepeda cukup tinggi di jam tersebut, maka **ketersediaan sepeda pada jam-jam tersebut dapat lebih dioptimalkan** agar layanan tetap lancar.
""")

#visualisasi pertanyaan 2
st.subheader("Total Penggunaan Sepeda di Setiap Musim")
penggunaan_per_musim = day.groupby('season')['cnt'].sum().reset_index()

urutan_musim = ['winter', 'spring', 'summer', 'fall']
penggunaan_per_musim['season'] = pd.Categorical(penggunaan_per_musim['season'], categories=urutan_musim, ordered=True)
penggunaan_per_musim = penggunaan_per_musim.sort_values('season')

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(penggunaan_per_musim['season'], penggunaan_per_musim['cnt'], color=['blue', 'green', 'red', 'orange'])
ax.set_title("Total Penggunaan Sepeda di Setiap Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Total Pengguna Sepeda")
ax.set_xticks(range(len(urutan_musim)))
ax.set_xticklabels(urutan_musim, rotation=30)  # Rotasi jika label terlalu panjang
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

#keterangan pertanyaan 2
st.write("### 🌦️ Pengaruh Musim terhadap Penggunaan Sepeda")

st.write("""
Hasil visualisasi menunjukkan bahwa terdapat pengaruh musim terhadap total penggunaan sepeda. 

- 🌞 **Total penggunaan sepeda tertinggi** terjadi pada **musim panas**.
- ❄️ **Total penggunaan sepeda terendah** terjadi pada **musim dingin**.

Ini berarti **semakin hangat dan nyaman cuaca, semakin banyak orang menggunakan sepeda**.  
Faktor lain yang mempengaruhi meningkatnya penggunaan sepeda pada musim panas mungkin dikarenakan adanya **liburan musim panas**.  

📌 **Kesimpulan:**  
Dengan mengetahui adanya pengaruh musim terhadap total penggunaan sepeda, **ketersediaan sepeda dapat disesuaikan untuk tiap musimnya** agar tetap optimal.
""")


#visualiasasi analisis lanjutan
st.subheader("Distribusi Hari Berdasarkan Dominasi Pengguna")
day["rasio_casual"] = day["casual"] / day["cnt"]
median_casual = day["rasio_casual"].median()
day["cluster"] = day["rasio_casual"].apply(lambda x: "Pengguna Casual" if x > median_casual else "Pengguna Registered")

analisis_cluster = day.groupby(["weekday", "cluster"]).size().unstack()

urutan_hari = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
analisis_cluster = analisis_cluster.reindex(urutan_hari)


fig, ax = plt.subplots(figsize=(10, 5))
analisis_cluster.plot(kind="bar", stacked=True, colormap="viridis", ax=ax)
ax.set_title("Distribusi Hari Berdasarkan Dominasi Pengguna")
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Jumlah Hari")
ax.set_xticks(range(len(urutan_hari)))
ax.set_xticklabels(urutan_hari, rotation=45)
ax.legend(title="Cluster")
ax.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig)

#keterangan analisis lanjutan
st.write("### 🚴‍♂️ Persebaran Pengguna Casual dan Registered")

st.write("""
Hasil analisis menunjukkan bahwa terdapat perbedaan pola penggunaan sepeda berdasarkan hari:  

- 📅 **Weekday (Hari kerja):** Didominasi oleh **Pengguna Registered**.  
- 🏖️ **Weekend (Akhir pekan):** Didominasi oleh **Pengguna Casual**.  

📌 **Kesimpulan:**  
- **Pengguna Registered** adalah mereka yang rutin menggunakan sepeda untuk berangkat dan pulang kerja/sekolah.  
- **Untuk meningkatkan jumlah Pengguna Registered**, sepeda sebaiknya ditempatkan di dekat **gedung perkantoran dan sekolah** agar lebih mudah diakses oleh pekerja dan pelajar.  
""")
