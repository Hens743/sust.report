import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import json
from jinja2 import Template
import os
from weasyprint import HTML

# Sample Data (REPLACE THIS WITH YOUR ACTUAL DATA INTEGRATION)
data = {
    'Metric': ['Energy Consumption', 'Waste Generation', 'Water Usage', 'CO2 Emissions'],
    '2022': [15000, 5000, 2000, 10000],
    '2023 (Target)': [14000, 4500, 1800, 9000]
}
df = pd.DataFrame(data)

st.title("Data-Driven Sustainability Reporting Tool")

# Data Input Section (Simplified - REPLACE WITH REAL INPUT)
st.subheader("Enter Sustainability Data")

energy_input = st.number_input("Energy Consumption (2023)", value=14500)
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

# Bar chart visualization
st.subheader("Progress Visualization")
fig, ax = plt.subplots()
df.set_index('Metric')[['2022', '2023']].plot(kind='bar', ax=ax)
plt.title("Sustainability Performance")
plt.ylabel("Units")
st.pyplot(fig)

# Progress towards targets
st.subheader("Progress Towards Targets")
df['Progress'] = ((df['2023'] - df['2022']) / (df['2023 (Target)'] - df['2022'])) * 100
st.dataframe(df[['Metric', 'Progress']])

# Recommendations
st.subheader("Recommendations")
for index, row in df.iterrows():
    if row['Progress'] < 0:
        st.write(f"- Consider improvement strategies for {row['Metric']}.")
    else:
        st.write(f"- Maintain current practices for {row['Metric']}.")


# JSON and PDF Report Generation
st.subheader("Download PDF Report")

def generate_json(df):
    try:
        report_data = {
            "report_title": "Sustainability Report",
            "metrics": df.to_dict(orient='records'),
            "year": 2023
        }
        return json.dumps(report_data, indent=4)
    except Exception as e:
        st.error(f"Error generating JSON: {e}")
        return None

def generate_pdf(json_data):
    if json_data is None:
        return None

    try:
        template_path = os.path.join(os.path.dirname(__file__), "report_template.html")
        with open(template_path, "r") as f:
            template_string = f.read()
        template = Template(template_string)

        data = json.loads(json_data)  # Load JSON data

        html_output = template.render(data=data)  # Pass the entire data dictionary

        pdf_bytes = HTML(string=html_output).write_pdf()

        return pdf_bytes

    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None


json_data = generate_json(df)

if json_data:
    pdf_bytes = generate_pdf(json_data)

    if pdf_bytes:
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'data:application/pdf;base64,{b64}'
        st.markdown(f'<a href="{href}" download="sustainability_report.pdf">Download PDF Report</a>', unsafe_allow_html=True)

# Future features
st.subheader("Future Features")
st.write("- Integration with existing business systems")
st.write("- More sophisticated data analysis and benchmarking")
st.write("- Customizable reporting templates")
st.write("- User authentication and role management")
