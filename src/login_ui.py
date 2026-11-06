"""
Fintech User Authentication UI & Login Dashboard for UPI Financial Wellness Assistant.
Provides a modern dark-themed authentication portal with tabs for Sign In, Account Registration,
and 1-Click Instant Demo Access, plus session status and user profile cards.
"""

import streamlit as st
import auth_manager


def render_login_screen():
    """
    Renders the full-page Fintech Login & Registration Dashboard.
    Shown whenever st.session_state['authenticated'] is False.
    """
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem; margin-bottom: 2rem;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 72px; height: 72px; border-radius: 50%; background: radial-gradient(circle, rgba(0, 229, 255, 0.25) 0%, rgba(3, 15, 63, 0.8) 70%); border: 2px solid #00e5ff; box-shadow: 0 0 25px rgba(0, 229, 255, 0.4); margin-bottom: 12px;">
            <span style="font-size: 2.2rem;">💰</span>
        </div>
        <h1 style="color: #f8fafc; font-weight: 800; font-size: 2.2rem; margin-bottom: 6px; letter-spacing: -0.02em;">
            UPI Financial Wellness Assistant
        </h1>
        <p style="color: #94a3b8; font-size: 1.05rem; max-width: 600px; margin: 0 auto;">
            AI-Driven Spending Forecasts, ML Anomaly Detection & Safe-to-Spend Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Center container for authentication box
    col_l, col_center, col_r = st.columns([1, 2.2, 1])
    with col_center:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(0, 229, 255, 0.25); border-radius: 16px; padding: 6px 20px 20px 20px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);">
        """, unsafe_allow_html=True)

        tab_login, tab_register, tab_demo = st.tabs([
            "🔐 Sign In", 
            "✨ Create Account", 
            "🚀 1-Click Demo"
        ])

        # ----------------- TAB 1: SIGN IN -----------------
        with tab_login:
            st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem; margin-top: 10px; margin-bottom: 15px;'>Enter your credentials to access your financial dashboard:</p>", unsafe_allow_html=True)
            with st.form("form_login"):
                login_user = st.text_input("Username or Email", placeholder="e.g. jashnavi or jashnavi@upiwellness.ai", key="login_u")
                login_pass = st.text_input("Password", type="password", placeholder="••••••••", key="login_p")
                submit_login = st.form_submit_button("Sign In to Dashboard ➔", use_container_width=True)

                if submit_login:
                    if not login_user or not login_pass:
                        st.error("Please enter both username/email and password.")
                    else:
                        success, profile, msg = auth_manager.authenticate(login_user, login_pass)
                        if success and profile:
                            st.session_state["authenticated"] = True
                            st.session_state["user_profile"] = profile
                            st.success(f"✓ {msg}")
                            st.rerun()
                        else:
                            st.error(f"✗ {msg}")

        # ----------------- TAB 2: REGISTER -----------------
        with tab_register:
            st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem; margin-top: 10px; margin-bottom: 15px;'>Create a new account with custom income targets:</p>", unsafe_allow_html=True)
            with st.form("form_register"):
                reg_name = st.text_input("Full Name", placeholder="e.g. Jashnavi", key="reg_fn")
                reg_uname = st.text_input("Username", placeholder="e.g. jashnavi", key="reg_un")
                reg_email = st.text_input("Email Address", placeholder="e.g. user@gmail.com", key="reg_em")
                reg_pass = st.text_input("Choose Password", type="password", placeholder="At least 4 characters", key="reg_pw")
                
                reg_c1, reg_c2 = st.columns(2)
                with reg_c1:
                    reg_income = st.number_input("Monthly Income (₹)", min_value=10000.0, value=75000.0, step=5000.0, key="reg_inc")
                with reg_c2:
                    reg_target = st.number_input("Savings Target (₹)", min_value=5000.0, value=150000.0, step=10000.0, key="reg_tgt")

                submit_reg = st.form_submit_button("Create My Account ✨", use_container_width=True)
                if submit_reg:
                    ok, reg_msg = auth_manager.register_user(
                        username=reg_uname,
                        password=reg_pass,
                        email=reg_email,
                        full_name=reg_name,
                        monthly_income=reg_income,
                        savings_target=reg_target
                    )
                    if ok:
                        st.success(f"✓ {reg_msg}")
                        # Automatically authenticate upon registration
                        _, profile, _ = auth_manager.authenticate(reg_uname, reg_pass)
                        if profile:
                            st.session_state["authenticated"] = True
                            st.session_state["user_profile"] = profile
                            st.rerun()
                    else:
                        st.error(f"✗ {reg_msg}")

        # ----------------- TAB 3: 1-CLICK DEMO -----------------
        with tab_demo:
            st.markdown("<p style='color: #cbd5e1; font-size: 0.95rem; margin-top: 10px; margin-bottom: 15px;'>Instant evaluation access without manual typing:</p>", unsafe_allow_html=True)
            
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                st.markdown("""
                <div style="background: rgba(3, 15, 63, 0.6); padding: 12px; border-radius: 10px; border: 1px solid rgba(0, 229, 255, 0.3); margin-bottom: 10px;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #f8fafc;">🌟 Jashnavi</div>
                    <div style="font-size: 0.8rem; color: #00e5ff;">Premium User • ₹85k/mo</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">Role: Admin & Analyst</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🚀 Login as Jashnavi", use_container_width=True, key="btn_demo_jashnavi"):
                    ok, profile, _ = auth_manager.authenticate("jashnavi", "admin123")
                    if ok and profile:
                        st.session_state["authenticated"] = True
                        st.session_state["user_profile"] = profile
                        st.rerun()

            with d_col2:
                st.markdown("""
                <div style="background: rgba(3, 15, 63, 0.6); padding: 12px; border-radius: 10px; border: 1px solid rgba(0, 229, 255, 0.3); margin-bottom: 10px;">
                    <div style="font-size: 1.1rem; font-weight: 700; color: #f8fafc;">👤 Demo Analyst</div>
                    <div style="font-size: 0.8rem; color: #00e5ff;">Standard User • ₹60k/mo</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">Role: Standard Testing</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("💼 Login as Demo", use_container_width=True, key="btn_demo_analyst"):
                    ok, profile, _ = auth_manager.authenticate("demo", "demo123")
                    if ok and profile:
                        st.session_state["authenticated"] = True
                        st.session_state["user_profile"] = profile
                        st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Feature Value Highlights Grid
    st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); text-align: center;">
            <div style="font-size: 1.8rem; margin-bottom: 6px;">🛡️</div>
            <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">Safe-to-Spend</div>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 4px;">Dynamic daily budget ceiling computed from recurring cashflow.</div>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); text-align: center;">
            <div style="font-size: 1.8rem; margin-bottom: 6px;">📈</div>
            <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">ML Forecasting</div>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 4px;">Multi-month predictive spending regression & Random Forest models.</div>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); text-align: center;">
            <div style="font-size: 1.8rem; margin-bottom: 6px;">🚨</div>
            <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">Anomaly Detection</div>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 4px;">Isolation Forest algorithms detecting suspicious or runaway expenses.</div>
        </div>
        """, unsafe_allow_html=True)

    with f4:
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); text-align: center;">
            <div style="font-size: 1.8rem; margin-bottom: 6px;">🤖</div>
            <div style="font-weight: 700; color: #f8fafc; font-size: 0.95rem;">AI Chatbot Copilot</div>
            <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 4px;">Conversational financial advisor grounded directly in your UPI ledger.</div>
        </div>
        """, unsafe_allow_html=True)


def logout_user():
    """Clears authentication session state and reloads the login portal."""
    st.session_state["authenticated"] = False
    st.session_state["user_profile"] = None
    st.rerun()


def render_sidebar_profile():
    """Renders user profile card and logout button in the sidebar."""
    profile = st.session_state.get("user_profile")
    if not profile:
        return

    avatar = profile.get("avatar", "👤")
    name = profile.get("full_name", profile.get("username", "User"))
    role = profile.get("role", "Standard Member")
    income = profile.get("monthly_income", 0.0)
    target = profile.get("savings_target", 0.0)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(3, 15, 63, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%); 
                border: 1px solid rgba(0, 229, 255, 0.35); border-radius: 12px; padding: 12px 14px; margin-bottom: 15px; 
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="font-size: 1.6rem; background: rgba(0, 229, 255, 0.15); width: 40px; height: 40px; 
                        display: flex; align-items: center; justify-content: center; border-radius: 50%; 
                        border: 1px solid #00e5ff;">
                {avatar}
            </div>
            <div style="overflow: hidden;">
                <div style="font-weight: 700; color: #f8fafc; font-size: 1rem; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{name}</div>
                <div style="font-size: 0.74rem; color: #00e5ff; font-weight: 600;">{role}</div>
            </div>
        </div>
        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255, 255, 255, 0.08); font-size: 0.78rem; color: #94a3b8;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                <span>Monthly Target:</span>
                <span style="color: #38bdf8; font-weight: 600;">₹{income:,.0f}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Savings Goal:</span>
                <span style="color: #4ade80; font-weight: 600;">₹{target:,.0f}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Sign Out", use_container_width=True, key="btn_logout_sidebar"):
        logout_user()


def render_topbar_user_badge():
    """Renders a compact user identity badge for the global top bar."""
    profile = st.session_state.get("user_profile")
    if not profile:
        return

    avatar = profile.get("avatar", "👤")
    name = profile.get("full_name", profile.get("username", "User"))
    role = profile.get("role", "Member")

    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: flex-end; gap: 8px; height: 100%; padding-top: 2px;">
        <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(0, 229, 255, 0.25); border-radius: 20px; padding: 4px 12px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);">
            <span style="font-size: 1rem;">{avatar}</span>
            <span style="font-size: 0.85rem; font-weight: 600; color: #f8fafc;">{name}</span>
            <span style="font-size: 0.68rem; background: rgba(0, 229, 255, 0.18); color: #00e5ff; padding: 2px 6px; border-radius: 8px; font-weight: 600;">{role}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

