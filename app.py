import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.ingestion import ingest_data
from src.db_manager import fetch_data_as_df
from src.ml_engine import ProductRatingModel

# --------------------------------------
# Page Config
# --------------------------------------
st.set_page_config(
    page_title="Urbanrise Product Analytics",
    layout="wide"
)

# --------------------------------------
# Persist ML Model
# --------------------------------------
if "ml_model" not in st.session_state:
    st.session_state.ml_model = ProductRatingModel()

# --------------------------------------
# Business Category Mapping
# --------------------------------------
CATEGORY_MAP = {
    "smartphones": "Electronics",
    "laptops": "Electronics",
    "mobile-accessories": "Electronics",

    "furniture": "Home & Living",
    "home-decoration": "Home & Living",
    "lighting": "Home & Living",

    "mens-shirts": "Fashion",
    "mens-shoes": "Fashion",
    "womens-dresses": "Fashion",
    "womens-shoes": "Fashion",

    "skincare": "Beauty",
    "fragrances": "Beauty",
    "beauty": "Beauty",

    "groceries": "Daily Essentials",
}

# Function to map category with automatic "Others"
def map_category(cat):
    return CATEGORY_MAP.get(cat, "Others")

# --------------------------------------
# Data Cleaning & Feature Engineering
# --------------------------------------
def prepare_data(df):
    df = df.copy()

    # ---- Basic Cleaning ----
    df = df[(df["rating"] >= 1) & (df["rating"] <= 5)]
    df["price"] = df["price"].clip(upper=df["price"].quantile(0.98))
    df["discountPercentage"] = df["discountPercentage"].clip(0, 80)
    df["stock"] = df["stock"].clip(lower=0)

    # ---- Category Grouping ----
    df["category_group"] = df["category"].apply(map_category)

    # ---- Business Flags ----
    df["rating_flag"] = np.where(df["rating"] >= 4, "High Rated", "Low Rated")

    df["stock_risk"] = pd.cut(
        df["stock"],
        bins=[0, 20, 50, 1000],
        labels=["Low Stock", "Normal", "Overstock"]
    )

    # ---- Price Segmentation ----
    df["price_group"] = df["price"].apply(
        lambda x: "≤ 2000 (Budget Segment)" if x <= 2000 else "> 2000 (Premium Segment)"
    )

    return df

