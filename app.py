import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar
import os

# Set page config
st.set_page_config(layout="wide", page_title="Noise Pollution Dashboard")

# Custom CSS to improve layout
st.markdown("""
    <style>
    .main > div {
        padding: 2rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    try:
        # Read the CSV files directly using pandas
        stations_df = pd.read_csv("data/stations.csv")
        monthly_data = pd.read_csv("data/station_month.csv")

        # Merge the datasets
        df = pd.merge(monthly_data, stations_df, on='Station')

        # Add month name
        df['MonthName'] = df['Month'].apply(lambda x: calendar.month_name[x])

        return df

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("""
        Please ensure:
        1. The 'data' folder exists in your project directory
        2. Both CSV files are present in the data folder:
           - station_month.csv
           - stations.csv
        3. The CSV files are properly formatted
        """)
        st.stop()

# Load data
df = load_data()

# Dashboard title and description
st.title("🔊 Urban Noise Pollution Monitoring Dashboard")
st.markdown("""
### Analysis of Noise Levels Across Major Indian Cities
This dashboard provides comprehensive analysis of noise pollution levels, including temporal patterns,
zone-wise distribution, and compliance with noise limits.
""")

# Sidebar configuration
st.sidebar.title("Dashboard Controls")

# Main Filters
st.sidebar.header("Main Filters")

# City filter
selected_city = st.sidebar.selectbox("Select City", sorted(df['City'].unique()))

# Month filter
selected_month = st.sidebar.select_slider(
    "Select Month",
    options=range(1, 13),
    value=6,
    format_func=lambda x: calendar.month_name[x]
)

# Type filter
zone_types = sorted(df['Type'].unique())
selected_types = st.sidebar.multiselect(
    "Select Zone Types",
    zone_types,
    default=zone_types
)

# Temporal Analysis Settings
st.sidebar.markdown("---")
st.sidebar.header("Temporal Analysis Settings")

# Before months selection
st.sidebar.subheader("Before Period")
before_start = st.sidebar.select_slider(
    "Start Month (Before)",
    options=range(1, selected_month),
    value=max(1, selected_month - 3),
    format_func=lambda x: calendar.month_name[x],
    key='before_start'
)

before_end = st.sidebar.select_slider(
    "End Month (Before)",
    options=range(before_start, selected_month),
    value=selected_month - 1,
    format_func=lambda x: calendar.month_name[x],
    key='before_end'
)

# After months selection
st.sidebar.subheader("After Period")
after_start = st.sidebar.select_slider(
    "Start Month (After)",
    options=range(selected_month + 1, 13),
    value=selected_month + 1,
    format_func=lambda x: calendar.month_name[x],
    key='after_start'
)

after_end = st.sidebar.select_slider(
    "End Month (After)",
    options=range(after_start, 13),
    value=min(12, selected_month + 3),
    format_func=lambda x: calendar.month_name[x],
    key='after_end'
)

# Calculate comparison periods
before_months = list(range(before_start, before_end + 1))
after_months = list(range(after_start, after_end + 1))
comparison_months = before_months + [selected_month] + after_months

# Filter data based on selections
city_data = df[df['City'] == selected_city]
month_data = city_data[
    (city_data['Month'] == selected_month) &
    (city_data['Type'].isin(selected_types))
]

# SECTION 1: MAIN DASHBOARD
st.header("📊 Current Month Overview")

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

# Metrics
with col1:
    avg_day = month_data['Day'].mean()
    if selected_month > 1:
        prev_month_avg = city_data[city_data['Month'] == selected_month - 1]['Day'].mean()
        day_change = avg_day - prev_month_avg
        st.metric("Average Day Noise Level", f"{avg_day:.1f} dB", f"{day_change:+.1f} dB")
    else:
        st.metric("Average Day Noise Level", f"{avg_day:.1f} dB")

with col2:
    avg_night = month_data['Night'].mean()
    if selected_month > 1:
        prev_month_avg = city_data[city_data['Month'] == selected_month - 1]['Night'].mean()
        night_change = avg_night - prev_month_avg
        st.metric("Average Night Noise Level", f"{avg_night:.1f} dB", f"{night_change:+.1f} dB")
    else:
        st.metric("Average Night Noise Level", f"{avg_night:.1f} dB")

with col3:
    violation_perc = (
        (month_data['Day'] > month_data['DayLimit']).sum() +
        (month_data['Night'] > month_data['NightLimit']).sum()
    ) / (len(month_data) * 2) * 100
    st.metric("Violations Percentage", f"{violation_perc:.1f}%")

# Current Month Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("Noise Levels by Zone Type")
    zone_fig = px.box(
        month_data,
        x="Type",
        y=["Day", "Night"],
        points="all",
        title=f"Noise Distribution by Zone Type - {calendar.month_name[selected_month]}",
    )
    st.plotly_chart(zone_fig, use_container_width=True)

with col2:
    st.subheader("Monthly Trend")
    trend_data = city_data[city_data['Type'].isin(selected_types)].groupby('Month')[['Day', 'Night']].mean().reset_index()
    trend_fig = go.Figure()

    trend_fig.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Day'],
        name='Day',
        line=dict(color='orange')
    ))

    trend_fig.add_trace(go.Scatter(
        x=trend_data['Month'],
        y=trend_data['Night'],
        name='Night',
        line=dict(color='blue')
    ))

    trend_fig.update_layout(
        title=f"Average Noise Levels Throughout the Year",
        xaxis_title="Month",
        yaxis_title="Noise Level (dB)",
        xaxis=dict(tickmode='array', ticktext=calendar.month_abbr[1:], tickvals=list(range(1,13)))
    )
    st.plotly_chart(trend_fig, use_container_width=True)

# SECTION 2: TEMPORAL ANALYSIS
st.markdown("---")
st.header("🕒 Before-During-After Analysis")

# Display selected periods
period_col1, period_col2, period_col3 = st.columns(3)
with period_col1:
    st.info(f"Before Period: {calendar.month_name[before_start]} - {calendar.month_name[before_end]}")
with period_col2:
    st.success(f"Selected Month: {calendar.month_name[selected_month]}")
with period_col3:
    st.info(f"After Period: {calendar.month_name[after_start]} - {calendar.month_name[after_end]}")

# Create three columns for period stats
before_col, current_col, after_col = st.columns(3)

# Filter data for each period
before_data = city_data[
    (city_data['Month'].isin(before_months)) &
    (city_data['Type'].isin(selected_types))
]
current_data = city_data[
    (city_data['Month'] == selected_month) &
    (city_data['Type'].isin(selected_types))
]
after_data = city_data[
    (city_data['Month'].isin(after_months)) &
    (city_data['Type'].isin(selected_types))
]

# Display period metrics with monthly breakdown
with before_col:
    st.subheader("📉 Before Period")
    if not before_data.empty:
        st.metric("Avg Day Noise", f"{before_data['Day'].mean():.1f} dB")
        st.metric("Avg Night Noise", f"{before_data['Night'].mean():.1f} dB")
        st.metric("Violations", ((before_data['Day'] > before_data['DayLimit']) |
                               (before_data['Night'] > before_data['NightLimit'])).sum())

        st.markdown("**Monthly Breakdown:**")
        before_monthly = before_data.groupby('Month').agg({
            'Day': 'mean',
            'Night': 'mean'
        }).round(1)
        before_monthly.index = before_monthly.index.map(lambda x: calendar.month_name[x])
        st.dataframe(before_monthly, use_container_width=True)

with current_col:
    st.subheader("📊 Selected Month")
    st.metric("Avg Day Noise", f"{current_data['Day'].mean():.1f} dB")
    st.metric("Avg Night Noise", f"{current_data['Night'].mean():.1f} dB")
    st.metric("Violations", ((current_data['Day'] > current_data['DayLimit']) |
                           (current_data['Night'] > current_data['NightLimit'])).sum())

    st.markdown("**Zone-wise Breakdown:**")
    current_zones = current_data.groupby('Type').agg({
        'Day': 'mean',
        'Night': 'mean'
    }).round(1)
    st.dataframe(current_zones, use_container_width=True)

with after_col:
    st.subheader("📈 After Period")
    if not after_data.empty:
        st.metric("Avg Day Noise", f"{after_data['Day'].mean():.1f} dB")
        st.metric("Avg Night Noise", f"{after_data['Night'].mean():.1f} dB")
        st.metric("Violations", ((after_data['Day'] > after_data['DayLimit']) |
                               (after_data['Night'] > after_data['NightLimit'])).sum())

        st.markdown("**Monthly Breakdown:**")
        after_monthly = after_data.groupby('Month').agg({
            'Day': 'mean',
            'Night': 'mean'
        }).round(1)
        after_monthly.index = after_monthly.index.map(lambda x: calendar.month_name[x])
        st.dataframe(after_monthly, use_container_width=True)

# Temporal Comparison Visualization
st.subheader("Comparative Analysis")

# Create enhanced comparison visualization
comparison_data = city_data[
    (city_data['Month'].isin(comparison_months)) &
    (city_data['Type'].isin(selected_types))
]
comparison_avg = comparison_data.groupby('Month')[['Day', 'Night']].mean().reset_index()

fig = go.Figure()

# Before period
before_data = comparison_avg[comparison_avg['Month'].isin(before_months)]
fig.add_trace(go.Scatter(
    x=before_data['Month'],
    y=before_data['Day'],
    name='Before (Day)',
    line=dict(color='lightblue', width=2),
    mode='lines+markers'
))
fig.add_trace(go.Scatter(
    x=before_data['Month'],
    y=before_data['Night'],
    name='Before (Night)',
    line=dict(color='darkblue', width=2),
    mode='lines+markers'
))

# Selected month
selected_data = comparison_avg[comparison_avg['Month'] == selected_month]
if not selected_data.empty:
    fig.add_trace(go.Scatter(
        x=[selected_month],
        y=[selected_data['Day'].iloc[0]],
        name='Selected Month (Day)',
        marker=dict(color='orange', size=12, symbol='star'),
        mode='markers'
    ))
    fig.add_trace(go.Scatter(
        x=[selected_month],
        y=[selected_data['Night'].iloc[0]],
        name='Selected Month (Night)',
        marker=dict(color='red', size=12, symbol='star'),
        mode='markers'
    ))

# After period
after_data = comparison_avg[comparison_avg['Month'].isin(after_months)]
fig.add_trace(go.Scatter(
    x=after_data['Month'],
    y=after_data['Day'],
    name='After (Day)',
    line=dict(color='lightgreen', width=2),
    mode='lines+markers'
))
fig.add_trace(go.Scatter(
    x=after_data['Month'],
    y=after_data['Night'],
    name='After (Night)',
    line=dict(color='darkgreen', width=2),
    mode='lines+markers'
))

# Add vertical line for selected month
fig.add_vline(
    x=selected_month,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Selected Month ({calendar.month_name[selected_month]})"
)

fig.update_layout(
    title="Noise Levels: Before, During, and After Selected Month",
    xaxis_title="Month",
    yaxis_title="Noise Level (dB)",
    xaxis=dict(
        tickmode='array',
        ticktext=[calendar.month_name[i] for i in range(1,13)],
        tickvals=list(range(1,13))
    ),
    hovermode='x unified',
    showlegend=True,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# SECTION 3: STATION-WISE ANALYSIS
st.markdown("---")
st.header("📍 Station-wise Analysis")

# Station-wise violation analysis
# Continuing from the previous code...

# Station-wise analysis visualization
st.subheader("Station-wise Noise Levels")
station_data = month_data.sort_values('Day', ascending=False)

fig = go.Figure()

# Add Day levels
fig.add_trace(go.Bar(
    name='Day',
    x=station_data['Name'],
    y=station_data['Day'],
    marker_color='orange',
    text=station_data['Day'].round(1),
    textposition='auto',
))

# Add Night levels
fig.add_trace(go.Bar(
    name='Night',
    x=station_data['Name'],
    y=station_data['Night'],
    marker_color='blue',
    text=station_data['Night'].round(1),
    textposition='auto',
))

# Add limit lines
fig.add_trace(go.Scatter(
    name='Day Limit',
    x=station_data['Name'],
    y=station_data['DayLimit'],
    mode='lines',
    line=dict(color='red', dash='dash', width=2)
))

fig.add_trace(go.Scatter(
    name='Night Limit',
    x=station_data['Name'],
    y=station_data['NightLimit'],
    mode='lines',
    line=dict(color='purple', dash='dash', width=2)
))

fig.update_layout(
    title=f"Station-wise Noise Levels - {calendar.month_name[selected_month]}",
    xaxis_title="Station",
    yaxis_title="Noise Level (dB)",
    barmode='group',
    height=600,
    showlegend=True,
    xaxis={'tickangle': 45},
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

# Replace the Violation Analysis section with this corrected version:

# Violation Analysis
st.subheader("🚫 Violation Analysis")

# Create violation analysis dataframe
violation_data = month_data.copy()
violation_data['Day Violation'] = violation_data['Day'] > violation_data['DayLimit']
violation_data['Night Violation'] = violation_data['Night'] > violation_data['NightLimit']
violation_data['Total Violations'] = violation_data['Day Violation'].astype(int) + violation_data['Night Violation'].astype(int)

# Display violation metrics
v_col1, v_col2, v_col3 = st.columns(3)

with v_col1:
    day_violations = violation_data['Day Violation'].sum()
    st.metric("Day Violations", f"{day_violations}")

with v_col2:
    night_violations = violation_data['Night Violation'].sum()
    st.metric("Night Violations", f"{night_violations}")

with v_col3:
    violation_percentage = ((day_violations + night_violations) / (len(violation_data) * 2)) * 100
    st.metric("Violation Rate", f"{violation_percentage:.1f}%")

# Detailed violation table
st.markdown("### Detailed Violation Report")

# Prepare the violation table
violation_table = violation_data[[
    'Name', 'Type', 'Day', 'Night', 'DayLimit', 'NightLimit',
    'Day Violation', 'Night Violation', 'Total Violations'
]].sort_values('Total Violations', ascending=False)

# Format the numeric columns
violation_table['Day'] = violation_table['Day'].round(1)
violation_table['Night'] = violation_table['Night'].round(1)
violation_table['DayLimit'] = violation_table['DayLimit'].round(1)
violation_table['NightLimit'] = violation_table['NightLimit'].round(1)

# Create a custom style function for the entire dataframe
def color_violations(val):
    """
    Colors the cells based on violations:
    - Red background for violations
    - Green background for compliant values
    """
    if isinstance(val, bool):
        return f'background-color: {"#ffcccc" if val else "#ccffcc"}'
    return ''

# Apply the styling
styled_table = violation_table.style\
    .format({
        'Day': '{:.1f}',
        'Night': '{:.1f}',
        'DayLimit': '{:.1f}',
        'NightLimit': '{:.1f}',
    })\
    .map(color_violations, subset=['Day Violation', 'Night Violation'])\
    .background_gradient(subset=['Total Violations'], cmap='Reds')\
    .set_properties(**{
        'background-color': 'white',
        'font-size': '11px',
        'text-align': 'center'
    })

# Display the styled table
st.dataframe(styled_table, use_container_width=True)

# Add summary statistics
st.markdown("### Summary Statistics")
summary_stats = pd.DataFrame({
    'Metric': [
        'Average Day Level',
        'Average Night Level',
        'Maximum Day Level',
        'Maximum Night Level',
        'Total Day Violations',
        'Total Night Violations',
        'Overall Violation Rate'
    ],
    'Value': [
        f"{violation_data['Day'].mean():.1f} dB",
        f"{violation_data['Night'].mean():.1f} dB",
        f"{violation_data['Day'].max():.1f} dB",
        f"{violation_data['Night'].max():.1f} dB",
        f"{day_violations}",
        f"{night_violations}",
        f"{violation_percentage:.1f}%"
    ]
})

# Display summary statistics in two columns
col1, col2 = st.columns(2)
with col1:
    st.dataframe(summary_stats.iloc[:4], use_container_width=True, hide_index=True)
with col2:
    st.dataframe(summary_stats.iloc[4:], use_container_width=True, hide_index=True)

# Add zone-wise violation breakdown
st.markdown("### Zone-wise Violation Analysis")
zone_violations = violation_data.groupby('Type').agg({
    'Day Violation': 'sum',
    'Night Violation': 'sum',
    'Total Violations': 'sum'
}).reset_index()

# Create zone violation chart
fig = go.Figure()

fig.add_trace(go.Bar(
    name='Day Violations',
    x=zone_violations['Type'],
    y=zone_violations['Day Violation'],
    marker_color='orange'
))

fig.add_trace(go.Bar(
    name='Night Violations',
    x=zone_violations['Type'],
    y=zone_violations['Night Violation'],
    marker_color='blue'
))

fig.update_layout(
    title="Violations by Zone Type",
    xaxis_title="Zone Type",
    yaxis_title="Number of Violations",
    barmode='group',
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)