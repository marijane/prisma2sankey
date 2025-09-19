import streamlit as st
from datetime import datetime
import math

num_databases = 1
num_registers = 0
db_records = 0
reg_records = 0
total_db_reg_records = 0

def clear_inputs():
    pass

def reset_form():
    pass

st.set_page_config(page_title="PRISMA Sankey Diagram Configuration Generator")

st.title("PRISMA Sankey Diagram Configuration Generator", anchor=False)
st.write("""
Sankey Diagrams are a great match for PRISMA screening data! 

Use this tool to create a configuration file to visualize your PRISMA flow data with [SankeyMATIC](https://sankeymatic.com/).
""")

study_slug = st.text_input("Enter a unique name for your study (no spaces or special characters)", value="my_study", key="study_slug")

st.header("Identification", divider="rainbow", anchor=False)

with st.expander("Previous Studies and Reports for Updated Reviews", expanded=False):
    col1, col2 = st.columns([0.45, 0.55])
    with col1:
        prev_studies = st.number_input("Studies included in previous version of review", min_value=0, step=1, value=0, key="prev_studies")
    with col2:
        prev_reports = st.number_input("Reports of studies included in previous version of review", min_value=0, step=1, value=0, key="prev_reports")

with st.container(border=True):
    st.subheader("Identification of new studies via databases and registers", divider="blue", anchor=False)
    st.toggle("Specify each database and register", value=False, key="specify_databases_registers")
    if st.session_state.get("specify_databases_registers", True):
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            num_databases = st.number_input(
                "Number of Databases", min_value=1, step=1, value=1, key="num_databases_sidebar"
            )
        with col2:
            num_registers = st.number_input(
                "Number of Registers", min_value=0, step=1, value=0, key="num_registers_sidebar"
            )

    if st.session_state.get("specify_databases_registers", True):
        st.subheader("Databases", divider="green", anchor=False)
        databases = []
        for i in range(num_databases):
            col1, col2 = st.columns([2,1])
            with col1:
                db_name = st.text_input(f"Database #{i+1} name", key=f"db_name_{i}")
                db_name = db_name.strip().replace(" ", "\\n") if " " in db_name.strip() else db_name.strip()
            with col2:
                db_count = st.number_input(f"Number of records identified", min_value=0, step=1, key=f"db_count_{i}")
            databases.append({"name": db_name, "count": db_count})
            databases.sort(key=lambda db: db["count"], reverse=True)
        db_records = sum(db["count"] for db in databases)
        with st.container(horizontal_alignment="right"):
            st.badge(f"**Total records from databases:** {db_records}", color="green")

        if num_registers > 0:
            st.subheader("Registers", divider="orange", anchor=False)
            registers = []
            for i in range(num_registers):
                col1, col2 = st.columns([2,1])
                with col1:
                    reg_name = st.text_input(f"Register #{i+1} name", key=f"reg_name_{i}")
                    reg_name = reg_name.strip().replace(" ", "\\n") if " " in reg_name.strip() else reg_name.strip()
                with col2:
                    reg_count = st.number_input(f"Number of records identified", min_value=0, step=1, key=f"reg_count_{i}")
                registers.append({"name": reg_name, "count": reg_count})
                registers.sort(key=lambda reg: reg["count"], reverse=True)
            reg_records = sum(reg["count"] for reg in registers)
            with st.container(horizontal_alignment="right"):
                st.badge(f"**Total records from registers:** {reg_records}", color="orange")
    else:
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            db_records = st.number_input("Databases", min_value=0, step=1, value=0, key="db_records")
            with st.container(horizontal_alignment="right"):
                st.badge(f"**Total records from databases:** {db_records}", color="blue")
        with col2:
            reg_records = st.number_input("Registers", min_value=0, step=1, value=0, key="reg_records")
            with st.container(horizontal_alignment="right"):
                st.badge(f"**Total records from registers:** {reg_records}", color="blue")

    total_db_reg_records = db_records + reg_records

    if num_registers > 0:
        with st.container(horizontal_alignment="center"):
            st.badge(f"**Total records from databases and registers:** {total_db_reg_records}", color="blue")

