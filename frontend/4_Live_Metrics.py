import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from backend.state import get_state
from backend.metrics import calculate_cpu, calculate_memory
from backend.autoscaler import apply_autoscaling
from backend.auth import require_auth, show_user_sidebar

st.set_page_config(page_title="Live Metrics — CloudScale", layout="wide", page_icon="📈")
user = require_auth()
show_user_sidebar()

state = get_state()

# Update
state.cpu_usage = calculate_cpu(state.active_users, state.instances)
state.memory_usage = calculate_memory(state.active_users, state.instances)
apply_autoscaling(state)
state.cpu_usage = calculate_cpu(state.active_users, state.instances)
state.memory_usage = calculate_memory(state.active_users, state.instances)
state.record_snapshot()

st.markdown("## 📈 Live Metrics")
st.caption("Detailed real-time performance monitoring dashboard")

st.divider()

# --------------------------
# Current Readings
# --------------------------
m1, m2, m3, m4 = st.columns(4)

with m1:
    cpu_delta = state.history_cpu[-1] - state.history_cpu[-2] if len(state.history_cpu) > 1 else 0
    st.metric("CPU Usage", f"{state.cpu_usage:.1f}%", f"{cpu_delta:+.1f}%")
with m2:
    mem_delta = state.history_memory[-1] - state.history_memory[-2] if len(state.history_memory) > 1 else 0
    st.metric("Memory Usage", f"{state.memory_usage:.1f}%", f"{mem_delta:+.1f}%")
with m3:
    inst_delta = state.history_instances[-1] - state.history_instances[-2] if len(state.history_instances) > 1 else 0
    st.metric("Instances", state.instances, f"{inst_delta:+d}" if inst_delta != 0 else "stable")
with m4:
    st.metric("Active Users", f"{state.active_users:,}", "Running" if state.load_running else "Idle")

st.divider()

# --------------------------
# Full Width CPU Chart
# --------------------------
if len(state.history_cpu) > 1:
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("CPU Utilization (%)", "Memory Utilization (%)", "Instance Count", "User Load"),
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )

    # CPU
    fig.add_trace(go.Scatter(
        y=state.history_cpu, mode='lines',
        name='CPU',
        line=dict(color='#3b82f6', width=2.5),
        fill='tozeroy', fillcolor='rgba(59,130,246,0.08)'
    ), row=1, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="rgba(239,68,68,0.5)", row=1, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="rgba(59,130,246,0.5)", row=1, col=1)

    # Memory
    fig.add_trace(go.Scatter(
        y=state.history_memory, mode='lines',
        name='Memory',
        line=dict(color='#a855f7', width=2.5),
        fill='tozeroy', fillcolor='rgba(168,85,247,0.08)'
    ), row=1, col=2)

    # Instances
    fig.add_trace(go.Scatter(
        y=state.history_instances, mode='lines+markers',
        name='Instances',
        line=dict(color='#22c55e', width=2.5),
        marker=dict(size=5, color='#22c55e'),
        fill='tozeroy', fillcolor='rgba(34,197,94,0.08)'
    ), row=2, col=1)

    # Users
    fig.add_trace(go.Scatter(
        y=state.history_users, mode='lines',
        name='Users',
        line=dict(color='#f59e0b', width=2.5),
        fill='tozeroy', fillcolor='rgba(245,158,11,0.08)'
    ), row=2, col=2)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=550,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )

    fig.update_yaxes(range=[0, 100], row=1, col=1)
    fig.update_yaxes(range=[0, 100], row=1, col=2)

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------
    # Stats Summary Table
    # --------------------------
    st.divider()
    st.markdown("### Performance Summary")

    if len(state.history_cpu) >= 2:
        import statistics

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("""
            <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-radius:12px;padding:20px">
                <h4 style="color:#3b82f6;margin:0 0 12px">CPU Statistics</h4>
            """, unsafe_allow_html=True)

            cpu_data = state.history_cpu
            st.markdown(f"""
                <table style="width:100%;color:#94a3b8;font-size:0.85rem">
                    <tr><td>Current</td><td style="text-align:right;color:#f1f5f9;font-weight:600">{cpu_data[-1]:.1f}%</td></tr>
                    <tr><td>Average</td><td style="text-align:right;color:#f1f5f9;font-weight:600">{statistics.mean(cpu_data):.1f}%</td></tr>
                    <tr><td>Peak</td><td style="text-align:right;color:#ef4444;font-weight:600">{max(cpu_data):.1f}%</td></tr>
                    <tr><td>Min</td><td style="text-align:right;color:#22c55e;font-weight:600">{min(cpu_data):.1f}%</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown("""
            <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-radius:12px;padding:20px">
                <h4 style="color:#a855f7;margin:0 0 12px">Memory Statistics</h4>
            """, unsafe_allow_html=True)

            mem_data = state.history_memory
            st.markdown(f"""
                <table style="width:100%;color:#94a3b8;font-size:0.85rem">
                    <tr><td>Current</td><td style="text-align:right;color:#f1f5f9;font-weight:600">{mem_data[-1]:.1f}%</td></tr>
                    <tr><td>Average</td><td style="text-align:right;color:#f1f5f9;font-weight:600">{statistics.mean(mem_data):.1f}%</td></tr>
                    <tr><td>Peak</td><td style="text-align:right;color:#ef4444;font-weight:600">{max(mem_data):.1f}%</td></tr>
                    <tr><td>Min</td><td style="text-align:right;color:#22c55e;font-weight:600">{min(mem_data):.1f}%</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

else:
    st.info("No data yet. Navigate to the **Load Generator** and start generating traffic to see live metrics.")

st.markdown("---")
st.caption("CloudScale Platform • Real-time metrics update on each page interaction")