# --------------------------------------
# Main App
# --------------------------------------
def main():
    st.title("📊 Urbanrise Product Analytics")
    st.caption("Business-focused insights using clean & meaningful visualizations")

    # ============================
    # Sidebar
    # ============================
    with st.sidebar:
        st.header("⚙️ Controls")

        if st.button("Fetch Data from API"):
            with st.spinner("Fetching data & updating MongoDB..."):
                msg = ingest_data()
            st.success(msg)

        st.divider()

        if st.button("Train Model"):
            df_raw = fetch_data_as_df()
            if df_raw.empty:
                st.error("No data available. Fetch data first.")
            else:
                df_clean = prepare_data(df_raw)
                with st.spinner("Training ML model..."):
                    status = st.session_state.ml_model.train(df_clean)
                st.success(status)

    # ============================
    # Load Data
    # ============================
    df_raw = fetch_data_as_df()
    if df_raw.empty:
        st.warning("⚠️ Please fetch data first.")
        return

    df = prepare_data(df_raw)

    tab1, tab2 = st.tabs(["📈 Business Insights", "🤖 Prediction"])

    # =====================================================
    # TAB 1: BUSINESS INSIGHTS
    # =====================================================
    with tab1:
        st.subheader("📋 Product Snapshot")
        st.dataframe(
            df[[
                "title",
                "category_group",
                "price",
                "price_group",
                "rating",
                "discountPercentage",
                "stock"
            ]].head(10),
            use_container_width=True
        )

        st.divider()

        # -------------------------------------------------
        # 1️⃣ COUNT BAR – PRICE DISTRIBUTION
        # -------------------------------------------------
        st.subheader("💰 Product Price Distribution")

        price_counts = df["price_group"].value_counts().reset_index()
        price_counts.columns = ["Price Segment", "Product Count"]

        fig_price = px.bar(
            price_counts,
            x="Price Segment",
            y="Product Count",
            title="Budget vs Premium Product Count"
        )
        st.plotly_chart(fig_price, use_container_width=True)

        # -------------------------------------------------
        # 2️⃣ SCATTER – AVG RATING VS AVG PRICE
        # -------------------------------------------------
        st.subheader("📊 Category Performance: Avg Rating vs Avg Price")

        category_summary = (
            df.groupby("category_group")
            .agg(
                avg_rating=("rating", "mean"),
                avg_price=("price", "mean"),
                product_count=("title", "count")
            )
            .reset_index()
        )

        fig_category_perf = px.scatter(
            category_summary,
            x="avg_rating",
            y="avg_price",
            size="product_count",
            color="category_group",
            hover_data=["avg_rating", "avg_price", "product_count"],
            title="Average Rating vs Average Price by Business Category",
        )

        st.plotly_chart(fig_category_perf, use_container_width=True)

        # -------------------------------------------------
        # 3️⃣ PIE – INVENTORY RISK
        # -------------------------------------------------
        st.subheader("📦 Inventory Risk Composition")

        stock_dist = df["stock_risk"].value_counts().reset_index()
        stock_dist.columns = ["Stock Risk", "Count"]

        fig_stock = px.pie(
            stock_dist,
            names="Stock Risk",
            values="Count",
            title="Inventory Risk Split"
        )
        st.plotly_chart(fig_stock, use_container_width=True)

        # -------------------------------------------------
        # 4️⃣ BOX PLOT – DISCOUNT DISCIPLINE
        # -------------------------------------------------
        st.subheader("🎯 Discount Strategy Discipline")

        fig_discount = px.box(
            df,
            x="category_group",
            y="discountPercentage",
            title="Discount Distribution by Business Category"
        )
        st.plotly_chart(fig_discount, use_container_width=True)

        # -------------------------------------------------
        # 5️⃣ PIE – HIGH RATED PRODUCTS BY CATEGORY
        # -------------------------------------------------
        st.subheader("🥇 High Rated Products Contribution by Category")

        # Aggregate high-rated product counts only
        category_perf = df.groupby("category_group").agg(
            high_rated_count=("rating_flag", lambda x: (x == "High Rated").sum())
        ).reset_index()

        fig_high_rated_pie = px.pie(
            category_perf,
            names="category_group",
            values="high_rated_count",
            title="High Rated Products Contribution by Category",
            labels={"high_rated_count": "High Rated Products", "category_group": "Category"}
        )

        st.plotly_chart(fig_high_rated_pie, use_container_width=True)

    # =====================================================
    # TAB 2: PREDICTION
    # =====================================================
    with tab2:
        st.subheader("🔮 Predict Product Rating Quality")

        if st.session_state.ml_model.accuracy is None:
            st.warning("Please train the model first.")
            return

        st.success(f"Model Accuracy: {st.session_state.ml_model.accuracy:.2f}")

        c1, c2, c3 = st.columns(3)
        with c1:
            in_price = st.number_input("Price", min_value=0.0, value=1500.0)
        with c2:
            in_discount = st.number_input("Discount %", 0.0, 80.0, 10.0)
        with c3:
            in_stock = st.number_input("Stock", min_value=0, value=30)

        if st.button("Predict"):
            label, prob = st.session_state.ml_model.predict(
                in_price, in_discount, in_stock
            )
            st.metric("Prediction", label)
            st.progress(prob, text=f"Confidence: {prob:.2%}")

# --------------------------------------
# Run App
# --------------------------------------
if __name__ == "__main__":
    main()
