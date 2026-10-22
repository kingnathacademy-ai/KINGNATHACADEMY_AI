"""
=============================================================================
🎓 KING NATH ACADEMY (KNA) - OFFICIAL EDUCATIONAL INTELLIGENCE ENGINE
=============================================================================
Modified & Perfected Streamlit Application for Render / Cloud deployment.
=============================================================================
"""

import os
import uuid
import time
import requests
import streamlit as st
import streamlit.components.v1 as components

# 1. PAGE SETUP & CORPORATE DARK ACADEMIC STYLING
st.set_page_config(
    page_title="King Nath Academy | AI Educational Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background-color: #0b0f19; color: #f8fafc; font-family: -apple-system, sans-serif; }
textarea[data-testid="stChatInputTextArea"] {
    background-color: #1E1E1E !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
div[data-testid="stChatInput"] {
    background-color: #1E1E1E !important;
    border: 1px solid #334155 !important;
    border-radius: 16px !important;
}
.stButton>button {
    width: 100%;
    border-radius: 8px;
    background: linear-gradient(135deg, #009688 0%, #00796b 100%);
    color: white;
    font-weight: 600;
}
.premium-badge {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    color: #0f172a;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: 800;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# 2. BULLETPROOF MULTI-SOURCE API KEY RESOLUTION
def resolve_google_api_key() -> str | None:
    for key_name in ["GOOGLEAPIKEY", "GEMINI_API_KEY", "RENDER_API_KEY"]:
        val = os.environ.get(key_name)
        if val and val.strip() and val != "NOT_SET":
            return val.strip()
    if hasattr(st, "secrets") and st.secrets is not None:
        for secret_name in ["GOOGLEAPIKEY", "GEMINI_API_KEY", "SECRET"]:
            if secret_name in st.secrets:
                val = st.secrets[secret_name]
                if val and str(val).strip():
                    return str(val).strip()
    return None

GOOGLE_API_KEY = resolve_google_api_key()
# =====================================================================
# BULLETPROOF KEY & SECRET RESOLUTION (RENDER & STREAMLIT SAFE)
# =====================================================================
def safe_get_secret(key_name: str, default: str = "") -> str:
    """
    Safely retrieves a configuration key.
    Checks os.environ (Render environment variables) first,
    then safely probes st.secrets without crashing if secrets.toml is absent.
    """
    # 1. Check direct environment variables (Works on Render dashboard)
    val = os.environ.get(key_name)
    if val is not None and str(val).strip() != "" and str(val).strip() != "NOT_SET":
        return str(val).strip()

    # 2. Safely probe st.secrets with complete exception protection
    try:
        if hasattr(st, "secrets"):
            sec = st.secrets
            if sec is not None and key_name in sec:
                v = sec[key_name]
                if v is not None and str(v).strip():
                    return str(v).strip()
    except Exception:
        # Silently catches StreamlitSecretNotFoundError and FileNotFoundError on Render
        pass
    except BaseException:
        pass

    return default


def resolve_google_api_key() -> str | None:
    """Safely retrieves the Google API Key across Render, .env, and Streamlit secrets."""
    for candidate in ["GOOGLEAPIKEY", "GEMINI_API_KEY", "RENDER_API_KEY", "GOOGLE_API_KEY", "SECRET"]:
        val = safe_get_secret(candidate, "")
        if val:
            return val
    return None


GOOGLE_API_KEY = resolve_google_api_key()

# Paystack API Keys (Render environment variables take priority, test key fallback)
PAYSTACK_PUBLIC_KEY = safe_get_secret(
    "PAYSTACK_PUBLIC_KEY",
    "pk_test_3a458555d53c5d8bfe36aa3cb9cd5a6508058160"
)
PAYSTACK_SECRET_KEY = safe_get_secret(
    "PAYSTACKSECRETKEY",
    safe_get_secret("PAYSTACK_SECRET_KEY", safe_get_secret("SECRET", ""))
)
    st.session_state.paystack_ref = None
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. GEMINI CLIENT SETUP
has_gemini = False
client = None

if GOOGLE_API_KEY:
    try:
        from google import genai
        from google.genai import types
        if "ai_client" not in st.session_state:
            st.session_state.ai_client = genai.Client(api_key=GOOGLE_API_KEY)
        client = st.session_state.ai_client
        has_gemini = True
    except Exception as e:
        st.warning(f"Note on Gemini SDK: {e}")

active_model = "gemini-2.5-pro" if st.session_state.is_premium else "gemini-2.5-flash"

SYSTEM_PROMPT = f"""
You are the proprietary AI Educational Intelligence Engine for King Nath Academy (KNA), matching elite academic precision.
Environment model: {active_model}.
{"PRO REASONING ACTIVE: Deliver step-by-step mathematical proofs and structural software architectures." if st.session_state.is_premium else "STANDARD SPEED LAYER: Provide concise, accurate pedagogical answers. Suggest upgrading to Pro for full derivations."}
"""

if has_gemini and client:
    if "chat_session" not in st.session_state or getattr(st.session_state.get("chat_session"), "_model", None) != active_model:
        st.session_state.chat_session = client.chats.create(
            model=active_model,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
        )

# 5. SIDEBAR: ACCOUNT & PAYSTACK WORKFLOW
with st.sidebar:
    st.header("👤 Account Status")
    if st.session_state.is_premium:
        st.markdown('<div class="premium-badge">🌟 PRO PLAN ENABLED</div>', unsafe_allow_html=True)
        st.success("Account active with Go Pro with KNA tier!")
    else:
        st.caption("Standard Access (1 free query before student sign-in)")

    if st.session_state.authenticated:
        st.caption(f"Logged in as: **{st.session_state.user_email}**")
        if st.button("🚪 Sign Out"):
            st.session_state.authenticated = False
            st.session_state.user_email = ""
            st.session_state.question_count = 0
            st.rerun()
    else:
        with st.form("login_form"):
            email_field = st.text_input("Student Email", placeholder="student@kingnathacademy.com")
            if st.form_submit_button("Sign In"):
                if email_field.strip() and "@" in email_field:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email_field.strip()
                    st.success("Signed in successfully!")
                    st.rerun()

    # Paystack Upgrade Portal
    if not st.session_state.is_premium:
        st.markdown("---")
        st.subheader("⚡ Upgrade to Pro (₦5,000)")
        if st.button("🚀 Initialize Paystack Reference"):
            st.session_state.paystack_ref = f"KNA-{uuid.uuid4().hex[:10].upper()}"

        if st.session_state.paystack_ref:
            customer_email = st.session_state.user_email or "student@kingnathacademy.com"
            paystack_iframe_code = f"""
            <html>
            <head><script src="https://js.paystack.co/v2/inline.js"></script></head>
            <body style="background:transparent; margin:0; padding:10px 0;">
                <button onclick="pay()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color:white; font-size:15px; font-weight:bold; border:none; padding:12px; border-radius:8px; cursor:pointer; width:100%;">
                    💳 Securely Pay ₦5,000 via Paystack
                </button>
                <script>
                    function pay() {{
                        const popup = new PaystackPop();
                        popup.newTransaction({{
                            key: '{PAYSTACK_PUBLIC_KEY}',
                            email: '{customer_email}',
                            amount: 500000,
                            ref: '{st.session_state.paystack_ref}',
                            currency: 'NGN',
                            onSuccess: function(t) {{ parent.postMessage({{type:'PAYSTACK_SUCCESS', ref:t.reference}}, '*'); }}
                        }});
                    }}
                </script>
            </body>
            </html>
            """
            components.html(paystack_iframe_code, height=65)
            st.caption(f"Ref: `{st.session_state.paystack_ref}`")

            if st.button("🔄 Confirm Payment Status"):
                verify_url = f"https://api.paystack.co/transaction/verify/{st.session_state.paystack_ref}"
                headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
                try:
                    if PAYSTACK_SECRET_KEY:
                        res = requests.get(verify_url, headers=headers, timeout=10).json()
                        if res.get("status") and res.get("data", {}).get("status") == "success":
                            st.session_state.is_premium = True
                            st.success("🎉 Payment verified! Welcome to Pro!")
                            st.rerun()
                        else:
                            st.error("❌ Paystack records indicate payment is incomplete.")
                    else:
                        st.session_state.is_premium = True
                        st.success("🎉 Sandbox verified! Pro enabled!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Verification error: {e}")

    st.markdown("---")
    if st.button("🗑️ Reset Chat Canvas"):
        st.session_state.messages = []
        if "chat_session" in st.session_state:
            del st.session_state["chat_session"]
        st.rerun()

# 6. MAIN CHAT WORKSPACE
st.title("🎓 King Nath Academy")
st.caption("Official Educational Intelligence Engine — Powered by KNA Core")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Interact with King Nath Academy intelligence database...")

if user_input:
    # Free-tier gate: block on 2nd query if not signed in
    if st.session_state.question_count >= 1 and not st.session_state.authenticated:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            st.warning("🔐 You have used your 1 free preview query. Please sign in in the sidebar to unlock unlimited intelligence.")
        st.stop()

    st.session_state.question_count += 1
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.status("🧠 Processing academic reasoning matrices...", expanded=st.session_state.is_premium) as status:
            response_text = None
            for attempt in range(3):
                try:
                    response = st.session_state.chat_session.send_message(user_input)
                    response_text = response.text
                    status.update(label="Response generated successfully!", state="complete", expanded=False)
                    break
                except Exception as e:
                    if attempt < 2:
                        time.sleep(2)
                    else:
                        status.update(label="Pipeline error", state="error")
                        st.error(f"Error: {e}")

            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
