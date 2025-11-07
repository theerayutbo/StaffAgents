import time
from typing import List

import streamlit as st


st.set_page_config(page_title="StaffAgents Mission Control", layout="wide")

if "status" not in st.session_state:
    st.session_state.status = "Idle"
if "logs" not in st.session_state:
    st.session_state.logs: List[str] = []
if "reports" not in st.session_state:
    st.session_state.reports = {
        "Executive Summary": "",
        "Planner Report": "",
        "Marketing Report": "",
    }


st.title("StaffAgents Mission Control Center")

# Sidebar configuration
st.sidebar.header("ส่วนตั้งค่าภารกิจ")
main_objective = st.sidebar.text_area("กำหนดเป้าหมายหลัก", height=120)
llm_model = st.sidebar.selectbox(
    "เลือกโมเดลภาษา",
    ("Gemini-Pro", "GPT-4o", "Claude-3-Sonnet"),
)
data_sources = st.sidebar.multiselect(
    "เลือกแหล่งข้อมูล",
    ("Web Search", "News Feeds", "File Upload"),
)
agent_team = st.sidebar.selectbox(
    "เลือกทีมปฏิบัติงาน",
    (
        "Strategic Planning Team",
        "Marketing Analysis Team",
        "Risk Assessment Team",
    ),
)
start_button = st.sidebar.button("เริ่มภารกิจ", type="primary")

status_container = st.container()
log_placeholder = st.empty()


def simulate_mission():
    st.session_state.status = "Running..."
    st.session_state.logs = []
    logs = [
        "[Manager]: กำลังมอบหมายงานให้ทีม...",
        "[Planner]: กำลังค้นหาข้อมูลยุทธศาสตร์...",
        "[Analyst]: ประเมินความเสี่ยงจากฐานข้อมูล...",
        "[Marketing]: รวบรวมแนวโน้มตลาดจากข่าว...",
        "[Researcher]: ตรวจสอบความถูกต้องของข้อมูล...",
        "[Planner]: สรุปข้อมูลเพื่อนำเสนอ...",
        "[Manager]: ตรวจสอบความครบถ้วนของรายงาน...",
    ]
    for line in logs:
        st.session_state.logs.append(line)
        with log_placeholder.container():
            st.write("\n".join(st.session_state.logs))
        time.sleep(1)

    st.session_state.reports["Executive Summary"] = (
        "# ภาพรวมภารกิจ\n\n"
        "## เป้าหมายหลัก\n"
        f"- {main_objective or 'ยังไม่ได้กำหนด'}\n\n"
        "## ไฮไลต์สำคัญ\n"
        "- ทีมงานรวบรวมข้อมูลจากแหล่งที่เกี่ยวข้อง\n"
        "- วิเคราะห์โอกาสและความเสี่ยงเชิงกลยุทธ์\n"
        "- เตรียมข้อเสนอแนะสำหรับผู้บริหาร\n"
    )
    st.session_state.reports["Planner Report"] = (
        "# รายงานจากนักวางแผน\n\n"
        "- ประมวลผลข้อมูลยุทธศาสตร์หลัก\n"
        "- จัดลำดับความสำคัญของโครงการ\n"
        "- เตรียมแผนตอบสนองตามสถานการณ์\n"
    )
    st.session_state.reports["Marketing Report"] = (
        "# รายงานจากฝ่ายการตลาด\n\n"
        "- วิเคราะห์แนวโน้มตลาดล่าสุด\n"
        "- ประเมินคู่แข่งหลัก\n"
        "- จัดทำแผนการสื่อสารเชิงรุก\n"
    )
    st.session_state.status = "Complete"


if start_button:
    with status_container:
        st.success("เริ่มภารกิจแล้ว กำลังจำลองการทำงาน...")
    simulate_mission()

# Status display
with status_container:
    st.subheader("สถานะปัจจุบัน")
    st.write(st.session_state.status)

with log_placeholder.container():
    st.subheader("สถานะและ Log")
    st.write("\n".join(st.session_state.logs) if st.session_state.logs else "ยังไม่มีข้อมูล Log")

# Report tabs
summary_tab, planner_tab, marketing_tab = st.tabs(
    ["สรุปผลผู้บริหาร", "รายงานจากนักวางแผน", "รายงานจากฝ่ายการตลาด"]
)

with summary_tab:
    st.markdown(st.session_state.reports["Executive Summary"] or "ยังไม่มีรายงาน")
    st.download_button(
        label="Export (.md)",
        data=st.session_state.reports["Executive Summary"],
        file_name="executive_summary.md",
        mime="text/markdown",
        disabled=not st.session_state.reports["Executive Summary"],
    )
    if st.button("แปลเป็นภาษาไทย", key="translate_summary"):
        st.session_state.reports["Executive Summary"] = "นี่คือรายงานฉบับแปลภาษาไทย (ตัวอย่าง)"
        st.experimental_rerun()

with planner_tab:
    st.markdown(st.session_state.reports["Planner Report"] or "ยังไม่มีรายงาน")
    if st.button("แปลเป็นภาษาไทย", key="translate_planner"):
        st.session_state.reports["Planner Report"] = "นี่คือรายงานฉบับแปลภาษาไทย (ตัวอย่าง)"
        st.experimental_rerun()

with marketing_tab:
    st.markdown(st.session_state.reports["Marketing Report"] or "ยังไม่มีรายงาน")
    if st.button("แปลเป็นภาษาไทย", key="translate_marketing"):
        st.session_state.reports["Marketing Report"] = "นี่คือรายงานฉบับแปลภาษาไทย (ตัวอย่าง)"
        st.experimental_rerun()
