import streamlit as st
import pandas as pd
import io
import base64
import json
from jinja2 import Template
import os
from weasyprint import HTML
import requests

st.set_page_config(layout="wide")

st.title("Data-Driven Sustainability Reporting Tool")

# Initialize report data in session state
if "report_data" not in st.session_state:
    st.session_state.report_data = {
        "report_title": "Sustainability Report",
        "year": 2023,
        "organization_number": "",  # Add organization number field
        "organization_name": "Example Company Name",
        "leadership_statement": "A message from leadership emphasizing our commitment to sustainability...",
        "reporting_period": "January 1, 2023 - December 31, 2023",
        "legal_form": "Limited Liability Company (LLC)",
        "ownership": "Privately held",
        "location": "123 Main Street, Anytown, CA 91234",
        "employees": "25 (15 full-time, 10 part-time)",
        "activities": "We manufacture and sell sustainable widgets...",
        "governance": "Our board of directors oversees our sustainability strategy...",
        "stakeholder_engagement": "We engage with our stakeholders through surveys, community events, and online platforms...",
        "reporting_process": "This report was compiled by the sustainability team...",
        "material_topics": [{"name": "Environmental Impact", "description": "Reducing our carbon footprint and minimizing waste..."}],
        "metrics": [{"name": "Energy Consumption", "2022": 15000, "2023_target": 14000, "2023": 14500}]
    }

report_data = st.session_state.report_data

# --- Input Sections ---

st.subheader("Report Information")
report_data["report_title"] = st.text_input("Report Title", value=report_data["report_title"])
report_data["year"] = st.number_input("Year", value=report_data["year"], min_value=2000, max_value=2100)

st.subheader("Organization Information")

org_number = st.text_input("Organization Number", value=report_data["organization_number"])

if st.button("Fetch Organization Information"):
    if org_number:
        try:
            api_url = f"https://data.brreg.no/enhetsregisteret/api/enheter/{org_number}"
            response = requests.get(api_url)
            response.raise_for_status()
            org_data = response.json()

            # Update report_data with API values ONLY if they exist in the response
            report_data["organization_name"] = org_data.get("navn") or report_data["organization_name"]  # Use existing value if API doesn't provide it
            report_data["legal_form"] = org_data.get("organisasjonsform", {}).get("beskrivelse") or report_data["legal_form"]
            report_data["hjemmeside"] = org_data.get("hjemmeside") or report_data.get("hjemmeside")
            report_data["postadresse"] = f"{org_data.get('postadresse', {}).get('adresse', [])[0] if org_data.get('postadresse', {}).get('adresse') else ''} {org_data.get('postadresse', {}).get('postnummer') or ''} {org_data.get('postadresse', {}).get('poststed') or ''}" if org_data.get('postadresse') else report_data.get("postadresse")
            report_data["forretningsadresse"] = f"{org_data.get('forretningsadresse', {}).get('adresse', [])[0] if org_data.get('forretningsadresse', {}).get('adresse') else ''} {org_data.get('forretningsadresse', {}).get('postnummer') or ''} {org_data.get('forretningsadresse', {}).get('poststed') or ''}" if org_data.get('forretningsadresse') else report_data.get("forretningsadresse")
            report_data["naeringskode1"] = org_data.get("naeringskode1", {}).get("beskrivelse") or report_data.get("naeringskode1")
            report_data["naeringskode2"] = org_data.get("naeringskode2", {}).get("beskrivelse") or report_data.get("naeringskode2")
            report_data["naeringskode3"] = org_data.get("naeringskode3", {}).get("beskrivelse") or report_data.get("naeringskode3")
            report_data["antallAnsatte"] = org_data.get("antallAnsatte") or report_data.get("antallAnsatte")
            report_data["stiftelsesdato"] = org_data.get("stiftelsesdato") or report_data.get("stiftelsesdato")
            report_data["vedtektsfestetFormaal"] = org_data.get("vedtektsfestetFormaal") or report_data.get("vedtektsfestetFormaal")
            report_data["aktivitet"] = org_data.get("aktivitet") or report_data.get("aktivitet")

            st.success("Organization information fetched successfully!")

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data from API: {e}")
        except (KeyError, TypeError, IndexError) as e:
            st.error(f"Error parsing API response. The API might have returned unexpected data or the data structure has changed. Error: {e}")
    else:
        st.warning("Please enter an organization number.")


