import streamlit as st
from backend.state import get_state
from backend.auth import require_auth, show_user_sidebar

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="Load Generator", layout="wide", page_icon="⚡")
user = require_auth()
show_user_sidebar()

state = get_state()

st.title("⚡ Load Generator")
st.caption("Simulate user traffic to trigger Auto Scaling behavior")

st.divider()

# --------------------------
# Load Slider
# --------------------------
st.subheader("Simulated User Load")

users = st.slider(
    "Users",
    min_value=0,
    max_value=1000,
    step=50,
    value=state.active_users
)

# Load level indicator
if users == 0:
    load_label = "🔘 No Load"
    load_color = "gray"
elif users < 300:
    load_label = "🟢 Low Load"
    load_color = "green"
elif users < 700:
    load_label = "🟡 Medium Load"
    load_color = "orange"
else:
    load_label = "🔴 High Load"
    load_color = "red"

st.markdown(f"**Load Level:** `{load_label}`")

st.divider()

# --------------------------
# Controls
# --------------------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ Apply Load", use_container_width=True, type="primary"):
        state.active_users = users
        state.load_running = users > 0
        if users > 0:
            state.logs.append(f"[LOAD SET] Load set to {users} users")
        else:
            state.logs.append("[STOP] Load set to 0")
        st.rerun()

with col2:
    if st.button("🚀 Max Load (1000)", use_container_width=True):
        state.active_users = 1000
        state.load_running = True
        state.logs.append("[MAX LOAD] Load set to 1000 users")
        st.rerun()

with col3:
    if st.button("⛔ Stop Load", use_container_width=True):
        state.active_users = 0
        state.load_running = False
        state.logs.append("[STOP] Load stopped")
        st.rerun()

st.divider()

# --------------------------
# Quick Load Presets
# --------------------------
st.subheader("Quick Presets")
p1, p2, p3, p4, p5 = st.columns(5)

with p1:
    if st.button("100 Users", use_container_width=True):
        state.active_users = 100
        state.load_running = True
        state.logs.append("[LOAD SET] Load set to 100 users")
        st.rerun()
with p2:
    if st.button("300 Users", use_container_width=True):
        state.active_users = 300
        state.load_running = True
        state.logs.append("[LOAD SET] Load set to 300 users")
        st.rerun()
with p3:
    if st.button("500 Users", use_container_width=True):
        state.active_users = 500
        state.load_running = True
        state.logs.append("[LOAD SET] Load set to 500 users")
        st.rerun()
with p4:
    if st.button("750 Users", use_container_width=True):
        state.active_users = 750
        state.load_running = True
        state.logs.append("[LOAD SET] Load set to 750 users")
        st.rerun()
with p5:
    if st.button("1000 Users", use_container_width=True):
        state.active_users = 1000
        state.load_running = True
        state.logs.append("[LOAD SET] Load set to 1000 users")
        st.rerun()

st.divider()

# --------------------------
# Load Status
# --------------------------
st.subheader("Current Status")

if state.load_running and state.active_users > 0:
    st.success(
        f"Load generator running — **{state.active_users:,}** simulated users active across **{state.instances}** instance(s)"
    )
else:
    st.info(
        "No load is being generated. Use the slider or quick presets above."
    )

st.divider()

# --------------------------
# Explanation Section
# --------------------------
st.subheader("How Load Generation Works")

st.markdown(
    """
1️⃣ **Simulate Requests**
User traffic is generated using a virtual load slider.

2️⃣ **CPU Utilization Increases**
Each EC2 instance processes requests, raising CPU usage.

3️⃣ **CloudWatch Detection (Simulated)**
Average CPU is monitored continuously.

4️⃣ **Auto Scaling Triggered**
Instances are added or removed based on thresholds.
"""
)

st.markdown("---")
st.caption("AWS Auto Scaling — simulated environment (no real AWS resources)")
