import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
# import matplotlib.pyplot as plt


df = pd.read_csv("jiji_electronics_2.csv", index_col=0)

df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

st.set_page_config(page_title="Jiji Electronics Insights", layout="centered")


st.markdown("""
    <style>
        body { background-color: #0d0d0d; color: #FFD700; }
        .stApp { background-color:#0d0d0d; color: #FFD700;  }
        .sidebar .sidebar-content { background-color: #FFD700; color: #1a1a1a; }
        h1, h2, h3, h4, h5, h6 { color: #FFD700; }
        .stTabs [role="tablist"] button {color: #FFD700; }
        .stTabs [role="tablist"] button[aria-selected="true"] { color: white; }
        write { font-size: 60px; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)


st.sidebar.title("Insights & Analysis")
analysis_choice = st.sidebar.radio(
    "Select an option",
    [   "Home",
        "Data Analysis",
        "Insights and Reccommendations"
    ]
)



if analysis_choice == "Home":
    st.image("laptop.jpg", width=150) 
    st.title("Jiji Electronics Overview")

# Cards
    total_products = len(df)
    total_categories = df["Category"].nunique()
    total_brands = df["Brand"].nunique()
    avg_price = df["Price"].mean().round(2)

    highest_priced_item = df.loc[df["Price"].idxmax()]
    top_category = df["Category"].value_counts().idxmax()
    top_city = df["City"].value_counts().idxmax()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Products", f"{total_products:,}")
    kpi2.metric("Unique Categories", total_categories)
    kpi3.metric("Unique Brands", total_brands)
    kpi4.metric("Avg Price (₦)", f"{avg_price:,.0f}")

    st.subheader("🔥 Highlights")
    st.write(f"""
    - 💡 **Highest Priced Product:** {highest_priced_item['Title']}  
      *(₦{highest_priced_item['Price']:,.0f}, {highest_priced_item['Category']}, {highest_priced_item['City']})*  
    - 🏆 **Most Popular Category:** {top_category}  
    - 📍 **Top City by Listings:** {top_city}  
    """)

    st.write("Here's the full dataset")
    st.dataframe(df) 
    

elif analysis_choice == "Data Analysis":

    st.title("Jiji Electronics Analysis")

    st.header("Price Dynamics")
    st.write("Average, Median, and Range of prices across categories.")

    # Calculate stats
    price_stats = df.groupby("Category")["Price"].agg(
        Average="mean",
        Median="median",
        Min="min",
        Max="max"
    ).reset_index()

    # Add explicit Range column
    price_stats["Range"] = price_stats["Max"] - price_stats["Min"]

    # Round for nicer display
    price_stats[["Average", "Median", "Min", "Max", "Range"]] = (
        price_stats[["Average", "Median", "Min", "Max", "Range"]].round(2)
    )

    with st.expander("Price Statistics Table"):
        st.dataframe(price_stats)

    price_summary = df.groupby("Category")["Price"].agg(["mean"]).reset_index()
    fig = px.bar(
        price_summary,
        x="Category",
        y="mean",
        color="Category",
        title="Average Price by Category"
    )
    st.plotly_chart(fig, use_container_width=True)


        
    st.header("Geographic Concentration")
    st.write("Top states and cities with the highest number of listings.")

    tab1, tab2 = st.tabs(["By State", "By City"])

    with tab1:
        state_counts = df["Location"].value_counts().head(10).reset_index()
        state_counts.columns = ["State", "Count"]
        fig1 = px.bar(
            state_counts,
            x="Count",
            y="State",
            orientation="h",
            title="Top States with Most Listings",
            color="Count"
        )
        fig1.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        city_counts = df["City"].value_counts().head(10).reset_index()
        city_counts.columns = ["City", "Count"]
        fig2 = px.bar(
            city_counts,
            x="Count",
            y="City",
            orientation="h",
            title="Top Cities with Most Listings",
            color="Count"
        )
        fig2.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig2, use_container_width=True)



    st.header("Category Dominance")
    st.write("Which categories dominate listings?")

    cat_counts = df["Category"].value_counts()
    fig = px.bar(cat_counts, y=cat_counts.values, x=cat_counts.index,
                 title="Category Share of Listings")
    st.plotly_chart(fig, use_container_width=True)



    st.subheader("Condition of items across categories.")

    cond_counts = df["Condition"].value_counts(dropna=True)
    fig = px.pie(values=cond_counts.values, names=cond_counts.index,
                 title="Overall Condition Distribution")
    st.plotly_chart(fig, use_container_width=True)



    st.header("Brand Popularity")
    st.write("Most popular brands within categories.")

    brand_counts = df["Brand"].value_counts().head(15).reset_index()
    brand_counts.columns = ["Brand", "Count"]

    fig = px.treemap(
        brand_counts,
        path=["Brand"],
        values="Count",
        title="Top 15 Brands by Listings"
    )
    st.plotly_chart(fig, use_container_width=True)


    st.header("Regional Price Variations")
    st.write("Price differences across states and cities.")

    tab1, tab2 = st.tabs(["By State", "By City"])

    with tab1:
        state_price = df.groupby("Location")["Price"].mean().sort_values(ascending=False).head(10)
        fig1 = px.bar(state_price, x=state_price.index, y=state_price.values,
                      title="Average Prices by State", color=state_price.values)
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        city_price = df.groupby("City")["Price"].mean().sort_values(ascending=False).head(10)
        fig2 = px.bar(city_price, x=city_price.index, y=city_price.values,
                      title="Average Prices by City", color=city_price.values)
        st.plotly_chart(fig2, use_container_width=True)


elif analysis_choice == "Insights and Reccommendations":
    st.header("Insights")
    st.write("""
    1. **Price Dynamics** - Premium categories (e.g., *Laptops & Computers*) show high average/median prices, while accessories and smaller gadgets stay on the low end.  
    2. **Geographic Concentration** - Lagos is by far the largest hub, especially Ikeja and Ojodu. Oyo and Ogun follow but at smaller scales.  
    3. **Category Dominance** - Laptops & Computers account for the biggest share of listings, signaling strong demand.  
    4. **Condition Distribution** - Used items dominate the market, meaning resale is a major driver.  
    5. **Brand Popularity** - HP, Dell, and Apple dominate laptops; Samsung dominates phones; unknown brands flood accessories.  
    6. **Regional Price Variations** - Lagos cities (Ikeja, Lekki) show significantly higher prices for the same categories than other states, reflecting stronger purchasing power.  

    """)
    st.header("Recommendations")
    st.write("""
    1. **Target Hotspots** - Focus ads and promotions in Lagos, especially Ikeja (tech hub), since that's where listings cluster.  
    2. **Niche Expansion** - Push underrepresented but in-demand brands (Lenovo, Asus) to capture a less competitive niche.  
    3. **Trust Building** - Since used items dominate, offering warranties/after-sales support can make you stand out.  
    4. **Smart Pricing** - Align product pricing with regional dynamics (premium pricing in Lekki/Ikeja, budget focus in Ibadan or Ojo).  
    5. **Category Focus** - Double down on laptops and phones; experiment with security gadgets as they show growing presence.  
    6. **Data-Driven Inventory** - Stock more of what performs in Lagos hubs, and test markets outside Lagos for growth.  
    """)
