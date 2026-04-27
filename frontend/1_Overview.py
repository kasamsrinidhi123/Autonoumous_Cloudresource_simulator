import streamlit as st
import plotly.graph_objects as go
from backend.metrics import calculate_cpu, calculate_memory
from backend.autoscaler import apply_autoscaling
from backend.state import get_state
from backend.auth import require_auth, show_user_sidebar

st.set_page_config(page_title="Overview — CloudScale", layout="wide", page_icon="📊")
user = require_auth()
show_user_sidebar()

state = get_state()

# Update metrics
state.cpu_usage = calculate_cpu(state.active_users, state.instances)
state.memory_usage = calculate_memory(state.active_users, state.instances)
apply_autoscaling(state)
state.cpu_usage = calculate_cpu(state.active_users, state.instances)
state.memory_usage = calculate_memory(state.active_users, state.instances)
state.record_snapshot()

st.markdown("## 📊 System Overview")
st.caption("Real-time view of your infrastructure health and scaling status")

st.divider()

# --------------------------
# Gauges Row
# --------------------------
g1, g2, g3 = st.columns(3)

with g1:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=state.cpu_usage,
        number={"suffix": "%", "font": {"size": 36, "color": "#f1f5f9"}},
        title={"text": "CPU Utilization", "font": {"size": 14, "color": "#94a3b8"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#475569"},
            "bar": {"color": "#3b82f6"},
            "bgcolor": "#1a1f2e",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 30], "color": "rgba(34,197,94,0.15)"},
                {"range": [30, 70], "color": "rgba(245,158,11,0.15)"},
                {"range": [70, 100], "color": "rgba(239,68,68,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#ef4444", "width": 3},
                "thickness": 0.8,
                "value": 70
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=220,
        margin=dict(l=20, r=20, t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

with g2:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=state.memory_usage,
        number={"suffix": "%", "font": {"size": 36, "color": "#f1f5f9"}},
        title={"text": "Memory Utilization", "font": {"size": 14, "color": "#94a3b8"}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#475569"},
            "bar": {"color": "#a855f7"},
            "bgcolor": "#1a1f2e",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(34,197,94,0.15)"},
                {"range": [40, 75], "color": "rgba(245,158,11,0.15)"},
                {"range": [75, 100], "color": "rgba(239,68,68,0.15)"},
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=220,
        margin=dict(l=20, r=20, t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

with g3:
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=state.instances,
        number={"font": {"size": 52, "color": "#22c55e"}},
        title={"text": "Active Instances", "font": {"size": 14, "color": "#94a3b8"}},
        delta={"reference": state.history_instances[-2] if len(state.history_instances) > 1 else state.instances, "relative": False}
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=220,
        margin=dict(l=20, r=20, t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------
# Key Stats
# --------------------------
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("👥 Active Users", f"{state.active_users:,}")
with s2:
    st.metric("📈 Scale Outs", state.total_scale_outs)
with s3:
    st.metric("📉 Scale Ins", state.total_scale_ins)
with s4:
    st.metric("📋 Total Requests", f"{state.total_requests:,}")

# --------------------------
# System Status
# --------------------------
st.divider()

if state.cpu_usage > 70:
    st.error("🔴 **System Under High Load** — Scaling out to handle demand. New instances being provisioned.")
elif state.cpu_usage < 30 and state.instances > 1:
    st.info("🔵 **Low Load Detected** — Scaling in to reduce costs. Excess instances being terminated.")
elif state.load_running:
    st.success("🟢 **System Stable** — All instances healthy. Load within normal parameters.")
else:
    st.warning("⚠️ **Idle** — No active load. Go to Load Generator to simulate traffic.")
