import streamlit as st
from backend.auth import require_auth, show_user_sidebar
from backend.state import get_state

st.set_page_config(page_title="Architecture — CloudScale", layout="wide", page_icon="🧩")
user = require_auth()
show_user_sidebar()

state = get_state()

st.markdown("## 🧩 System Architecture")
st.caption("How CloudScale components interact to deliver automatic scaling")

st.divider()

# --------------------------
# Interactive Architecture Flow
# --------------------------
def arch_block(icon, title, description, color="#3b82f6", active=False):
    border = f"2px solid {color}" if active else "1px solid #2a2f3e"
    glow = f"0 0 20px {color}33" if active else "none"
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a1f2e 0%, #111827 100%);
        border: {border};
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        box-shadow: {glow};
        transition: all 0.3s;
        margin-bottom: 4px;">
        <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
        <h4 style="color: {color}; margin: 0 0 8px 0; font-size: 1rem;">{title}</h4>
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0; line-height: 1.5;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def arrow_down():
    st.markdown("""
    <div style="text-align:center; margin: 8px 0;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <polyline points="19 12 12 19 5 12"></polyline>
        </svg>
    </div>
    """, unsafe_allow_html=True)

# Flow
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    arch_block(
        "🌐", "Users / Clients",
        f"End users send requests to the application. Currently simulating {state.active_users:,} concurrent users.",
        "#f59e0b",
        active=state.active_users > 0
    )
    arrow_down()
    arch_block(
        "⚖️", "Application Load Balancer",
        "Distributes incoming requests evenly across available EC2 instances using round-robin routing.",
        "#22c55e",
        active=state.load_running
    )
    arrow_down()
    arch_block(
        "📦", "Auto Scaling Group",
        f"Manages instance fleet based on scaling policies. Scale out at >70% CPU, scale in at <30% CPU. Currently running {state.instances} instance(s).",
        "#3b82f6",
        active=state.cpu_usage > 70 or (state.cpu_usage < 30 and state.instances > 1)
    )
    arrow_down()

    # Instance grid
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1a1f2e 0%, #111827 100%);
        border: 1px solid #2a2f3e;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-bottom: 4px;">
        <h4 style="color: #22c55e; margin: 0 0 12px 0; font-size: 1rem;">🖥️ EC2 Instances</h4>
        <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
            {''.join([
                f'<div style="width:48px;height:48px;border-radius:10px;background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.3);display:flex;align-items:center;justify-content:center;font-size:1.2rem">🖥️</div>'
                for _ in range(state.instances)
            ])}
        </div>
        <p style="color: #64748b; font-size: 0.8rem; margin-top: 12px;">
            {state.instances} running • CPU: {state.cpu_usage:.1f}% • Mem: {state.memory_usage:.1f}%
        </p>
    </div>
    """, unsafe_allow_html=True)

    arrow_down()

    arch_block(
        "📊", "CloudWatch Monitoring",
        "Continuously monitors CPU and memory metrics. Triggers scaling policies when thresholds are breached.",
        "#a855f7",
        active=True
    )

st.divider()

# --------------------------
# Scaling Rules Summary
# --------------------------
st.markdown("### Scaling Configuration")

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown("""
    <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-radius:12px;padding:20px">
        <h4 style="color:#ef4444;margin:0 0 8px">📈 Scale Out</h4>
        <p style="color:#94a3b8;font-size:0.85rem;margin:0">When CPU > <strong style="color:#f1f5f9">70%</strong><br>Add 1 instance<br>Cooldown: 5 seconds</p>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-radius:12px;padding:20px">
        <h4 style="color:#3b82f6;margin:0 0 8px">📉 Scale In</h4>
        <p style="color:#94a3b8;font-size:0.85rem;margin:0">When CPU < <strong style="color:#f1f5f9">30%</strong><br>Remove 1 instance<br>Cooldown: 5 seconds</p>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown("""
    <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-radius:12px;padding:20px">
        <h4 style="color:#22c55e;margin:0 0 8px">🛡️ Guardrails</h4>
        <p style="color:#94a3b8;font-size:0.85rem;margin:0">Min instances: <strong style="color:#f1f5f9">1</strong><br>Max instances: <strong style="color:#f1f5f9">10</strong><br>Always-on baseline</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("CloudScale Platform • Simulated AWS Architecture (no real cloud resources)")
