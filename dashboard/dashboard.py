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

#filter berdasarkan musim
if dataset_option == "Day":
    season_option = st.sidebar.multiselect(
        "Pilih Musim:",
        options=data["season"].unique(),
        default=data["season"].unique()
    )
    data = data[data["season"].isin(season_option)]

#filter berdasarkan cuaca
weather_option = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca:",
    options=data["weathersit"].unique(),
    default=data["weathersit"].unique()
)
data = data[data["weathersit"].isin(weather_option)]

#filter berdasarkan weekday/weekend 
if dataset_option == "Hour":
    day_type = st.sidebar.radio(
        "Pilih Hari:",
        options=["Weekday", "Weekend", "Semua"],
        index=2  # Default: Semua
    )

    #daftar nama hari untuk weekday dan weekend
    weekday_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
    weekend_days = ["saturday", "sunday"]

    #filter data berdasarkan pilihan
    if day_type == "Weekday":
        data = data[data["weekday"].isin(weekday_days)]
    elif day_type == "Weekend":
        data = data[data["weekday"].isin(weekend_days)]

#filter pilih warna visualisasi
if dataset_option == "Day":
    pilih_palette = st.sidebar.selectbox("Pilih Palet Warna Suhu", ["viridis", "coolwarm"])
    
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
if dataset_option == "Hour":
    st.subheader("Tren Penggunaan Sepeda Sepanjang Hari")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=data, x='hr', y='cnt', estimator='mean', ci=None, marker='o', ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Pengguna Sepeda")
    ax.set_title("Tren Penggunaan Sepeda Sepanjang Hari (Sesuai Filter)")
    ax.set_xticks(range(0, 24))
    ax.grid()
    st.pyplot(fig)

    #keterangan pertanyaan 1
    st.write("#### ⏰ Tren Penggunaan Sepeda Sepanjang Hari")
    st.write("""
    Hasil analisis menunjukkan bahwa terdapat jam-jam tertentu di mana penggunaan sepeda meningkat secara signifikan, yaitu:  
    - **08:00** → Jam berangkat kerja/sekolah  
    - **17:00 - 18:00** → Jam pulang kerja/sekolah  
    - Pola tidak berlaku di weekend, karena tidak ada aktivitas berangkat kerja/sekolah maupun pulang kerja/sekolah
    
    📌 **Kesimpulan:**  
    Dengan mengetahui bahwa permintaan penggunaan sepeda cukup tinggi di jam tersebut, maka **ketersediaan sepeda pada jam-jam tersebut dapat lebih dioptimalkan** agar layanan tetap lancar.
    """)

#visualisasi pertanyaan 2
if dataset_option == "Day":
    st.subheader("Total Penggunaan Sepeda di Setiap Musim")
    penggunaan_per_musim = data.groupby('season')['cnt'].sum().reset_index()
    urutan_musim = ['winter', 'spring', 'summer', 'fall']
    penggunaan_per_musim['season'] = pd.Categorical(penggunaan_per_musim['season'], categories=urutan_musim, ordered=True)
    penggunaan_per_musim = penggunaan_per_musim.sort_values('season')
    warna_musim = ['blue', 'green', 'red', 'orange']
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(penggunaan_per_musim['season'], penggunaan_per_musim['cnt'], color=warna_musim)
    ax.set_title("Total Penggunaan Sepeda di Setiap Musim (Sesuai Filter)")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Pengguna Sepeda")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    #keterangan pertanyaan 2
    st.write("#### 🌦️ Pengaruh Musim terhadap Penggunaan Sepeda")
    
    st.write("""
    Hasil visualisasi menunjukkan bahwa terdapat pengaruh musim terhadap total penggunaan sepeda. 
    - 🌞 **Total penggunaan sepeda tertinggi** terjadi pada **musim panas**.
    - ❄️ **Total penggunaan sepeda terendah** terjadi pada **musim dingin**.
             
    Ini berarti **semakin hangat dan nyaman cuaca, semakin banyak orang menggunakan sepeda**. 
    Faktor lain yang mempengaruhi meningkatnya penggunaan sepeda pada musim panas mungkin dikarenakan adanya **liburan musim panas**.  
    
    📌 **Kesimpulan:** 
    Dengan mengetahui adanya pengaruh musim terhadap total penggunaan sepeda, **ketersediaan sepeda dapat disesuaikan untuk tiap musimnya** agar tetap optimal.
    """)


# #visualiasasi analisis lanjutan
#membuat kategori suhu
if dataset_option == "Day":
    bins = [0, 0.3, 0.6, 1] 
    labels = ["Dingin", "Normal", "Panas"]
    day["temp_category"] = pd.cut(day["temp"], bins=bins, labels=labels)

    #menghitung total penggunaan sepeda berdasarkan kategori suhu
    usage_by_temp = day.groupby("temp_category")["cnt"].sum().reset_index()

    st.subheader("Total Penggunaan Sepeda Berdasarkan Kategori Suhu")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="temp_category", y="cnt", data=usage_by_temp, palette=pilih_palette, ax=ax)
    ax.set_title("Total Penggunaan Sepeda Berdasarkan Kategori Suhu")
    ax.set_xlabel("Kategori Suhu")
    ax.set_ylabel("Total Pengguna Sepeda")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    #keterangan analisis lanjutan
    st.write("#### 🌡️ Analisis Penggunaan Sepeda Berdasarkan Suhu")

    st.write("""
    Hasil analisis menunjukkan adanya perbedaan jumlah penggunaan sepeda berdasarkan kategori suhu:

    - ❄️ **Dingin:** Penggunaan sepeda paling rendah.
    - 🌤️ **Normal:** Penggunaan sepeda tertinggi.
    - ☀️ **Panas:** Penggunaan sepeda masih cukup tinggi, meskipun sedikit lebih rendah dari kategori normal.

    📌 **Kesimpulan & Rekomendasi:**
    - Saat suhu dingin, persediaan sepeda dapat dikurangi atau penyedia layanan dapat memberikan **diskon** agar jumlah pengguna tetap stabil.
    - Saat suhu normal dan panas, permintaan sepeda lebih tinggi, sehingga ketersediaan sepeda harus lebih banyak untuk memenuhi kebutuhan pengguna.
    """)