report_data["organization_name"] = st.text_input("Organization Name", value=report_data["organization_name"]) # Now the input will show the value from the API or the default one
report_data["legal_form"] = st.text_input("Legal Form", value=report_data["legal_form"])
report_data["hjemmeside"] = st.text_input("Website", value=report_data["hjemmeside"])
report_data["postadresse"] = st.text_input("Postal Address", value=report_data["postadresse"])
report_data["forretningsadresse"] = st.text_input("Business Address", value=report_data["forretningsadresse"])
report_data["naeringskode1"] = st.text_input("Industry Code 1", value=report_data["naeringskode1"])
report_data["naeringskode2"] = st.text_input("Industry Code 2", value=report_data["naeringskode2"])
report_data["naeringskode3"] = st.text_input("Industry Code 3", value=report_data["naeringskode3"])
report_data["antallAnsatte"] = st.text_input("Number of Employees", value=report_data["antallAnsatte"])
report_data["stiftelsesdato"] = st.text_input("Date of Establishment", value=report_data["stiftelsesdato"])
report_data["vedtektsfestetFormaal"] = st.text_area("Purpose", value=report_data["vedtektsfestetFormaal"], height=150)
report_data["aktivitet"] = st.text_area("Activity", value=report_data["aktivitet"], height=150)






st.subheader("Material Topics")
new_topic = st.text_input("New Material Topic (e.g., Community Engagement)")
if st.button("Add Material Topic"):
    if new_topic and new_topic not in [topic["name"] for topic in report_data["material_topics"]]:
        report_data["material_topics"].append({"name": new_topic, "description": "Describe the topic here..."}) #Example description
        st.success(f"Material Topic '{new_topic}' added successfully.")
    elif new_topic in [topic["name"] for topic in report_data["material_topics"]]:
        st.error(f"Material Topic '{new_topic}' already exists. Please enter a different metric.")

for i, topic in enumerate(report_data["material_topics"]):
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        topic["name"] = st.text_input(f"Topic {i+1} Name", value=topic["name"], key=f"topic_name_{i}")
    with col2:
        topic["description"] = st.text_area(f"Topic {i+1} Description", value=topic["description"], height=100, key=f"topic_desc_{i}")
    with col3:
        if st.button(f"Delete Topic {i+1}", key=f"delete_topic_{i}"):
            del report_data["material_topics"][i]
            st.experimental_rerun()

st.subheader("Metrics")
new_metric = st.text_input("New Metric Name (e.g., Water Usage)")
if st.button("Add Metric"):
    if new_metric and new_metric not in [metric["name"] for metric in report_data["metrics"]]:
        report_data["metrics"].append({"name": new_metric, "2022": None, "2023_target": None, "2023": None})
        st.success(f"Metric '{new_metric}' added successfully.")
    elif new_metric in [metric["name"] for metric in report_data["metrics"]]:
        st.error(f"Metric '{new_metric}' already exists. Please enter a different metric.")

for i, metric in enumerate(report_data["metrics"]):
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    with col1:
        metric["name"] = st.text_input(f"Metric {i+1} Name", value=metric["name"], key=f"metric_name_{i}")
    with col2:
        metric["2022"] = st.number_input(f"2022 Value", value=metric["2022"], key=f"metric_2022_{i}")
    with col3:
        metric["2023_target"] = st.number_input(f"2023 Target", value=metric["2023_target"], key=f"metric_target_{i}")
    with col4:
        metric["2023"] = st.number_input(f"2023 Value", value=metric["2023"], key=f"metric_2023_{i}")
    with col5:
        if st.button(f"Delete Metric {i+1}", key=f"delete_metric_{i}"):
            del report_data["metrics"][i]
            st.experimental_rerun()

st.session_state.report_data = report_data


# --- PDF Generation ---
st.subheader("Download PDF Report")

def generate_pdf(report_data):
    try:
        template_path = os.path.join(os.path.dirname(__file__), "report_template.html")
        with open(template_path, "r") as f:
            template_string = f.read()
        template = Template(template_string)

        html_output = template.render(data=report_data)  # Pass the entire report_data dictionary

        pdf_bytes = HTML(string=html_output).write_pdf()
        return pdf_bytes

    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None

if st.button("Generate PDF Report"):
    pdf_bytes = generate_pdf(report_data)
    if pdf_bytes:
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'data:application/pdf;base64,{b64}'
        st.markdown(f'<a href="{href}" download="sustainability_report.pdf">Download PDF Report</a>', unsafe_allow_html=True)


# Future features (no changes)
st.subheader("Future Features")
st.write("- Integration with existing business systems")
st.write("- More sophisticated data analysis and benchmarking")
st.write("- Customizable reporting templates")
st.write("- User authentication and role management")
