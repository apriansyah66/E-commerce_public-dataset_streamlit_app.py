import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🏆 Dashboard Title
st.title("🚴‍♂️ Bike Sharing Data Analysis ")
st.subheader("Dataset: Bike Sharing Dataset")
st.text("📅 2011/01/01 – 2012/12/31")

# 📌 Load Dataset
def load_data():
    day_df = pd.read_csv("dashboard/main_data.csv")  # Ganti dengan path dataset Anda
    return day_df

day_df = load_data()

# ⏳ Konversi kolom tanggal
day_df["dateday"] = pd.to_datetime(day_df["dateday"])
day_df.sort_values(by="dateday", inplace=True)
day_df.reset_index(drop=True, inplace=True)

# 📆 Sidebar: Filter data berdasarkan tanggal
min_date, max_date = day_df["dateday"].min(), day_df["dateday"].max()

with st.sidebar:
    try:
        start_date, end_date = st.date_input(
            "📅 Pilih Rentang Waktu:",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
        # 🔹 Filter dataset berdasarkan rentang tanggal yang dipilih
        day_df = day_df[(day_df["dateday"] >= str(start_date)) & (day_df["dateday"] <= str(end_date))]
    except Exception as e:
        st.warning(f"⚠️ Terjadi kesalahan pada pemilihan tanggal: {e}")

# 🔹 Filter dataset berdasarkan rentang tanggal yang dipilih
day_df = day_df[(day_df["dateday"] >= str(start_date)) & (day_df["dateday"] <= str(end_date))]

# 📊 Perbandingan Total Penyewaan per Tahun
st.subheader("📊 Perbandingan Jumlah Penyewaan Sepeda per Tahun")

yearly_counts = day_df.groupby("year", observed=False)["count"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=yearly_counts, x="year", y="count", palette="Set2", ax=ax)

# Menambahkan angka di atas batang
for p in ax.patches:
    ax.annotate(f"{int(p.get_height()):,}", 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12, fontweight="bold",
                xytext=(0, 1), textcoords='offset points')

ax.set_title("Total Penyewaan Sepeda per Tahun", fontsize=14, fontweight="bold")
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)

# 📌 Analisis Berdasarkan Kategori Pengguna
st.subheader("📈 Analisis Penyewaan Sepeda Berdasarkan Kategori Pengguna")

# 🔎 Agregasi data berdasarkan tahun
annual_result = day_df.groupby("year", observed=False).agg({
    "registered": ["sum"],
    "casual": ["sum"]
}).reset_index()

# 🟢 Pilihan kategori pengguna (Diberi `key` unik)
selected_category = st.selectbox(
    "Pilih Kategori Pengguna:", 
    ["registered", "casual"], 
    index=0, 
    key="user_category_selectbox"
)

# Menyesuaikan data berdasarkan pilihan pengguna
category_data = annual_result[("registered", "sum")] if selected_category == "Registered" else annual_result[("casual", "sum")]

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=annual_result["year"], y=category_data, palette="Set2", ax=ax)

# Menambahkan angka di atas batang
for i, v in enumerate(category_data):
    ax.text(i, v + 5000, f"{v:,.0f}", ha="center", fontsize=12, fontweight="bold")

ax.set_title(f"Penyewaan Sepeda ({selected_category.capitalize()}) per Tahun", fontsize=14, fontweight="bold")
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
st.pyplot(fig)

# 📌 Perbandingan Penyewaan Sepeda Berdasarkan Musim
st.subheader("❄️☀️ Perbandingan Penyewaan Sepeda Berdasarkan Musim")

seasonal_year_counts = day_df.groupby(["year", "season"], observed=False).agg({
    "count": "sum"
}).reset_index()

# 🟢 Pilih musim (Diberi `key` unik)
selected_season = st.selectbox(
    "Pilih Musim:", 
    ["Spring", "Summer", "Fall", "Winter"], 
    key="season_selectbox"
)

# Filter data berdasarkan musim
filtered_data = seasonal_year_counts[seasonal_year_counts["season"] == selected_season]

if filtered_data.empty:
    st.warning(f"⚠️ Tidak ada data untuk musim {selected_season}. Coba pilih musim lain.")
else:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=filtered_data, x="season", y="count", hue="year", palette="Set2", ax=ax)

    # Menambahkan angka pada batang
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}',
                    (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='center', fontsize=10, color='black',
                    xytext=(0, 3), textcoords='offset points')

    ax.set_title(f"Jumlah Penyewaan Sepeda di Musim {selected_season}", fontsize=12, fontweight="bold")
    ax.set_xlabel("Musim", fontsize=10)
    ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=10)
    st.pyplot(fig)

# 📌 Perbandingan Penyewaan Sepeda Berdasarkan Hari Kerja
st.subheader("📅 Perbandingan Penyewaan Sepeda Berdasarkan Hari Kerja")

weekday_comparison = day_df.groupby(["year", "weekday"], observed=False).agg({
    "count": "sum"
}).reset_index()

fig, ax = plt.subplots(figsize=(14, 8))
sns.barplot(data=weekday_comparison, x="weekday", y="count", hue="year", palette="Set2", width=0.85, ax=ax)

# Menambahkan angka di atas batang
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=12, fontweight="bold",
                xytext=(0, 3), textcoords='offset points')

ax.set_title("Perbandingan Penyewaan Sepeda Berdasarkan Hari Kerja", fontsize=16)
ax.set_xlabel("Hari", fontsize=14)
ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=14)
st.pyplot(fig)

# 📌 Diagram Lingkaran Penyewaan pada Hari Kerja vs Libur
st.subheader("📅 Perbandingan Penyewaan Sepeda: Hari Kerja vs Libur")

workingday_comparison = day_df.groupby(["year", "workingday"], observed=False).agg({
    "count": "sum"
}).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
colors = sns.color_palette("Set2", n_colors=2)

for i, year in enumerate(workingday_comparison["year"].unique()):
    data_year = workingday_comparison[workingday_comparison["year"] == year]
    axes[i].pie(data_year["count"], labels=["Non-Working Day", "Working Day"], autopct='%1.1f%%', startangle=90, colors=colors)
    axes[i].set_title(f"Penyewaan Sepeda Tahun {year}")

st.pyplot(fig)