with st.expander("Other Methods", expanded=False):
    st.subheader("Identification of new studies via other methods", divider="violet", anchor=False)
    st.toggle("Specify backward/forward citation searches separately", value=False, key="specify_citation_searches")
    if st.session_state.get("specify_citation_searches", True):
        col1, col2 = st.columns([0.5, 0.5], border=True)
        with col1:
            website_records = st.number_input("Websites", min_value=0, step=1, value=0, key="website_records")
            organization_records = st.number_input("Organizations", min_value=0, step=1, value=0, key="organization_records")
        with col2:
            backward_records = st.number_input("Backward citation searching", min_value=0, step=1, value=0, key="backward_records")
            forward_records = st.number_input("Forward citation searching", min_value=0, step=1, value=0, key="forward_records")
            citation_records = backward_records + forward_records
            with st.container(horizontal_alignment="center"):
                st.badge(f"**Total citation searching records:** {citation_records}", color="violet")

    else:
        col1, col2, col3 = st.columns([0.3, 0.33, 0.36])
        with col1: 
            website_records = st.number_input("Websites", min_value=0, step=1, value=0, key="website_records")
        with col2:
            organization_records = st.number_input("Organizations", min_value=0, step=1, value=0, key="organization_records")
        with col3:
            citation_records = st.number_input("Citation searching", min_value=0, step=1, value=0, key="citation_records")

    total_other_records = website_records + organization_records + citation_records
    with st.container(horizontal_alignment="center"):
        st.badge(f"**Total records from other sources:** {total_other_records}", color="violet")

with st.container(border=True):
    st.subheader("Records removed", divider="red", anchor=False)
    col1, col2, col3 = st.columns([0.33, 0.34, 0.33])
    with col1:
        duplicates_removed = st.number_input(
            "Duplicates removed manually", min_value=0, step=1, value=0, key="duplicates_removed"
        )
    with col2:
        automatically_excluded = st.number_input(
            "Records removed by software", min_value=0, step=1, value=0, key="automatically_excluded"
        )
    with col3:
        other_exclusions = st.number_input(
            "Records removed for other reasons", min_value=0, step=1, value=0, key="other_exclusions"
        )

    total_removed = duplicates_removed + automatically_excluded + other_exclusions
    with st.container(horizontal_alignment="center"):
        st.badge(f"**Total records removed:** {total_removed}", color="red")


st.header("Screening", divider="rainbow", anchor=False)
with st.container(border=True):
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        records_screened = st.number_input(
            "Records screened",
            min_value=0,
            step=1,
            value=total_db_reg_records - total_removed if total_db_reg_records > total_removed else 0,
            key="records_screened",
            disabled=True,
        )
    with col2:
        records_excluded = st.number_input("Records excluded", min_value=0, step=1, value=0, key="records_excluded")
        reports_not_retrieved = st.number_input("Reports not retrieved", min_value=0, step=1, value=0, key="reports_not_retrieved")
    with col1:
            reports_sought = st.number_input(
            "Reports sought for retrieval",
            min_value=0,
            step=1,
            value=records_screened - records_excluded if records_screened > records_excluded else 0,
            key="reports_sought",
            disabled=True,
        )

    reports_assessed = st.number_input("Reports assessed for eligibility", min_value=0, step=1, value=reports_sought - reports_not_retrieved if reports_sought > reports_not_retrieved else 0, key="reports_assessed", disabled=True)

    with st.container(border=True):
        num_exclusion_reasons = st.number_input("How many exclusion reasons did the screening team use for reports sourced from databases and/or registers?", min_value=1, step=1, value=1, key="num_exclusion_reasons")
        exclusion_reasons = []
        for i in range(num_exclusion_reasons):
            col1, col2 = st.columns([2, 1])
            with col1:
                reason = st.text_input(f"Exclusion reason #{i+1}", key=f"exclusion_reason_{i}")
            with col2:
                count = st.number_input(f"Reports excluded", min_value=0, step=1, key=f"exclusion_count_{i}")
            exclusion_reasons.append({"reason": reason, "count": count})
            exclusion_reasons.sort(key=lambda r: r["count"], reverse=True)
        total_exclusions = sum(reason["count"] for reason in exclusion_reasons)
        with st.container(horizontal_alignment="right"):
            st.badge(f"**Total reports excluded:** {total_exclusions}", color="yellow")
    reports_included = reports_assessed - total_exclusions
    with st.container(horizontal_alignment="center"):
        st.badge(f"**Total new reports included from databases/registers:** {reports_included}", color="blue")

