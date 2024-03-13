# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to the test of my first data visualization app! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        I am interested in presenting meteorological and snowpack data with aesthetic.  
        **👈 Select something from the sidebar** to see what I haven't created yet!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
    """
    )


if __name__ == "__main__":
    run()

# Load data
df = pd.read_csv('/workspaces/mwac-vis/Working MWAC data.csv')

# Mapping of wind direction categories to degrees
direction_to_degrees = {
    'N': 0,
    'NE': 45,
    'E': 90,
    'SE': 135,
    'S': 180,
    'SW': 225,
    'W': 270,
    'NW': 315
}

# Replace the wind direction strings with their corresponding degree values
df['Wind_Direction_Degrees'] = df['Wdir'].replace(direction_to_degrees)

START_YEAR = 2023

# Assign the correct year based on the month. Months 11 and 12 belong to the start year, and months 1 to 4 belong to the next year.
df['Year'] = df['Month'].apply(lambda month: START_YEAR if month >= 11 else START_YEAR + 1)

# Combine 'Year', 'Month', and 'Day' into a single 'Date' column
df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])


#WIND SPEED


# Ensure the columns for wind gust and wind speed are numeric
df['Wmax'] = pd.to_numeric(df['Wmax'], errors='coerce')
df['Wavg'] = pd.to_numeric(df['Wavg'], errors='coerce')

# Prepare the data for plotting by melting the DataFrame
plot_data = df.melt(id_vars='Date', value_vars=['Wmax', 'Wavg'], var_name='Wind Type', value_name='Speed (mph)')

# Create the line chart with Altair, making it interactive for zooming and panning
line_chart = alt.Chart(plot_data).mark_line().encode(
    x=alt.X('Date:T', axis=alt.Axis(title='Date', format='%b %d', labelAngle=-45)),  # Format date as "Month day", tilt labels
    y=alt.Y('Speed (mph):Q', axis=alt.Axis(title='Speed (mph)')),  # Quantitative data type for the Y-axis
    color='Wind Type:N',  # Nominal data type for color encoding to differentiate the lines
    tooltip=['Date:T', 'Speed (mph):Q', 'Wind Type:N']  # Tooltip for interactivity
).properties(
    title='Wind Speed Analysis'
).interactive(bind_x=True)  # Enable horizontal zooming and panning

# Display the chart in Streamlit
st.altair_chart(line_chart, use_container_width=True)



# Create a bar chart for HNS with a slight offset to the left
bar_chart_hns = alt.Chart(df).mark_bar(opacity=0.7, color='blue', xOffset=-5).encode(
    x=alt.X('Date:T', title='Date'),
    y=alt.Y('HNS:Q', title='Snow Totals (HNS)'),
    tooltip=['Date', 'HNS', 'HNW']
).properties(
    title='Snow Totals and Snow/Water Equivalent'
)

# Create a bar chart for HNW with a slight offset to the right
bar_chart_hnw = alt.Chart(df).mark_bar(opacity=0.7, color='green', xOffset=5).encode(
    x='Date:T',
    y='HNW:Q',
    tooltip=['Date', 'HNS', 'HNW']
)

# Layer the two bar charts
combined_chart = (bar_chart_hns + bar_chart_hnw).resolve_scale(
    y='shared'  # This ensures both charts use the same scale for the y-axis
)

# Display the combined chart in Streamlit
st.altair_chart(combined_chart, use_container_width=True)


# Display data
st.write(df)

