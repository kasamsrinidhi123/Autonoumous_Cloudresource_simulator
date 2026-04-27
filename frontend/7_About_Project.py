import streamlit as st
from backend.auth import require_auth, show_user_sidebar

st.set_page_config(page_title="About — CloudScale", layout="wide", page_icon="ℹ️")
user = require_auth()
show_user_sidebar()

st.markdown("## ℹ️ About CloudScale")
st.caption("Project details, tech stack, and credits")

st.divider()

# --------------------------
# Project Info
# --------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Project Overview

    **CloudScale** is a dynamic web application that simulates **AWS Auto Scaling** behavior.
    It provides a fully interactive dashboard for understanding how cloud infrastructure
    automatically adjusts compute capacity based on real-time demand.

    ### What This Demonstrates

    - **Load Simulation** — Generate virtual user traffic with configurable patterns
    - **Auto Scaling Logic** — Policy-driven scale-out and scale-in decisions based on CPU thresholds
    - **Real-Time Monitoring** — Live charts showing CPU, memory, instance count, and user load
    - **Cost Optimization** — See how auto scaling reduces infrastructure costs vs. fixed provisioning
    - **Event Tracking** — Complete timeline of all scaling events with detailed context
    - **System Architecture** — Visual representation of AWS component interactions
    """)

with col2:
    st.markdown("""
    <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-radius:14px;padding:24px">
        <h4 style="color:#3b82f6;margin:0 0 16px">Tech Stack</h4>
        <div style="margin-bottom:10px">
            <span style="color:#64748b;font-size:0.8rem">Frontend</span><br>
            <span style="color:#f1f5f9;font-weight:600">Streamlit</span>
        </div>
        <div style="margin-bottom:10px">
            <span style="color:#64748b;font-size:0.8rem">Backend</span><br>
            <span style="color:#f1f5f9;font-weight:600">Python 3.11+</span>
        </div>
        <div style="margin-bottom:10px">
            <span style="color:#64748b;font-size:0.8rem">Charts</span><br>
            <span style="color:#f1f5f9;font-weight:600">Plotly</span>
        </div>
        <div style="margin-bottom:10px">
            <span style="color:#64748b;font-size:0.8rem">Database</span><br>
            <span style="color:#f1f5f9;font-weight:600">SQLite</span>
        </div>
        <div>
            <span style="color:#64748b;font-size:0.8rem">Concept</span><br>
            <span style="color:#f1f5f9;font-weight:600">AWS Auto Scaling</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --------------------------
# AWS Concepts Explained
# --------------------------
st.markdown("### AWS Concepts Covered")

concepts = [
    ("EC2 Instances", "Virtual servers that run applications. Our simulator creates and removes these based on demand.", "#3b82f6"),
    ("Auto Scaling Group", "Manages a fleet of EC2 instances. Automatically scales based on CloudWatch metrics.", "#22c55e"),
    ("Application Load Balancer", "Distributes incoming traffic across multiple instances for high availability.", "#f59e0b"),
    ("CloudWatch", "Monitors metrics like CPU usage. Triggers alarms that invoke scaling policies.", "#a855f7"),
    ("Scaling Policies", "Rules that define when to add or remove instances. We use CPU threshold-based policies.", "#ef4444"),
    ("Cooldown Period", "Time between scaling actions to prevent rapid fluctuations. Set to 5 seconds in our simulation.", "#06b6d4"),
]

cols = st.columns(3)
for i, (title, desc, color) in enumerate(concepts):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-left:3px solid {color};border-radius:10px;padding:16px;margin-bottom:12px;min-height:130px">
            <h4 style="color:{color};font-size:0.9rem;margin:0 0 8px">{title}</h4>
            <p style="color:#94a3b8;font-size:0.82rem;margin:0;line-height:1.5">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# --------------------------
# How to Use
# --------------------------
st.markdown("### How to Use")

st.markdown("""
| Step | Page | Action |
|------|------|--------|
| 1 | **Load Generator** | Set number of simulated users and click Start Load |
| 2 | **Overview** | Watch metrics update — CPU, instances, scaling status |
| 3 | **Live Metrics** | View detailed charts of CPU, memory, instances over time |
| 4 | **Architecture** | See which components are active based on current state |
| 5 | **Scaling Activity** | Review timeline of all scale-out and scale-in events |
| 6 | **Cost Analysis** | Compare costs of auto scaling vs. fixed provisioning |
""")

st.divider()

st.markdown("""
> **Note:** This is a **cost-free simulation**. No real AWS EC2 instances are launched.
> All scaling behavior is computed locally using Python.
""")

st.markdown("---")
st.caption("CloudScale Platform • Final Year Project • Auto Scaling Simulation")
