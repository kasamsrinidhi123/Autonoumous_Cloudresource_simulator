import streamlit as st
import time
from backend.state import get_state
from backend.metrics import calculate_cpu, calculate_memory
from backend.autoscaler import apply_autoscaling
from backend.auth import show_login_page, show_user_sidebar, get_user

# --------------------------
# Page Config
# --------------------------
st.set_page_config(
    page_title="CloudScale Platform",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------
# Auth Gate
# --------------------------
if not get_user():
    show_login_page()
    st.stop()

# --------------------------
# Light Theme Styles
# --------------------------
st.markdown("""
<style>
    .stApp { background-color: #f8fafc !important; }

    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] * { color: #1e293b !important; }
    [data-testid="stSidebar"] .stCaption p { color: #64748b !important; }

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .metric-card:hover {
        border-color: #3b82f6;
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(59,130,246,0.1);
    }
    .metric-card .metric-icon { font-size: 1.8rem; margin-bottom: 10px; }
    .metric-card .metric-label { font-size: 0.82rem; color: #64748b; margin-bottom: 6px; font-weight: 500; }
    .metric-card .metric-value { font-size: 1.9rem; font-weight: 700; color: #0f172a; }
    .metric-card .metric-sub { font-size: 0.75rem; color: #94a3b8; margin-top: 6px; }

    .status-banner {
        border-radius: 12px; padding: 16px 20px; margin: 16px 0;
        display: flex; align-items: center; gap: 12px; font-weight: 500; font-size: 0.92rem;
    }
    .status-scaling-out { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; }
    .status-scaling-in { background: #eff6ff; border: 1px solid #bfdbfe; color: #2563eb; }
    .status-stable { background: #f0fdf4; border: 1px solid #bbf7d0; color: #16a34a; }

    .brand-title {
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 1.6rem; font-weight: 800;
    }

    .cpu-bar-container {
        background: #f1f5f9; border-radius: 8px; height: 10px; overflow: hidden; margin-top: 10px;
    }
    .cpu-bar-fill { height: 100%; border-radius: 8px; transition: width 0.5s ease; }

    .event-card {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 14px 18px; margin-bottom: 8px; display: flex; align-items: center; gap: 12px;
    }
    .event-card:hover { border-color: #cbd5e1; }
    .event-card .event-title { font-size: 0.9rem; color: #0f172a; font-weight: 600; }
    .event-card .event-sub { font-size: 0.78rem; color: #94a3b8; }

    h1, h2, h3, h4, h5, h6, p, span, div, label { color: #0f172a; }
    .stMarkdown h3 { color: #1e293b !important; }
    [data-testid="stCaptionContainer"] p { color: #64748b !important; }

    .chart-container {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px;
        padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    /* Instance cards */
    .inst-card {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
        padding: 16px; transition: all 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .inst-card:hover { border-color: #3b82f6; box-shadow: 0 4px 16px rgba(59,130,246,0.08); }
    .inst-card .inst-name { font-size: 0.85rem; font-weight: 700; color: #0f172a; margin-bottom: 2px; }
    .inst-card .inst-id { font-size: 0.72rem; color: #94a3b8; font-family: monospace; }
    .inst-card .inst-bar-bg { background: #f1f5f9; border-radius: 4px; height: 6px; margin-top: 6px; overflow: hidden; }
    .inst-card .inst-bar-fill { height: 100%; border-radius: 4px; transition: width 0.5s ease; }
    .inst-card .inst-stat { font-size: 0.78rem; color: #475569; display: flex; justify-content: space-between; margin-top: 4px; }
    .inst-badge {
        display: inline-flex; align-items: center; gap: 4px;
        padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 600;
    }
    .inst-badge.healthy { background: #f0fdf4; color: #16a34a; }
    .inst-badge.warning { background: #fffbeb; color: #d97706; }
    .inst-badge.critical { background: #fef2f2; color: #dc2626; }
    .inst-badge.launching { background: #eff6ff; color: #2563eb; }
    .inst-badge.initializing { background: #f5f3ff; color: #7c3aed; }
    .inst-badge-dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }

    .live-dot {
        display: inline-block; width: 8px; height: 8px; border-radius: 50%;
        background: #22c55e; margin-right: 6px; animation: livePulse 2s ease-in-out infinite;
    }
    @keyframes livePulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }
        50% { opacity: 0.7; box-shadow: 0 0 0 6px rgba(34,197,94,0); }
    }
</style>
""", unsafe_allow_html=True)

show_user_sidebar()

# --------------------------
# Header (static — doesn't need refresh)
# --------------------------
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<span class="brand-title">☁️ CloudScale Dashboard</span>', unsafe_allow_html=True)
    st.caption(f"Logged in as **{get_user()['full_name']}** • Real-time infrastructure monitoring")


# --------------------------
# Live Dashboard Fragment — auto-refreshes every 2s
# --------------------------
@st.fragment(run_every=2)
def live_dashboard():
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    state = get_state()

    # Recalculate and run autoscaler
    state.cpu_usage = calculate_cpu(state.active_users, state.instances)
    state.memory_usage = calculate_memory(state.active_users, state.instances)
    apply_autoscaling(state)
    state.cpu_usage = calculate_cpu(state.active_users, state.instances)
    state.memory_usage = calculate_memory(state.active_users, state.instances)

    # Update individual instances
    state.tick_fleet()
    state.record_snapshot()

    if state.load_running:
        state.total_requests += state.active_users

    # ── Live indicator ──
    st.markdown(
        '<div style="font-size:0.82rem;color:#64748b;margin-bottom:8px">'
        '<span class="live-dot"></span>Live — auto-refreshing every 2 seconds</div>',
        unsafe_allow_html=True
    )

    # ── Status Banner ──
    if state.cpu_usage > 70:
        st.markdown(
            '<div class="status-banner status-scaling-out">🔴 High load detected — Auto Scaling OUT in progress</div>',
            unsafe_allow_html=True
        )
    elif state.cpu_usage < 30 and state.instances > 1:
        st.markdown(
            '<div class="status-banner status-scaling-in">🔵 Low load — Auto Scaling IN to optimize costs</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-banner status-stable">🟢 System stable — All instances healthy</div>',
            unsafe_allow_html=True
        )

    # ── Metric Cards ──
    c1, c2, c3, c4 = st.columns(4)
    cpu_color = "#ef4444" if state.cpu_usage > 70 else "#f59e0b" if state.cpu_usage > 50 else "#22c55e"
    mem_color = "#ef4444" if state.memory_usage > 80 else "#f59e0b" if state.memory_usage > 60 else "#22c55e"

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-label">Active Users</div>
            <div class="metric-value">{state.active_users:,}</div>
            <div class="metric-sub">{'🟢 Load running' if state.load_running else '⚪ No load'}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🖥️</div>
            <div class="metric-label">Active Instances</div>
            <div class="metric-value">{state.instances}</div>
            <div class="metric-sub">Min 1 / Max 10</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⚡</div>
            <div class="metric-label">CPU Usage</div>
            <div class="metric-value" style="color:{cpu_color}">{state.cpu_usage:.1f}%</div>
            <div class="cpu-bar-container">
                <div class="cpu-bar-fill" style="width:{min(state.cpu_usage, 100):.0f}%;background:{cpu_color}"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💾</div>
            <div class="metric-label">Memory Usage</div>
            <div class="metric-value" style="color:{mem_color}">{state.memory_usage:.1f}%</div>
            <div class="cpu-bar-container">
                <div class="cpu-bar-fill" style="width:{min(state.memory_usage, 100):.0f}%;background:{mem_color}"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # ── Instance Fleet ──
    st.markdown("### Instance Fleet")
    fleet = state.get_fleet_summary()

    if fleet:
        # Render instances in rows of 5
        cols_per_row = 5
        for row_start in range(0, len(fleet), cols_per_row):
            row_instances = fleet[row_start:row_start + cols_per_row]
            cols = st.columns(cols_per_row)
            for i, inst in enumerate(row_instances):
                with cols[i]:
                    cpu_c = "#ef4444" if inst["cpu"] > 75 else "#f59e0b" if inst["cpu"] > 50 else "#22c55e"
                    mem_c = "#ef4444" if inst["memory"] > 80 else "#f59e0b" if inst["memory"] > 60 else "#22c55e"
                    health = inst["health"]
                    badge_class = health if health in ("healthy", "warning", "critical", "launching", "initializing") else "healthy"

                    st.markdown(f"""
                    <div class="inst-card">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                            <div>
                                <div class="inst-name">🖥️ {inst['name']}</div>
                                <div class="inst-id">{inst['id']}</div>
                            </div>
                            <span class="inst-badge {badge_class}"><span class="inst-badge-dot"></span> {health}</span>
                        </div>
                        <div class="inst-stat"><span>CPU</span><span style="font-weight:600;color:{cpu_c}">{inst['cpu']}%</span></div>
                        <div class="inst-bar-bg"><div class="inst-bar-fill" style="width:{min(inst['cpu'],100):.0f}%;background:{cpu_c}"></div></div>
                        <div class="inst-stat" style="margin-top:8px"><span>Memory</span><span style="font-weight:600;color:{mem_c}">{inst['memory']}%</span></div>
                        <div class="inst-bar-bg"><div class="inst-bar-fill" style="width:{min(inst['memory'],100):.0f}%;background:{mem_c}"></div></div>
                        <div class="inst-stat" style="margin-top:8px"><span>Requests</span><span style="font-weight:600">{inst['requests']:,}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

            # Fill remaining empty cols if last row is incomplete
            # (handled by streamlit columns automatically)

    st.markdown("")

    # ── Charts ──
    if len(state.history_cpu) > 1:
        col_chart1, col_chart2 = st.columns(2)

        light_layout = dict(
            template="plotly_white",
            paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
            height=300, margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(orientation="h", y=1.12),
            font=dict(color="#475569"),
            xaxis=dict(gridcolor="#f1f5f9", zeroline=False),
            yaxis=dict(gridcolor="#f1f5f9", zeroline=False),
        )

        with col_chart1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=state.history_cpu, mode='lines', name='CPU %',
                line=dict(color='#3b82f6', width=2.5),
                fill='tozeroy', fillcolor='rgba(59,130,246,0.06)'
            ))
            fig.add_trace(go.Scatter(
                y=state.history_memory, mode='lines', name='Memory %',
                line=dict(color='#8b5cf6', width=2.5),
                fill='tozeroy', fillcolor='rgba(139,92,246,0.04)'
            ))
            fig.add_hline(y=70, line_dash="dash", line_color="rgba(239,68,68,0.35)", annotation_text="Scale Out")
            fig.add_hline(y=30, line_dash="dash", line_color="rgba(59,130,246,0.35)", annotation_text="Scale In")
            fig.update_layout(title="CPU & Memory Utilization", yaxis_range=[0, 100], **light_layout)
            st.plotly_chart(fig, use_container_width=True)

        with col_chart2:
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])
            fig2.add_trace(go.Scatter(
                y=state.history_instances, mode='lines+markers', name='Instances',
                line=dict(color='#22c55e', width=2.5), marker=dict(size=5)
            ), secondary_y=False)
            fig2.add_trace(go.Scatter(
                y=state.history_users, mode='lines', name='Users',
                line=dict(color='#f59e0b', width=2.5),
                fill='tozeroy', fillcolor='rgba(245,158,11,0.05)'
            ), secondary_y=True)
            fig2.update_layout(title="Instances & User Load", **light_layout)
            fig2.update_yaxes(title_text="Instances", secondary_y=False, gridcolor="#f1f5f9")
            fig2.update_yaxes(title_text="Users", secondary_y=True, gridcolor="#f1f5f9")
            st.plotly_chart(fig2, use_container_width=True)

    # ── Scaling Events ──
    st.markdown("### Recent Scaling Events")
    if state.scaling_events:
        for event in reversed(state.scaling_events[-5:]):
            icon = "🟢" if event["direction"] == "up" else "🔵"
            st.markdown(
                f"""<div class="event-card">
                    <span style="font-size:1.2rem">{icon}</span>
                    <div>
                        <div class="event-title">{event['type']} — {event['from']} → {event['to']} instances</div>
                        <div class="event-sub">{event['time']} • {event['reason']}</div>
                    </div>
                </div>""",
                unsafe_allow_html=True
            )
    else:
        st.info("No scaling events yet. Go to **Load Generator** to simulate traffic and trigger auto scaling.")


# Run the live dashboard
live_dashboard()

st.markdown("---")
st.caption("CloudScale Platform • Auto Scaling Simulation")
