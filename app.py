import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Diwali Sales Data Analytics",
    page_icon="🛍️",
    layout="wide"
)

# Title & Description
st.title("🛍️ Diwali Sales Data Analytics Dashboard")
st.markdown("Interactive exploratory data analysis on customer purchasing behavior during Diwali.")

# Load and Clean Data
@st.cache_data
def load_and_clean_data():
    # Load dataset
    df = pd.read_csv('Diwali Sales Data.csv', encoding='unicode_escape')
    
    # Drop empty/unrelated columns if present
    cols_to_drop = [col for col in ['Status', 'unnamed1'] if col in df.columns]
    if cols_to_drop:
        df.drop(columns=cols_to_drop, inplace=True)
        
    # Handle missing values and types
    df.dropna(inplace=True)
    df['Amount'] = df['Amount'].astype(int)
    
    return df

try:
    df = load_and_clean_data()
    
    # Sidebar Filters
    st.sidebar.header("Filter Options")
    
    zone_filter = st.sidebar.multiselect(
        "Select Zone:",
        options=df["Zone"].unique(),
        default=df["Zone"].unique()
    )
    
    gender_filter = st.sidebar.multiselect(
        "Select Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )
    
    age_filter = st.sidebar.multiselect(
        "Select Age Group:",
        options=sorted(df["Age Group"].unique()),
        default=sorted(df["Age Group"].unique())
    )

    # Apply Filters
    filtered_df = df[
        (df["Zone"].isin(zone_filter)) &
        (df["Gender"].isin(gender_filter)) &
        (df["Age Group"].isin(age_filter))
    ]

    # Key Performance Indicators (KPIs)
    total_sales = filtered_df["Amount"].sum()
    total_orders = filtered_df["Orders"].sum()
    total_customers = filtered_df["User_ID"].nunique()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₹{total_sales:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Unique Customers", f"{total_customers:,}")
    col4.metric("Avg Spend per Order", f"₹{avg_order_value:,.2f}")

    st.markdown("---")

    # Visualizations Row 1
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Sales Amount by Gender")
        gender_sales = filtered_df.groupby("Gender", as_index=False)["Amount"].sum()
        fig_gender = px.bar(
            gender_sales, 
            x="Gender", 
            y="Amount", 
            color="Gender",
            text_auto='.2s',
            labels={"Amount": "Total Sales (₹)"},
            color_discrete_map={'F': '#E91E63', 'M': '#2196F3'}
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    with row1_col2:
        st.subheader("Sales by Age Group & Gender")
        age_gender_sales = filtered_df.groupby(["Age Group", "Gender"], as_index=False)["Amount"].sum()
        fig_age = px.bar(
            age_gender_sales, 
            x="Age Group", 
            y="Amount", 
            color="Gender", 
            barmode="group",
            labels={"Amount": "Total Sales (₹)"},
            color_discrete_map={'F': '#E91E63', 'M': '#2196F3'}
        )
        st.plotly_chart(fig_age, use_container_width=True)

    # Visualizations Row 2
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("Top 10 States by Total Sales")
        state_sales = filtered_df.groupby("State", as_index=False)["Amount"].sum().sort_values(by="Amount", ascending=False).head(10)
        fig_state = px.bar(
            state_sales, 
            x="Amount", 
            y="State", 
            orientation="h",
            labels={"Amount": "Total Sales (₹)"},
            color="Amount",
            color_continuous_scale="Viridis"
        )
        fig_state.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_state, use_container_width=True)

    with row2_col2:
        st.subheader("Sales by Product Category")
        cat_sales = filtered_df.groupby("Product_Category", as_index=False)["Amount"].sum().sort_values(by="Amount", ascending=False).head(10)
        fig_cat = px.bar(
            cat_sales, 
            x="Product_Category", 
            y="Amount",
            labels={"Amount": "Total Sales (₹)", "Product_Category": "Category"},
            color="Amount",
            color_continuous_scale="Plasma"
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # Visualizations Row 3
    st.subheader("Sales Distribution by Customer Occupation")
    occ_sales = filtered_df.groupby("Occupation", as_index=False)["Amount"].sum().sort_values(by="Amount", ascending=False)
    fig_occ = px.bar(
        occ_sales, 
        x="Occupation", 
        y="Amount", 
        color="Occupation",
        labels={"Amount": "Total Sales (₹)"}
    )
    st.plotly_chart(fig_occ, use_container_width=True)

    # Filtered Data Table View
    with st.expander("🔍 View Raw Filtered Data"):
        st.dataframe(filtered_df)

except FileNotFoundError:
    st.error("Error: 'Diwali Sales Data.csv' file not found. Please place the CSV file in the same directory as this script.")