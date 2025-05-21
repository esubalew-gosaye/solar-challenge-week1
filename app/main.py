import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Solar Radiation Dashboard")

st.title("☀️ Solar Radiation Analysis Dashboard")

# Load Data
@st.cache_data
def load_data():
    df_benin = pd.read_csv("data/cleaned/benin-malanville_clean.csv")
    df_togo = pd.read_csv("data/cleaned/togo-dapaong_qc_clean.csv")
    df_sierra = pd.read_csv("data/cleaned/sierraleone-bumbuna_clean.csv")
    
    df_benin["Country"] = "Benin"
    df_togo["Country"] = "Togo"
    df_sierra["Country"] = "Sierra Leone"
    
    return pd.concat([df_benin, df_togo, df_sierra], ignore_index=True)

df = load_data()

# Sidebar country selector
country = st.sidebar.selectbox("Select a Country", df["Country"].unique())

# Filter
df_filtered = df[df["Country"] == country]

# Summary table
st.subheader(f"📊 Summary Statistics - {country}")
st.write(df_filtered[["GHI", "DNI", "DHI"]].describe())


st.subheader("📦 Boxplots of Solar Metrics by Country")

metrics = ["GHI", "DNI", "DHI"]
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

for i, metric in enumerate(metrics):
    sns.boxplot(data=df, x="Country", y=metric, ax=axs[i], hue="Country", palette="Set2")
    axs[i].set_title(f"{metric} by Country")

st.pyplot(fig)


st.subheader("🔝 Countries Ranked by Average GHI")

avg_ghi = df.groupby("Country")["GHI"].mean().sort_values()

fig, ax = plt.subplots(figsize=(6, 4))
avg_ghi.plot(kind='barh', color='skyblue', edgecolor='black', ax=ax)
ax.set_xlabel("Average GHI (W/m²)")
ax.set_title("Average GHI by Country")

st.pyplot(fig)


st.subheader("📈 Correlation Heatmap (Radiation & Temperature)")

corr_cols = ["GHI", "DNI", "DHI", "TModA", "TModB"]
corr = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(corr, annot=True, cmap="YlGnBu", ax=ax)
st.pyplot(fig)
