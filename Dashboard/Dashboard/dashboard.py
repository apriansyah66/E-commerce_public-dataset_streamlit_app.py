import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi gaya seaborn
sns.set_style("whitegrid")

# Judul aplikasi
st.title("📊 Dashboard Analisis Pelanggan & Review")

# Sidebar untuk navigasi
st.sidebar.header("📌 Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Analisis Pelanggan", "Analisis Review"])

# Upload file dataset (opsional)
st.sidebar.subheader("📂 Upload Dataset (Opsional)")
customer_file = st.sidebar.file_uploader("Upload File Customers", type=["csv"])
review_file = st.sidebar.file_uploader("Upload File Reviews", type=["csv"])

# Jika tidak diupload, gunakan default
if not customer_file:
    customer_file = "customers_dataset.csv"
if not review_file:
    review_file = "order_reviews_dataset.csv"

try:
    # Membaca dataset
    df_customers = pd.read_csv(customer_file)
    df_reviews = pd.read_csv(review_file)

    if page == "Analisis Pelanggan":
        # ---- Analisis Pelanggan ----
        st.header("🏙 Analisis Pelanggan Berdasarkan Kota")

        # Menghitung jumlah pelanggan per kota
        city_counts = df_customers['customer_city'].value_counts()

        # Kota dengan jumlah pelanggan terbanyak
        most_common_city = city_counts.idxmax()
        most_common_count = city_counts.max()

        # Menampilkan daftar 10 kota dengan pelanggan terbanyak
        st.subheader("🔝 Top 10 Kota dengan Pelanggan Terbanyak")
        st.write(city_counts.head(10))

        # Menampilkan informasi kota dengan pelanggan terbanyak
        st.success(f"Customer terbanyak ada pada kota *{most_common_city}* dengan jumlah *{most_common_count}* pelanggan.")

        # Membuat diagram batang interaktif pelanggan
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=city_counts.head(10).index, y=city_counts.head(10).values, palette="Blues_r", ax=ax)
        ax.set_title("Top 10 Kota dengan Jumlah Pelanggan Terbanyak", fontsize=14)
        ax.set_xlabel("Kota", fontsize=12)
        ax.set_ylabel("Jumlah Pelanggan", fontsize=12)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # ---- Tambahan: Visualisasi Jumlah Pelanggan Unik ----
        if "customer_unique_id" in df_customers.columns:
            jumlah_pelanggan_unik = df_customers["customer_unique_id"].nunique()
            st.subheader("📊 Jumlah Pelanggan Unik")
            
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.bar(["Pelanggan Unik"], [jumlah_pelanggan_unik], color='skyblue')
            ax.set_ylabel("Jumlah")
            ax.set_title("Jumlah Pelanggan Unik dalam Dataset")
            ax.text(0, jumlah_pelanggan_unik, str(jumlah_pelanggan_unik), ha='center', va='bottom', fontsize=12)
            st.pyplot(fig)
            
            st.success(f"Jumlah pelanggan unik dalam dataset: **{jumlah_pelanggan_unik}**")
    
    elif page == "Analisis Review":
        # ---- Analisis Review ----
        st.header("⭐ Analisis Review")

        if 'review_score' in df_reviews.columns:
            # Filter skor review dengan slider
            min_score, max_score = st.sidebar.slider("Filter Review Score", 1, 5, (1, 3))
            filtered_reviews = df_reviews[df_reviews['review_score'].between(min_score, max_score)]
            review_counts = filtered_reviews['review_score'].value_counts().sort_index()

            # Menampilkan jumlah review berdasarkan filter
            st.subheader(f"📌 Statistik Review (Skor {min_score}-{max_score})")
            st.write(f"Total jumlah review dengan skor *{min_score}-{max_score}: **{filtered_reviews.shape[0]}*")

            # Menampilkan distribusi skor dalam tabel
            st.write("📊 *Distribusi Review:*")
            st.table(review_counts)

            # Membuat diagram batang interaktif review
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=review_counts.index, y=review_counts.values, palette="coolwarm", ax=ax)
            ax.set_title(f"Distribusi Review Skor {min_score}-{max_score}", fontsize=14)
            ax.set_xlabel("Skor Review", fontsize=12)
            ax.set_ylabel("Jumlah Review", fontsize=12)
            st.pyplot(fig)

        else:
            st.error("Kolom 'review_score' tidak ditemukan dalam dataset.")

except FileNotFoundError:
    st.error("Salah satu file dataset tidak ditemukan. Pastikan dataset tersedia di folder yang benar.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
