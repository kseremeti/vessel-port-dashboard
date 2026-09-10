import streamlit as st
import pandas as pd
import plotly.express as px


# -------------------------
# Page settings
# -------------------------

st.set_page_config(
    page_title="Port Call Analysis",
    layout="wide"
)


# -------------------------
# Dashboard title
# -------------------------

st.title("Port Call Analysis")

st.write(
    "Comparison of operational port calls "
    "between January-April 2019 and 2020."
)


# -------------------------
# Load prepared data
# -------------------------

df = pd.read_csv(
    "port_calls_monthly_analysis.csv"
)


# Convert month numbers into month names
month_names = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr"
}

df["MONTH_NAME"] = (
    df["MONTH"].map(month_names)
)


# -------------------------
# Sidebar filters
# -------------------------

st.sidebar.header("Filters")

selected_years = st.sidebar.multiselect(
    "Select year",
    options=sorted(df["YEAR"].unique()),
    default=sorted(df["YEAR"].unique())
)

selected_ports = st.sidebar.multiselect(
    "Select port",
    options=sorted(df["PORT_NAME"].unique()),
    default=sorted(df["PORT_NAME"].unique())
)


# -------------------------
# Apply filters
# -------------------------

filtered_df = df[
    df["YEAR"].isin(selected_years)
    &
    df["PORT_NAME"].isin(selected_ports)
]


# -------------------------
# KPI summary cards
# -------------------------

total_teu = filtered_df[
    "TOTAL_TEU"
].sum()

total_arrivals = filtered_df[
    "TOTAL_ARRIVALS"
].sum()

total_time = filtered_df[
    "TOTAL_TIME_IN_PORT_HOURS"
].sum()


col1, col2, col3 = st.columns(3)

col1.metric(
    "Total TEU",
    f"{total_teu:,.0f}"
)

col2.metric(
    "Total Arrivals",
    f"{total_arrivals:,.0f}"
)

col3.metric(
    "Total Time in Port (hours)",
    f"{total_time:,.0f}"
)


# -------------------------
# Total TEU chart
# -------------------------

st.subheader(
    "Total TEU per Month and Port"
)

teu_chart = px.bar(
    filtered_df,
    x="MONTH_NAME",
    y="TOTAL_TEU",
    color="PORT_NAME",
    facet_col="YEAR",
    barmode="group",
    category_orders={
        "MONTH_NAME": [
            "Jan",
            "Feb",
            "Mar",
            "Apr"
        ]
    },
    labels={
        "MONTH_NAME": "Month",
        "TOTAL_TEU": "Total TEU",
        "PORT_NAME": "Port"
    }
)

st.plotly_chart(
    teu_chart,
    use_container_width=True
)


# -------------------------
# Total Arrivals chart
# -------------------------

st.subheader(
    "Total Arrivals per Month and Port"
)

arrivals_chart = px.line(
    filtered_df,
    x="MONTH_NAME",
    y="TOTAL_ARRIVALS",
    color="PORT_NAME",
    facet_col="YEAR",
    markers=True,
    category_orders={
        "MONTH_NAME": [
            "Jan",
            "Feb",
            "Mar",
            "Apr"
        ]
    },
    labels={
        "MONTH_NAME": "Month",
        "TOTAL_ARRIVALS": "Total Arrivals",
        "PORT_NAME": "Port"
    }
)

st.plotly_chart(
    arrivals_chart,
    use_container_width=True
)


# -------------------------
# Time Spent at Port chart
# -------------------------

st.subheader(
    "Total Time Spent at Port per Month and Port"
)

time_chart = px.bar(
    filtered_df,
    x="TOTAL_TIME_IN_PORT_HOURS",
    y="MONTH_NAME",
    color="PORT_NAME",
    facet_col="YEAR",
    barmode="group",
    orientation="h",
    category_orders={
        "MONTH_NAME": [
            "Jan",
            "Feb",
            "Mar",
            "Apr"
        ]
    },
    labels={
        "MONTH_NAME": "Month",
        "TOTAL_TIME_IN_PORT_HOURS": "Time in Port (Hours)",
        "PORT_NAME": "Port"
    }
)

st.plotly_chart(
    time_chart,
    use_container_width=True
)


# -------------------------
# Supporting data
# -------------------------

with st.expander(
    "View underlying monthly data"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
