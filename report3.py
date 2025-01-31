import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import json
from jinja2 import Template
import os
from weasyprint import HTML

st.set_page_config(layout="wide") # Set page layout to wide for better visualization

st.title("Data-Driven Sustainability Reporting Tool")

# Initialize data in session state
if "sustainability_data" not in st.session_state:
    st.session_state.sustainability_data = pd.DataFrame(columns=['Metric', '2022', '2023 (Target)', '2023'])

df = st.session_state.sustainability_data

# Data Input Section (Completely Dynamic)
st.subheader("Enter/Edit Sustainability Data")

new_metric = st.text_input("New Metric Name")
if st.button("Add Metric"):
    if new_metric:
        if new_metric not in df['Metric'].values: # Check for duplicate metrics
            new_row = pd.DataFrame({'Metric': [new_metric], '2022': [None], '2023 (Target)': [None], '2023': [None]})
            df = pd.concat([df, new_row], ignore_index=True)
            st.session_state.sustainability_data = df
            st.success(f"Metric '{new_metric}' added successfully.")
        else:
            st.error(f"Metric '{new_metric}' already exists. Please enter a different metric.")

# Edit/Delete Metrics
for index, row in df.iterrows():
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1]) # Adjust column widths

    with col1:
        st.write(row['Metric'])
    with col2:
        year_2022 = st.number_input(f"2022", value=row['2022'] if pd.notna(row['2022']) else None, key=f"2022_{index}")
        df.loc[index, '2022'] = year_2022
    with col3:
        year_2023_target = st.number_input(f"2023 Target", value=row['2023 (Target)'] if pd.notna(row['2023 (Target)']) else None, key=f"target_{index}")
        df.loc[index, '2023 (Target)'] = year_2023_target
    with col4:
        year_2023 = st.number_input(f"2023", value=row['2023'] if pd.notna(row['2023']) else None, key=f"2023_{index}")
        df.loc[index, '2023'] = year_2023
    with col5:
        if st.button(f"Delete", key=f"delete_{index}"):
            df = df.drop(index)
            st.session_state.sustainability_data = df
            st.experimental_rerun()

st.session_state.sustainability_data = df

# Report Generation
st.subheader("Sustainability Report")

if not df.empty: # Check if the dataframe is not empty before displaying and plotting
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
else:
    st.write("Please add sustainability metrics to generate the report.")


# JSON and PDF Report Generation
st.subheader("Download PDF Report")

def generate_json(df):
    if not df.empty:
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
    else:
        return None

def generate_pdf(json_data):
    if json_data is None:
        return None

    try:
        template_path = os.path.join(os.path.dirname(__file__), "report_template.html")
        with open(template_path, "r") as f:
            template_string = f.read()
        template = Template(template_string)

        data = json.loads(json_data)

        html_output = template.render(data=data)

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