expand = True if total_other_records > 0 else False
with st.expander("Other Sources", expanded=expand):
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        other_reports_sought = st.number_input("Reports from other sources sought for retrieval", min_value=0, step=1, value=0, key="reports_from_other_sources")
    with col2:
        other_reports_not_retrieved = st.number_input("Reports from other sources not retrieved", min_value=0, step=1, value=total_other_records - other_reports_sought if total_other_records > other_reports_sought else 0, key="other_reports_not_retrieved", disabled=True)
    with st.container(border=True):
        num_other_exclusion_reasons = st.number_input(
            "How many exclusion reasons did the screening team use for reports sourced via other methods?",
            min_value=1,
            step=1,
            value=1,
            key="num_other_exclusion_reasons",
        )
        other_exclusion_reasons = []
        for i in range(num_other_exclusion_reasons):
            col1, col2 = st.columns([2, 1])
            with col1:
                other_reason = st.text_input(f"Other exclusion reason #{i+1}", key=f"other_exclusion_reason_{i}")
            with col2:
                other_count = st.number_input(f"Other reports excluded", min_value=0, step=1, key=f"other_exclusion_count_{i}")
            other_exclusion_reasons.append({"reason": other_reason, "count": other_count})
            other_exclusion_reasons.sort(key=lambda r: r["count"], reverse=True)

        # Check for duplicate exclusion reasons
        exclusion_reason_texts = {reason["reason"].strip().lower() for reason in exclusion_reasons}
        for other_reason_obj in other_exclusion_reasons:
            if other_reason_obj["reason"].strip().lower() in exclusion_reason_texts and other_reason_obj["reason"].strip():
                st.error(f'Duplicate exclusion reason: "{other_reason_obj["reason"]}" is already used above. Please provide unique reasons for reports from other sources.')
        total_other_exclusions = sum(reason["count"] for reason in other_exclusion_reasons)
        with st.container(horizontal_alignment="right"):
            st.badge(f"**Total other reports excluded:** {total_other_exclusions}", color="yellow")

    other_reports_included = other_reports_sought - total_other_exclusions
    with st.container(horizontal_alignment="center"):
        st.badge(f"**Total other new reports included:** {other_reports_included}", color="blue")

st.header("Inclusion", divider="rainbow", anchor=False)
col1, col2 = st.columns([0.5, 0.5])
with col1:
    included_studies = st.number_input("New studies included in review", min_value=0, step=1, value=0, key="new_studies")
with col2:
    included_reports = st.number_input("Reports of new included studies", min_value=0, step=1, value=reports_included + other_reports_included, key="new_reports", disabled=True)

st.header("Metrics", divider="rainbow", anchor=False)
duplicate_rate = ((duplicates_removed + automatically_excluded) / total_db_reg_records) * 100 if total_db_reg_records > 0 else 0
inclusion_rate = (included_reports / records_screened) * 100 if records_screened > 0 else 0
col1, col2 = st.columns([0.5, 0.5])
with col1:
    st.metric(label="Duplicate Rate", value=f"{duplicate_rate:.2f}%",help="Percentage of total records identified that were removed as duplicates")
with col2:
    st.metric(label="Inclusion Rate", value=f"{inclusion_rate:.2f}%",help="Percentage of screened records that resulted in included reports")

if prev_studies > 0 or prev_reports > 0:
    total_studies = included_studies + prev_studies
    total_reports = included_reports + prev_reports

    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        st.number_input(
            "Total studies included in review", min_value=0, step=1, value=total_studies, key="total_studies"
        )
    with col2:
        st.number_input(
            "Reports of total included studies",
            min_value=0,
            step=1,
            value=total_reports,
            key="total_reports",
            disabled=True,
        )

