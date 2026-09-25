# ============================================================
# Brain Cancer Public Health Dashboard
# Data source: NHS England / NDRS Cancer Registration Statistics
# Data period: 2013–2022
# Built using Python, Pandas, Plotly and Streamlit
# ============================================================


import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
df = pd.read_csv("data/brain_cancer.csv")

# Clean spaces from column names
df.columns = df.columns.str.strip()
# Convert the rate column to numbers
df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce")


# Title
st.title("Brain Cancer Incidence in England")
st.caption("NHS England cancer registration data | 2013–2022")

st.write(
    "This project demonstrates how public health data can be explored, "
    "analysed and communicated using Python and Streamlit."
)


# Introduction
st.write(
    "This dashboard explores brain cancer incidence across England "
    "from 2013 to 2022 using NHS England cancer registration data."
)
# Definitions and methodology
with st.expander("Definitions & methodology"):

    st.markdown("""
    ### What does the incidence rate mean?

    The incidence rate describes the number of new brain cancer cases
    occurring in a population over a given period of time.

    This dashboard uses **age-standardised incidence rates**.
    Age-standardisation allows cancer incidence to be compared between
    populations with different age structures.

    ### What data is being used?

    The data comes from the **NHS England National Disease Registration
    Service (NDRS)** Cancer Registration Statistics.

    The dashboard uses data from **2013 to 2022** and focuses on:

    - Brain cancer
    - All ages
    - All stages
    - All deprivation quintiles
    - Government Office Regions
    - Age-standardised rates

    ### Confidence intervals

    The table includes **95% confidence intervals** around the incidence
    rate. These provide an indication of the uncertainty around the
    estimated rate.

    ### Important limitation

    The dataset contains regional data rather than a separate
    England-wide incidence rate. Therefore, the dashboard does not
    present the average of regional rates as an official England
    incidence rate.

    The regional overview is shown as the average of the available
    regional age-standardised rates and is intended for visual
    comparison only.

    ### Data source

    NHS England - National Disease Registration Service (NDRS),
    Cancer Registration Statistics.

    For more information, visit the
    [NHS England Cancer Registration Statistics](https://digital.nhs.uk/ndrs/data/data-outputs/cancer-data-hub/cancer-registration-statistics)
    """)


# Select the data we want to analyse
filtered_df = df[
    (df["Type of rate"] == "Age-standardised") &
    (df["Age at diagnosis"] == "All ages") &
    (df["Geography type"] == "Government Office Region") &
    (df["Stage"] == "All stages") &
    (df["Deprivation"] == "All quintiles") &
    (df["NDRS main"] == "Brain") &
    (df["NDRS detailed"] == "All Brain")
]

# Dashboard filters
st.sidebar.header("Dashboard filters")

gender = st.sidebar.selectbox(
    "Select gender:",
    ["Females", "Males"]
)

region = st.sidebar.selectbox(
    "Select region:",
    sorted(filtered_df["Geography name"].unique())
)

year = st.sidebar.selectbox(
    "Select year for regional comparison:",
    sorted(filtered_df["Year"].unique(), reverse=True)
)



# Filter the data based on the selections
selected_df = filtered_df[
    (filtered_df["Gender"] == gender) &
    (filtered_df["Geography name"] == region)
]

# Create the graph
fig = px.line(
    selected_df,
    x="Year",
    y="Rate",
    markers=True,
    title=f"Brain Cancer Incidence — {region} ({gender})",
    labels={
        "Year": "Year",
        "Rate": "Age-standardised incidence rate"
    }
)

# Label the axes
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Age-standardised incidence rate"
)

# Display the graph
st.plotly_chart(fig, use_container_width=True)
# Regional comparison for selected year
comparison_df = filtered_df[
    (filtered_df["Gender"] == gender) &
    (filtered_df["Year"] == year)
]

# Create regional comparison chart
comparison_fig = px.bar(
    comparison_df,
    x="Geography name",
    y="Rate",
    title=f"Brain Cancer Incidence by Region — {year} ({gender})",
    labels={
        "Geography name": "Region",
        "Rate": "Age-standardised incidence rate"
    }
)


# Label the axes
comparison_fig.update_layout(
    xaxis_title="Region",
    yaxis_title="Age-standardised incidence rate"
)

# Display the comparison chart
st.plotly_chart(comparison_fig, use_container_width=True)
# Key statistics for the selected region and gender
latest_year = selected_df["Year"].max()
earliest_year = selected_df["Year"].min()

latest_rate = selected_df.loc[
    selected_df["Year"] == latest_year, "Rate"
].iloc[0]

earliest_rate = selected_df.loc[
    selected_df["Year"] == earliest_year, "Rate"
].iloc[0]

percentage_change = (
    (latest_rate - earliest_rate) / earliest_rate
) * 100

number_of_years = selected_df["Year"].nunique()

# Display the statistics
st.subheader("Key statistics")
st.caption(
    f"Selected region: {region} | Gender: {gender} | Data period: 2013–2022"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latest incidence rate",
    f"{latest_rate:.1f}"
)

col2.metric(
    "2013 incidence rate",
    f"{earliest_rate:.1f}"
)

col3.metric(
    "Change, 2013–2022",
    f"{percentage_change:.1f}%"
)

col4.metric(
    "Years of data",
    number_of_years
)
# Interactive data table
st.subheader("Explore the data")

table_df = selected_df[
    ["Year", "Gender", "Geography name", "Rate",
     "95% lower confidence interval",
     "95% upper confidence interval"]
].sort_values("Year")

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Rate": st.column_config.NumberColumn(
            "Incidence rate",
            format="%.1f"
        ),
        "95% lower confidence interval": st.column_config.NumberColumn(
            "Lower 95% CI",
            format="%.1f"
        ),
        "95% upper confidence interval": st.column_config.NumberColumn(
            "Upper 95% CI",
            format="%.1f"
        )
    }
)
st.divider()

st.caption(
    "Data source: NHS England National Disease Registration Service (NDRS) | "
    "Cancer Registration Statistics | 2013–2022"
)
