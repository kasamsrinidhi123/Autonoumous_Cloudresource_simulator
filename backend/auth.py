import streamlit as st
import streamlit.components.v1 as components
import random
from backend.db import signup, login

def get_user():
    return st.session_state.get("auth_user", None)

def require_auth():
    user = get_user()
    if not user:
        st.warning("Please sign in from the **Home** page to access this feature.")
        st.stop()
    return user

def show_login_page():
    user = get_user()
    if user:
        return True

    # ─── Full Premium CSS Override ───
    st.markdown("""
    <style>
    /* ── Hide all Streamlit chrome ── */
    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarCollapsedControl"],
    header[data-testid="stHeader"],
    #MainMenu, footer,
    [data-testid="stDecoration"],
    [data-testid="stToolbar"],
    .stDeployButton {
        display: none !important;
    }

    /* ── App background ── */
    .stApp {
        background: #030712 !important;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59,130,246,0.12), transparent),
            radial-gradient(ellipse 60% 40% at 80% 100%, rgba(139,92,246,0.08), transparent) !important;
    }

    /* ── Remove default padding ── */
    .stMainBlockContainer,
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem !important;
        max-width: 1200px !important;
    }

    /* ── Tab styling — pill toggle ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 14px !important;
        padding: 5px !important;
        gap: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        color: #6b7280 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 0 !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #d1d5db !important;
        background: rgba(255,255,255,0.04) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(59,130,246,0.3) !important;
    }

    .stTabs [data-baseweb="tab-border"],
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* ── Input fields — large, rounded, Claude-style ── */
    .stTextInput > div > div {
        border-radius: 14px !important;
        overflow: hidden;
    }

    .stTextInput > div > div > input {
        background: #111827 !important;
        border: 1px solid #374151 !important;
        border-radius: 14px !important;
        color: #f9fafb !important;
        padding: 16px 18px !important;
        font-size: 15px !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
        letter-spacing: 0.01em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        caret-color: #818cf8 !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow:
            0 0 0 4px rgba(99,102,241,0.15),
            0 0 32px rgba(99,102,241,0.08) !important;
        background: #1a2234 !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #6b7280 !important;
        font-weight: 400 !important;
    }

    .stTextInput > label {
        color: #9ca3af !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        margin-bottom: 6px !important;
    }

    /* ── Submit button — gradient with glow ── */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 50%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 16px 24px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 20px rgba(99,102,241,0.25) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stFormSubmitButton > button:hover {
        box-shadow:
            0 8px 32px rgba(99,102,241,0.4),
            0 0 60px rgba(99,102,241,0.15) !important;
        transform: translateY(-1px) !important;
    }

    .stFormSubmitButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Alert styling ── */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
        border: none !important;
        backdrop-filter: blur(8px) !important;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-color: #6366f1 transparent transparent !important;
    }

    /* ── Divider ── */
    [data-testid="stHorizontalBlock"] hr {
        border-color: rgba(255,255,255,0.06) !important;
    }

    /* ── Caption ── */
    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #6b7280 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ─── Animated Background Layer ───
    particles = ""
    for _ in range(30):
        x, y = random.randint(0, 100), random.randint(0, 100)
        d = round(random.uniform(4, 10), 1)
        dl = round(random.uniform(0, 8), 1)
        sz = random.choice([1, 2, 2, 3])
        op = round(random.uniform(0.15, 0.5), 2)
        particles += (
            f'<div style="position:fixed;width:{sz}px;height:{sz}px;'
            f'background:rgba(139,92,246,{op});border-radius:50%;'
            f'left:{x}%;top:{y}%;'
            f'animation:pFloat {d}s ease-in-out {dl}s infinite;'
            f'pointer-events:none;z-index:0"></div>'
        )

    components.html(f"""
    <style>
    @keyframes gridDrift {{
        0% {{ transform: translate(0,0) rotate(0deg); }}
        100% {{ transform: translate(60px,60px) rotate(0.5deg); }}
    }}
    @keyframes orbFloat1 {{
        0%,100% {{ transform: translate(0,0) scale(1); }}
        33% {{ transform: translate(-30px,20px) scale(1.05); }}
        66% {{ transform: translate(20px,-15px) scale(0.95); }}
    }}
    @keyframes orbFloat2 {{
        0%,100% {{ transform: translate(0,0) scale(1); }}
        50% {{ transform: translate(25px,-35px) scale(1.08); }}
    }}
    @keyframes pFloat {{
        0%,100% {{ opacity:0; transform: translateY(0px) scale(1); }}
        50% {{ opacity:1; transform: translateY(-25px) scale(1.5); }}
    }}
    @keyframes lineGlow {{
        0%,100% {{ opacity: 0.02; }}
        50% {{ opacity: 0.06; }}
    }}
    </style>

    <!-- Grid -->
    <div style="position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:0">
        <div style="position:absolute;inset:-50%;
            background-image:
                linear-gradient(rgba(99,102,241,0.03) 1px,transparent 1px),
                linear-gradient(90deg,rgba(99,102,241,0.03) 1px,transparent 1px);
            background-size:80px 80px;
            animation:gridDrift 25s linear infinite">
        </div>
    </div>

    <!-- Orbs -->
    <div style="position:fixed;width:700px;height:700px;border-radius:50%;
        background:radial-gradient(circle,rgba(59,130,246,0.07),rgba(59,130,246,0.02) 40%,transparent 70%);
        top:-250px;right:-150px;animation:orbFloat1 20s ease-in-out infinite;pointer-events:none;z-index:0">
    </div>
    <div style="position:fixed;width:500px;height:500px;border-radius:50%;
        background:radial-gradient(circle,rgba(139,92,246,0.06),rgba(139,92,246,0.01) 40%,transparent 70%);
        bottom:-150px;left:-100px;animation:orbFloat2 16s ease-in-out infinite;pointer-events:none;z-index:0">
    </div>
    <div style="position:fixed;width:300px;height:300px;border-radius:50%;
        background:radial-gradient(circle,rgba(34,197,94,0.04),transparent 70%);
        top:40%;left:45%;animation:orbFloat1 22s ease-in-out 3s infinite;pointer-events:none;z-index:0">
    </div>

    <!-- Accent line -->
    <div style="position:fixed;top:0;left:0;right:0;height:1px;
        background:linear-gradient(90deg,transparent,rgba(99,102,241,0.3),rgba(59,130,246,0.2),transparent);
        animation:lineGlow 4s ease-in-out infinite;pointer-events:none;z-index:1">
    </div>

    <!-- Particles -->
    {particles}
    """, height=0)

    # ─── Two-Column Layout ───
    col_brand, col_gap, col_auth = st.columns([1.15, 0.15, 0.85])

    # ── LEFT: Brand Panel ──
    with col_brand:
        st.markdown("")
        st.markdown("")
        st.markdown("")

        # Logo
        st.markdown("""
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:48px">
            <div style="width:44px;height:44px;border-radius:12px;
                background:linear-gradient(135deg,rgba(59,130,246,0.15),rgba(139,92,246,0.15));
                border:1px solid rgba(99,102,241,0.2);
                display:flex;align-items:center;justify-content:center;
                box-shadow:0 0 24px rgba(99,102,241,0.1)">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#818cf8" stroke-width="2">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
            </div>
            <span style="font-size:24px;font-weight:700;
                background:linear-gradient(135deg,#818cf8,#a78bfa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                CloudScale
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Headline
        st.markdown("""
        <h1 style="font-size:46px;font-weight:800;line-height:1.1;
            letter-spacing:-0.03em;margin:0 0 20px;color:#f9fafb">
            Infrastructure<br>that
            <span style="background:linear-gradient(135deg,#60a5fa,#818cf8,#a78bfa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent">
                scales with you.
            </span>
        </h1>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style="font-size:17px;color:#6b7280;line-height:1.75;margin-bottom:44px;max-width:460px;font-weight:400">
            Intelligent autoscaling, real-time monitoring, and traffic management
            — all from a single control plane.
        </p>
        """, unsafe_allow_html=True)

        # Feature cards
        features = [
            ("Smart Auto Scaling", "Policy-driven scaling with CPU and memory metrics", "linear-gradient(135deg,rgba(59,130,246,0.12),rgba(59,130,246,0.04))", "#60a5fa",
             '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 11-9-9c2.52 0 4.93 1 6.74 2.74L21 3v9z"/></svg>'),
            ("Real-Time Monitoring", "Live dashboards with alerts and event tracking", "linear-gradient(135deg,rgba(34,197,94,0.12),rgba(34,197,94,0.04))", "#4ade80",
             '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/></svg>'),
            ("Load Testing Built In", "Simulate traffic to validate scaling policies", "linear-gradient(135deg,rgba(168,85,247,0.12),rgba(168,85,247,0.04))", "#c084fc",
             '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>'),
        ]

        for title, desc, bg, color, icon in features:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:16px;
                padding:16px 20px;margin-bottom:10px;
                background:rgba(255,255,255,0.02);
                border:1px solid rgba(255,255,255,0.05);
                border-radius:14px;
                transition:all 0.3s cubic-bezier(0.4,0,0.2,1);
                cursor:default"
                onmouseover="this.style.borderColor='rgba(99,102,241,0.2)';this.style.background='rgba(255,255,255,0.04)';this.style.transform='translateX(4px)'"
                onmouseout="this.style.borderColor='rgba(255,255,255,0.05)';this.style.background='rgba(255,255,255,0.02)';this.style.transform='translateX(0)'">
                <div style="width:42px;height:42px;border-radius:12px;
                    background:{bg};
                    display:flex;align-items:center;justify-content:center;
                    color:{color};flex-shrink:0;
                    border:1px solid rgba(255,255,255,0.04)">
                    {icon}
                </div>
                <div>
                    <div style="font-size:14px;font-weight:600;color:#e5e7eb;margin-bottom:2px">{title}</div>
                    <div style="font-size:12px;color:#6b7280;font-weight:400">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Trust line
        st.markdown("")
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;margin-top:8px">
            <div style="display:flex;gap:-4px">
                <div style="width:6px;height:6px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px rgba(34,197,94,0.5)"></div>
            </div>
            <span style="font-size:12px;color:#4b5563;font-weight:500">All systems operational</span>
            <span style="font-size:12px;color:#374151;margin:0 4px">&bull;</span>
            <span style="font-size:12px;color:#4b5563">No AWS costs — fully simulated</span>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT: Auth Card ──
    with col_auth:
        st.markdown("")
        st.markdown("")
        st.markdown("")

        # Glassmorphism card wrapper
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.02);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 24px;
            padding: 8px;
            box-shadow:
                0 32px 64px rgba(0,0,0,0.4),
                0 0 0 1px rgba(255,255,255,0.03) inset,
                0 0 80px rgba(99,102,241,0.03);
        ">
        <!-- inner glow accent -->
        <div style="height:2px;border-radius:24px 24px 0 0;
            background:linear-gradient(90deg,transparent,rgba(99,102,241,0.25),rgba(139,92,246,0.15),transparent);
            margin-bottom:0">
        </div>
        </div>
        """, unsafe_allow_html=True)

        # Auth tabs
        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        with tab_login:
            st.markdown("")
            st.markdown("""
            <div style="margin-bottom:4px">
                <h2 style="font-size:22px;font-weight:700;color:#f9fafb;margin:0;letter-spacing:-0.02em">Welcome back</h2>
                <p style="font-size:14px;color:#6b7280;margin:6px 0 0;font-weight:400">Sign in to access your dashboard</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")

            with st.form("login_form", clear_on_submit=False, border=False):
                login_email = st.text_input("Email", placeholder="you@company.com", key="login_email")
                login_password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
                st.markdown("")
                login_submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")

            if login_submit:
                if not login_email or not login_password:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("Authenticating..."):
                        user, error = login(login_email, login_password)
                        if error:
                            st.error(error)
                        else:
                            st.session_state["auth_user"] = user
                            st.balloons()
                            st.success(f"Welcome back, **{user['full_name']}**!")
                            st.rerun()

        with tab_signup:
            st.markdown("")
            st.markdown("""
            <div style="margin-bottom:4px">
                <h2 style="font-size:22px;font-weight:700;color:#f9fafb;margin:0;letter-spacing:-0.02em">Create account</h2>
                <p style="font-size:14px;color:#6b7280;margin:6px 0 0;font-weight:400">Start scaling in under a minute</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")

            with st.form("signup_form", clear_on_submit=False, border=False):
                signup_name = st.text_input("Full Name", placeholder="John Doe", key="signup_name")
                signup_email = st.text_input("Email", placeholder="you@company.com", key="signup_email")
                signup_password = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="signup_password")

                st.markdown("""
                <p style="font-size:12px;color:#4b5563;margin:4px 0 0;line-height:1.5">
                    By creating an account, you agree to our Terms of Service.
                </p>
                """, unsafe_allow_html=True)
                st.markdown("")
                signup_submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")

            if signup_submit:
                if not signup_name or not signup_email or not signup_password:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("Creating your account..."):
                        user, error = signup(signup_name, signup_email, signup_password)
                        if error:
                            st.error(error)
                        else:
                            st.session_state["auth_user"] = user
                            st.balloons()
                            st.success(f"Welcome to CloudScale, **{user['full_name']}**!")
                            st.rerun()

        # Bottom of card
        st.markdown("""
        <div style="text-align:center;padding:12px 0 4px">
            <span style="font-size:12px;color:#374151">
                Secured with end-to-end encryption
                <span style="margin-left:6px;color:#4b5563">&bull;</span>
                <span style="margin-left:6px;color:#4b5563">SOC 2 Compliant</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    return False

def show_user_sidebar():
    """Show user info and logout in sidebar."""
    user = get_user()
    if not user:
        return

    with st.sidebar:
        st.divider()
        col1, col2 = st.columns([1, 3])
        with col1:
            initial = user['full_name'][0].upper() if user['full_name'] else 'U'
            st.markdown(
                f'<div style="width:38px;height:38px;border-radius:10px;'
                f'background:linear-gradient(135deg,{user.get("avatar_color","#3b82f6")},#6366f1);'
                f'display:flex;align-items:center;justify-content:center;'
                f'color:white;font-weight:700;font-size:16px;margin-top:4px;'
                f'box-shadow:0 2px 8px rgba(99,102,241,0.2)">'
                f'{initial}</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(f"**{user['full_name']}**")
            st.caption(user['email'])

        if st.button("Sign Out", use_container_width=True, key="logout_btn"):
            del st.session_state["auth_user"]
            st.rerun()
