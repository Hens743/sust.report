import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Sample Data (REPLACE THIS WITH YOUR ACTUAL DATA INTEGRATION)
data = {
    'Metric': ['Energy Consumption', 'Waste Generation', 'Water Usage', 'CO2 Emissions'],
    '2022': [15000, 5000, 2000, 10000],
    '2023 (Target)': [14000, 4500, 1800, 9000]
}
df = pd.DataFrame(data)

st.title("Data-Driven Sustainability Reporting Tool Prototype")

# Data Input Section (Simplified - REPLACE WITH REAL INPUT)
st.subheader("Enter Sustainability Data (Simplified)")

# Example manual input fields (replace with actual data entry)
energy_input = st.number_input("Energy Consumption (2023)", value=14500)  # Example
df.loc[df['Metric'] == 'Energy Consumption', '2023'] = energy_input

waste_input = st.number_input("Waste Generation (2023)", value=4800)
df.loc[df['Metric'] == 'Waste Generation', '2023'] = waste_input

water_input = st.number_input("Water Usage (2023)", value=1900)
df.loc[df['Metric'] == 'Water Usage', '2023'] = water_input

co2_input = st.number_input("CO2 Emissions (2023)", value=9500)
df.loc[df['Metric'] == 'CO2 Emissions', '2023'] = co2_input



# Report Generation
st.subheader("Sustainability Report")

# Display data as a table
st.dataframe(df)

# Create a bar chart to visualize progress
st.subheader("Progress Visualization")
fig, ax = plt.subplots()
df.set_index('Metric')[['2022', '2023']].plot(kind='bar', ax=ax)  # Compare 2022 and 2023
plt.title("Sustainability Performance")
plt.ylabel("Units")
st.pyplot(fig)

# Calculate and display progress towards targets (example)
st.subheader("Progress Towards Targets")
df['Progress'] = ((df['2023'] - df['2022']) / (df['2023 (Target)'] - df['2022'])) * 100
st.dataframe(df[['Metric', 'Progress']])

# Example Recommendations (replace with actual insights)
st.subheader("Recommendations (Example)")

for index, row in df.iterrows():
    if row['Progress'] < 0:
        st.write(f"- Consider improvement strategies for {row['Metric']}.")  # More general
    else:
        st.write(f"- Maintain current practices for {row['Metric']}.")


# Report Download Section
st.subheader("Download Report")

def generate_csv(df):
    output = io.StringIO()
    df.to_csv(output, index=False)
    csv_string = output.getvalue()
    return csv_string

csv = generate_csv(df)

b64 = base64.b64encode(csv.encode()).decode()
href = f'data:file/csv;base64,{b64}'

st.markdown(f'<a href="{href}" download="sustainability_report.csv">Download CSV Report</a>', unsafe_allow_html=True)


# Placeholder for future features
st.subheader("Future Features")
st.write("- Integration with existing business systems (accounting, energy, etc.)")
st.write("- More sophisticated data analysis and benchmarking")
st.write("- Customizable reporting templates")
st.write("- User authentication and role management")

# To run: streamlit run your_script_name.py (replace with your filename)
