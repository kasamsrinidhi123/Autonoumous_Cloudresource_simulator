import streamlit as st
import plotly.graph_objects as go
from backend.state import get_state
from backend.auth import require_auth, show_user_sidebar

st.set_page_config(page_title="Cost Analysis — CloudScale", layout="wide", page_icon="💰")
user = require_auth()
show_user_sidebar()

state = get_state()

COST_PER_INSTANCE_HOUR = 0.0116  # t2.micro equivalent
COST_PER_INSTANCE_MONTH = COST_PER_INSTANCE_HOUR * 24 * 30

st.markdown("## 💰 Cost Analysis")
st.caption("Understand how auto scaling optimizes your infrastructure spending")

st.divider()

# --------------------------
# Cost Metrics
# --------------------------
current_hourly = state.instances * COST_PER_INSTANCE_HOUR
current_monthly = state.instances * COST_PER_INSTANCE_MONTH
fixed_monthly = 10 * COST_PER_INSTANCE_MONTH  # Max instances always on
savings_pct = ((fixed_monthly - current_monthly) / fixed_monthly * 100) if fixed_monthly > 0 else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-radius:12px;padding:20px;text-align:center">
        <div style="color:#64748b;font-size:0.82rem;margin-bottom:4px">Hourly Cost</div>
        <div style="color:#22c55e;font-size:1.8rem;font-weight:700">${current_hourly:.4f}</div>
        <div style="color:#475569;font-size:0.75rem;margin-top:4px">{state.instances} instance(s)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-radius:12px;padding:20px;text-align:center">
        <div style="color:#64748b;font-size:0.82rem;margin-bottom:4px">Monthly Estimate</div>
        <div style="color:#3b82f6;font-size:1.8rem;font-weight:700">${current_monthly:.2f}</div>
        <div style="color:#475569;font-size:0.75rem;margin-top:4px">At current scale</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div style="background:#1a1f2e;border:1px solid #2a2f3e;border-radius:12px;padding:20px;text-align:center">
        <div style="color:#64748b;font-size:0.82rem;margin-bottom:4px">Fixed (10 instances)</div>
        <div style="color:#ef4444;font-size:1.8rem;font-weight:700">${fixed_monthly:.2f}</div>
        <div style="color:#475569;font-size:0.75rem;margin-top:4px">Without auto scaling</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.25);border-radius:12px;padding:20px;text-align:center">
        <div style="color:#22c55e;font-size:0.82rem;margin-bottom:4px">Savings</div>
        <div style="color:#22c55e;font-size:1.8rem;font-weight:700">{savings_pct:.0f}%</div>
        <div style="color:#475569;font-size:0.75rem;margin-top:4px">${(fixed_monthly - current_monthly):.2f}/month</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --------------------------
# Cost Comparison Chart
# --------------------------
col_ch1, col_ch2 = st.columns(2)

with col_ch1:
    st.markdown("### Cost Comparison")
    scenarios = ['Current (Auto Scaled)', 'Always 2 Instances', 'Always 5 Instances', 'Always 10 Instances']
    costs = [
        current_monthly,
        2 * COST_PER_INSTANCE_MONTH,
        5 * COST_PER_INSTANCE_MONTH,
        10 * COST_PER_INSTANCE_MONTH
    ]
    colors = ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444']

    fig = go.Figure(go.Bar(
        x=scenarios,
        y=costs,
        marker_color=colors,
        text=[f"${c:.2f}" for c in costs],
        textposition='outside',
        textfont=dict(color='#94a3b8')
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Monthly Cost ($)",
        height=350,
        margin=dict(l=20, r=20, t=10, b=20),
        yaxis=dict(gridcolor='rgba(42,47,62,0.5)')
    )
    st.plotly_chart(fig, use_container_width=True)

with col_ch2:
    st.markdown("### Instance Distribution")
    # Show a donut chart of instance types
    if state.history_instances:
        from collections import Counter
        inst_counts = Counter(state.history_instances)
        labels = [f"{k} instance{'s' if k > 1 else ''}" for k in sorted(inst_counts.keys())]
        values = [inst_counts[k] for k in sorted(inst_counts.keys())]

        fig2 = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=['#3b82f6', '#22c55e', '#a855f7', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899', '#14b8a6', '#64748b', '#f43f5e']),
            textinfo='label+percent',
            textfont=dict(size=12, color='#94a3b8')
        ))
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=20, r=20, t=10, b=20),
            showlegend=False,
            annotations=[dict(text=f"{state.instances}", x=0.5, y=0.5, font_size=28, font_color="#f1f5f9", showarrow=False)]
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Run load tests to see instance distribution data.")

st.divider()

# --------------------------
# Pricing Table
# --------------------------
st.markdown("### Instance Pricing (Simulated)")

st.markdown("""
<table style="width:100%;border-collapse:collapse;font-size:0.85rem">
    <thead>
        <tr style="border-bottom:2px solid #2a2f3e">
            <th style="text-align:left;padding:10px;color:#94a3b8">Instance Type</th>
            <th style="text-align:right;padding:10px;color:#94a3b8">vCPUs</th>
            <th style="text-align:right;padding:10px;color:#94a3b8">Memory</th>
            <th style="text-align:right;padding:10px;color:#94a3b8">Hourly Cost</th>
            <th style="text-align:right;padding:10px;color:#94a3b8">Monthly Cost</th>
        </tr>
    </thead>
    <tbody>
        <tr style="border-bottom:1px solid #1e2740;background:rgba(34,197,94,0.05)">
            <td style="padding:10px;color:#22c55e;font-weight:600">t2.micro (current)</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">1</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">1 GiB</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">$0.0116</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">$8.35</td>
        </tr>
        <tr style="border-bottom:1px solid #1e2740">
            <td style="padding:10px;color:#94a3b8">t2.small</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">1</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">2 GiB</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">$0.0230</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">$16.56</td>
        </tr>
        <tr style="border-bottom:1px solid #1e2740">
            <td style="padding:10px;color:#94a3b8">t2.medium</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">2</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">4 GiB</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">$0.0464</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">$33.41</td>
        </tr>
        <tr>
            <td style="padding:10px;color:#94a3b8">t2.large</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">2</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">8 GiB</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">$0.0928</td>
            <td style="text-align:right;padding:10px;color:#f1f5f9">$66.82</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

st.markdown("")
st.markdown("""
> **Key Insight:** Auto scaling with `t2.micro` instances at the current load of **{} users** costs **${:.2f}/month** — a **{:.0f}% savings** compared to provisioning the maximum 10 instances permanently.
""".format(state.active_users, current_monthly, savings_pct))

st.markdown("---")
st.caption("CloudScale Platform • Cost estimates are simulated using AWS t2.micro pricing")
