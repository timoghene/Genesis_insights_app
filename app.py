import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Setting the general style as white & page layout to wide
sns.set(style="whitegrid")
st.set_page_config(layout="wide")

# Formatting money values
def format_naira(x):
    return f"₦{x:,.0f}"

st.title("Genesis Insights Dashboard 📊")

# Uploaders for CSV files
st.sidebar.header("📂 Upload Your CSV Files")
uploaded_orders = st.sidebar.file_uploader("Upload CSV-1", type=["csv"])
uploaded_products = st.sidebar.file_uploader("Upload CSV-2", type=["csv"])

# Load data based on upload or default
if uploaded_orders:
    orders_df = pd.read_csv(uploaded_orders, parse_dates=["date"])
    st.sidebar.success("✅ CSV loaded successfully!")
else:
    orders_df = pd.read_csv("filtered_summary_a.csv", parse_dates=["date"])

if uploaded_products:
    products_df = pd.read_csv(uploaded_products)
    st.sidebar.success("✅ CSV loaded successfully!")
else:
    products_df = pd.read_csv("product_counts.csv")


# Tabs for each insight
tabs = st.tabs([
    "1️⃣ Peak Order Times",
    "2️⃣ Most Ordered Items",
    "3️⃣ Revenue by Channel",
    "4️⃣ Location Performance",
    "5️⃣ Average Order Value (AOV)",
    "6️⃣ Pickup vs Delivery"
])

# ------------------------------- 
# 1. Peak Order Times
# ------------------------------- 
with tabs[0]:
    st.header("Peak Order Times – Busiest Hours and Days")
    col1, col2 = st.columns(2)

    # Orders by Hour
    with col1:
        orders_by_hour = orders_df["time"].str[:2].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=orders_by_hour.index, y=orders_by_hour.values, ax=ax, palette="viridis")
        ax.set_title("Orders by Hour")
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Number of Orders")
        st.pyplot(fig)

    # Orders by Day of Week
    with col2:
        orders_by_day = orders_df["day_of_week"].value_counts().reindex([
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=orders_by_day.index, y=orders_by_day.values, ax=ax, palette="Set2")
        ax.set_title("Orders by Day of the Week")
        ax.set_ylabel("Number of Orders")
        ax.set_xlabel("Day")
        st.pyplot(fig)

# ------------------------------- 
# 2. Most Ordered Items
# ------------------------------- 
with tabs[1]:
    st.header("Most Ordered Items")
    top_n = st.slider("Select number of top items to display:", 5, 30, 10)

    top_items = products_df.sort_values("Order Count", ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y="Product Name", x="Order Count", data=top_items, palette="Blues_r", ax=ax)
    ax.set_title(f"Top {top_n} Most Ordered Products")
    st.pyplot(fig)

# ------------------------------- 
#  3. Revenue by Channel
# ------------------------------- 
with tabs[2]:
    st.header(" Revenue by Order Source (Mobile vs Website)")

    # Revenue
    platform_rev = orders_df.groupby("platform")["Total Amount"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(8, 4))
    platform_rev.plot(kind="barh", ax=ax, color="coral")
    ax.set_title("Revenue by Platform")
    ax.bar_label(ax.containers[0], fmt=lambda x: format_naira(x))
    st.pyplot(fig)

    # Orders
    platform_orders = orders_df["platform"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=platform_orders.index, y=platform_orders.values, palette="muted", ax=ax)
    ax.set_title("Order Count by Platform")
    st.pyplot(fig)

# ------------------------------- 
#  4. Location Performance
# ------------------------------- 
with tabs[3]:
    st.header(" Revenue & AOV by Outlet Location")
    col1, col2 = st.columns(2)

    # Total Revenue by Outlet
    with col1:
        outlet_rev = orders_df.groupby("Outlet Name")["Total Amount"].sum().sort_values()
        fig, ax = plt.subplots(figsize=(9, 5))
        outlet_rev.plot(kind="barh", ax=ax, color="teal")
        ax.set_title("Total Revenue by Outlet")
        ax.bar_label(ax.containers[0], fmt=lambda x: format_naira(x))
        st.pyplot(fig)

    # Orders by Outlet
    with col2:
        outlet_orders = orders_df["Outlet Name"].value_counts()
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(y=outlet_orders.index, x=outlet_orders.values, palette="Set3", ax=ax)
        ax.set_title("Order Count by Outlet")
        st.pyplot(fig)

    # AOV by Outlet
    outlet_aov = orders_df.groupby("Outlet Name")["Total Amount"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, 5))
    outlet_aov.plot(kind="barh", color="orange", ax=ax)
    ax.set_title("Average Order Value (AOV) by Outlet")
    ax.bar_label(ax.containers[0], fmt=lambda x: format_naira(x))
    st.pyplot(fig)

# ------------------------------- 
# 5. Average Order Value (AOV)
# ------------------------------- 
with tabs[4]:
    st.header("Average Order Value (AOV) Insights")

    # AOV by Platform
    platform_aov = orders_df.groupby("platform")["Total Amount"].mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    platform_aov.plot(kind="bar", ax=ax, color="orchid")
    ax.set_title("Average Order Value by Platform")
    ax.bar_label(ax.containers[0], fmt=lambda x: format_naira(x))
    st.pyplot(fig)

    # AOV by Outlet
    outlet_aov = orders_df.groupby("Outlet Name")["Total Amount"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(10, 5))
    outlet_aov.plot(kind="barh", ax=ax, color="steelblue")
    ax.set_title("AOV by Outlet")
    ax.bar_label(ax.containers[0], fmt=lambda x: format_naira(x))
    st.pyplot(fig)

# ------------------------------- 
# 6. Pickup vs Delivery
# ------------------------------- 
with tabs[5]:
    st.header("Pickup vs Delivery Trends")

    # Revenue by Delivery Type
    del_rev = orders_df.groupby("Delivery Type")["Total Amount"].sum()
    fig, ax = plt.subplots(figsize=(8, 4))
    del_rev.plot(kind="bar", ax=ax, color="limegreen")
    ax.set_title("Total Revenue by Delivery Type")
    ax.bar_label(ax.containers[0], fmt=lambda x: format_naira(x))
    st.pyplot(fig)

    # Orders by Delivery Type
    del_orders = orders_df["Delivery Type"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=del_orders.index, y=del_orders.values, palette="coolwarm", ax=ax)
    ax.set_title("Order Count by Delivery Type")
    st.pyplot(fig)
        
    # Formatted using pandas plot with markers, grid, and custom styling
    trend = orders_df.groupby(["date", "Delivery Type"]).size().unstack(fill_value=0)
    plt.figure(figsize=(12, 6))
    trend.plot(kind='line', marker='o', figsize=(12, 6))
    plt.xlabel("Date")
    plt.ylabel("Number of Orders")
    plt.title("Pickup vs. Delivery Trends Over Time")
    plt.legend(title="Delivery Type")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())