st.header("Export Configuration", divider="rainbow", anchor=False)
if st.button("Generate Configuration", type="primary", use_container_width=True):
    config_lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config_lines.append("// SankeyMATIC diagram inputs - https://sankeymatic.com/")
    config_lines.append(f"// Generated {now} by https://prisma-sankey.streamlit.app/")
    config_lines.append("")
    config_lines.append("// === Nodes and Flows ===")
    config_lines.append("")
    if st.session_state.get("specify_databases_registers", True):
        # both databases and registers specified
        if num_databases > 0 and num_registers > 0:
            config_lines.append("// == Databases and Registers ==")
            for db in databases:
                config_lines.append(f'{db["name"]} [{db["count"]}] Database records')
            config_lines.append("")
            for reg in registers:
                config_lines.append(f'{reg["name"]} [{reg["count"]}] Register records')
            config_lines.append("")
            config_lines.append(f'Database records [{db_records}] Total records identified')
            config_lines.append(f'Register records [{reg_records}] Total records identified')
            config_lines.append("")
        # only databases specified
        elif num_databases > 0 and num_registers == 0:
            config_lines.append("// == Databases ==")
            for db in databases:
                if db["name"].strip() and db["count"] > 0:
                    config_lines.append(f'{db["name"].strip()} [{db["count"]}] Total records identified')
            config_lines.append("")
        # only registers specified
        elif num_databases == 0 and num_registers > 0:
            config_lines.append("// == Registers ==")
            for reg in registers:
                if reg["name"].strip() and reg["count"] > 0:
                    config_lines.append(f'{reg["name"].strip()} [{reg["count"]}] Total records identified')
            config_lines.append("")
    else:
        config_lines.append("// == Total Records Identified ==")
        if db_records > 0:
            config_lines.append(f'Databases [{db_records}] Total records identified')
        if reg_records > 0:
            config_lines.append(f'Registers [{reg_records}] Total records identified')
        config_lines.append("")

    config_lines.append("// == Records Removed ==")
    config_lines.append(f'Total records identified [{total_removed}] Records removed')
    config_lines.append("")
    if duplicates_removed > 0:
        config_lines.append(f'Records removed [{duplicates_removed}] Duplicates removed manually')
    if automatically_excluded > 0:
        config_lines.append(f'Records removed [{automatically_excluded}] Records removed by software')
    if other_exclusions > 0:
        config_lines.append(f'Records removed [{other_exclusions}] Records removed for other reasons')
    config_lines.append("")

    config_lines.append("// == Screened Records ==")
    config_lines.append(f'Total records identified [{records_screened}] Records screened')
    config_lines.append("")
    config_lines.append(f'Records screened [{records_excluded}] Records excluded')
    config_lines.append(f'Records screened [{reports_sought}] Reports sought\\nfor retrieval')
    config_lines.append("")
    config_lines.append(f'Reports sought\\nfor retrieval [{reports_not_retrieved}] Reports not retrieved')
    config_lines.append(f'Reports sought\\nfor retrieval [{reports_assessed}] Reports assessed\\nfor eligibility')
    config_lines.append("")
    config_lines.append(f'Reports assessed\\nfor eligibility [{total_exclusions}] Reports excluded')
    config_lines.append("")

    for reason in exclusion_reasons:
        if reason["reason"].strip() and reason["count"] > 0:
            reason_text = reason["reason"].strip()
            config_lines.append(f'Reports excluded [{reason["count"]}] {reason_text}')
    config_lines.append("")

    config_lines.append(f'Reports assessed\\nfor eligibility [{reports_included}] New studies included in review')
    config_lines.append("")

    if total_other_records > 0:
        config_lines.append("// == Other Methods ==")
        if st.session_state.get("specify_citation_searches", True):
            config_lines.append(f'Backward\\ncitations [{backward_records}] Citation searching')
            config_lines.append(f'Forward\\ncitations [{forward_records}] Citation searching')
            config_lines.append("")

        if sum(bool(x) for x in [website_records, organization_records, citation_records]) >= 2:
            if website_records > 0:
                config_lines.append(f'Websites [{website_records}] Records identified\\nfrom other methods')
            if organization_records > 0:
                config_lines.append(f'Organizations [{organization_records}] Records identified\\nfrom other methods')
            if citation_records > 0:
                config_lines.append(f'Citation searching [{citation_records}] Records identified\\nfrom other methods')
            config_lines.append("")

            config_lines.append(f'Records identified\\nfrom other methods [{other_reports_sought}] Other reports\\nsought for retrieval')

        elif sum(bool(x) for x in [website_records, organization_records, citation_records]) == 1:
            if website_records > 0:
                config_lines.append(f'Websites [{website_records}] Other reports\\nsought for retrieval')
            if organization_records > 0:
                config_lines.append(f'Organizations [{organization_records}] Other reports\\nsought for retrieval')
            if citation_records > 0:
                config_lines.append(f'Citation searching [{citation_records}] Other reports\\nsought for retrieval')

        config_lines.append(f'Other reports\\nsought for retrieval [{other_reports_sought}] Other reports\\nassessed for eligibility')
        config_lines.append("")
        config_lines.append(
            f'Other reports\\nassessed for eligibility [{other_reports_included}] New studies included in review'
        )
        config_lines.append(f'Other reports\\nassessed for eligibility [{total_other_exclusions}] Other reports excluded')
        for reason in other_exclusion_reasons:
            if reason["reason"].strip() and reason["count"] > 0:
                reason_text = reason["reason"].strip()
                config_lines.append(f'Other reports excluded [{reason["count"]}] {reason_text}')
        config_lines.append("")

        config_lines.append(
            f"Other reports\\nsought for retrieval [{other_reports_not_retrieved}] Other reports not retrieved"
        )
        config_lines.append("")

    flow_text = "\n".join(config_lines)

    config_lines.append("// === Settings ===")
    config_lines.append("")
    # calculate diagram height based on total records identified
    height = total_db_reg_records + total_other_records
    # round up to nearest 100, minimum 100
    rounded_height = int(math.ceil(height / 100.0)) * 100 if height > 0 else 100
    # font size and left/right margins are 1.5% of height
    font_left_right = int((rounded_height/100)*1.5)
    # node and top/bottom margins are 1% of height
    node_top_bottom = int((rounded_height/100))

    config_lines.append(f"size w {int(rounded_height * (1+math.sqrt(5))/2)}")
    config_lines.append(f" h {rounded_height}")
    config_lines.append(f"margin l {node_top_bottom}")
    config_lines.append(f" r {node_top_bottom}")
    config_lines.append(f" t {font_left_right}")
    config_lines.append(f" b {font_left_right}")
    config_lines.append("bg color #ffffff")
    config_lines.append(" transparent N")
    config_lines.append(f"node w {node_top_bottom}")
    config_lines.append(" h 50")
    config_lines.append(" spacing 95")
    config_lines.append(" border 0")
    config_lines.append(" theme a")
    config_lines.append(" color #888888")
    config_lines.append(" opacity 1")
    config_lines.append("flow curvature 0.3")
    config_lines.append(" inheritfrom outside-in")
    config_lines.append(" color #999999")
    config_lines.append(" opacity 0.45")
    config_lines.append("layout order exact")
    config_lines.append(" justifyorigins N")
    config_lines.append(" justifyends Y")
    config_lines.append(" reversegraph N")
    config_lines.append(" attachincompletesto nearest")
    config_lines.append("labels color #000000")
    config_lines.append(" hide N")
    config_lines.append(" highlight 0.5")
    config_lines.append(" fontface sans-serif")
    config_lines.append(" linespacing 0.2")
    config_lines.append(" relativesize 110")
    config_lines.append(" magnify 100")
    config_lines.append("labelname appears Y")
    config_lines.append(f" size {font_left_right}")
    config_lines.append(" weight 400")
    config_lines.append("labelvalue appears Y")
    config_lines.append(" fullprecision Y")
    config_lines.append(" position above")
    config_lines.append(" weight 400")
    config_lines.append("labelposition autoalign 1")
    config_lines.append(" scheme auto")
    config_lines.append(" first before")
    config_lines.append(" breakpoint 8")
    config_lines.append("value format ',.'")
    config_lines.append(" prefix ''")
    config_lines.append(" suffix ''")
    config_lines.append("themeoffset a 0")
    config_lines.append(" b 0")
    config_lines.append(" c 0")
    config_lines.append(" d 0")
    config_lines.append("meta mentionsankeymatic Y")
    config_lines.append(" listimbalances Y")

    config_text = "\n".join(config_lines)
    today_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        "Download Configuration",
        data=config_text,
        file_name=f"prisma_sankey-{study_slug}-{today_str}.txt",
        mime="text/plain",
        use_container_width=True,
        on_click="ignore"
    )
    st.link_button("Launch SankeyMATIC", url="https://sankeymatic.com/build/", type="primary", use_container_width=True)
    st.code(flow_text, line_numbers=True)
