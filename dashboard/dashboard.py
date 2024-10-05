import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import datetime
sns.set(style='dark')

colors = ('#8B4513', '#FFF8DC', '#93C572', '#E67F0D')

# import data excel
data = pd.read_csv("main_data.csv")

# rename kolom dan hapus kolom yang tidak perlu ditampilkan
data.rename(columns={
    "dteday": "Date",
    "cnt": "total",
    "instant": "id",
}, inplace=True)
data.drop("yr", axis=1, inplace=True)


# mengurutkan DataFrame berdasarkan dteday serta memastikan kolom tersebut bertipe datetime.
datetime_columns = ["Date"]
data.sort_values(by="Date", inplace=True)
data.reset_index(inplace=True)

for column in datetime_columns:
    data[column] = pd.to_datetime(data[column])

# membuat component sort
min_date = data["Date"].min()
max_date = data["Date"].max()
 
with st.sidebar:
    
    st.text('Filter by')
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = data[(data["Date"] >= str(start_date)) & 
                (data["Date"] <= str(end_date))]

st.title('Bike Sharing List')
st.subheader("All List")
st.dataframe(main_df)

st.subheader('Daily Shared Bikes')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_bike = data.total.sum()
    st.metric("Total Bike Shared", value=total_bike)
 
with col2:
    total_casual = data.casual.sum()
    st.metric("Total Casual Bike", value=total_casual)

with col3:
    total_registered = data.registered.sum()
    st.metric("Total Registered Bike", value=total_registered)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    data["Date"],
    data["total"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader('By Season')

byseason_df = data.groupby(by="season").agg({
    "total": "sum",
    "casual": "sum",
    "registered": "sum",
})

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="total", 
    x="season",
    data=byseason_df.sort_values(by="total", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Total Bike Sharing Per-Season", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)


st.subheader("Based on Bike Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_season = round(byseason_df.total.mean(), 1)
    st.metric("Average Total Bike (days)", value=avg_season)
 
with col2:
    avg_casual = round(byseason_df.casual.mean(), 2)
    st.metric("Average Casual Bike", value=avg_casual)
 
with col3:
    avg_registered = round(byseason_df.registered.mean(), 3) 
    st.metric("Average Registered Bike", value=avg_registered)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(y="total", x="season", data=byseason_df.sort_values(by="total", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("season", fontsize=30)
ax[0].set_title("Total Bike", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="casual", x="season", data=byseason_df.sort_values(by="casual", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("season", fontsize=30)
ax[1].set_title("Casual Bike", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="registered", x="season", data=byseason_df.sort_values(by="registered", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("season", fontsize=30)
ax[2].set_title("Registered", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)



