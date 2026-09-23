import os
import time
import requests
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError
if "GOOGLEAPIKEY" in os.environ:
    st.get_option._config_options = st.get_option._config_options or {}
    st.secrets["GOOGLEAPIKEY"] = os.environ["GOOGLEAPIKEY"]
    st.secrets["GOOGLEAPIKEY"] = os.environ["GOOGLEAPIKEY"]

if "PAYSTACKSECRETKEY" in os.environ:
    st.secrets["PAYSTACKSECRETKEY"] = os.environ["PAYSTACKSECRETKEY"]
import uuid
st.markdown(
    """
    <style>
    textarea[data-testid="stChatInputTextArea"] {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    div[data-testid="stChatInput"] {
        background-color: #1E1E1E !important;
        border: 1px solid #444444 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
import streamlit.components.v1 as components

# =====================================================================
# 1. PLATFORM CONFIGURATIONS & CORPORATE BRAIDING
# =====================================================================
st.set_page_config(page_title="King Nath Academy ", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #009688; color: white; font-weight: bold; }
    .stChatInput { border-radius: 20px; }
    .premium-badge { background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%); color: #0f172a; padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 King Nath Academy ")
st.caption("Official Educational Intelligence Engine — Powered by KNA Core")

# =====================================================================
# 2. ENCRYPTED PAYMENT INTEGRATION TOKENS
# =====================================================================
GOOGLEAPIKEY = st.secrets["GOOGLEAPIKEY"] # Paste your Google AI Studio Key here

# Replace these strings with your official keys from ://paystack.com
PAYSTACK_PUBLIC_KEY = pk_test_3a458555d53c5d8bfe36aa3cb9cd5a6508058160
PAYSTACK_SECRET_KEY = st.secrets["SECRET"]

# =====================================================================
# 3. COMPONENT INSTANTIATION & PERSISTENCE MANAGEMENT
# =====================================================================
if "ai_client" not in st.session_state:
    st.session_state.ai_client = genai.Client(api_key=GOOGLEAPIKEY)

client = st.session_state.ai_client

# Initialize Premium validation trackers
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False
if "paystack_ref" not in st.session_state:
    st.session_state.paystack_ref = None

# Set model layer configurations according to user billing tier
active_model = "gemini-3.6-pro" if st.session_state.is_premium else "gemini-3.6-flash"


# =====================================================================
# 4. SIDEBAR ACCOUNT MANAGER & PAYSTACK ROUTER
# =====================================================================
st.sidebar.header("👤 Account Status")

if st.session_state.is_premium:
    st.sidebar.markdown('<span class="premium-badge">🌟 PRO PLAN ENABLED</span>', unsafe_allow_html=True)
    st.sidebar.success("Account optimized with Go Pro with KNA tier!")
    st.sidebar.markdown("""
    **Active Premium Privileges:**
    * 🧠 **Pro Engine Integration:** Complex computer math & programming.
    * ⚡ **Zero Speed Limits:** High priority server bandwidth allocations.
    * 📖 **Academy Module Access:** Structural guidance & step-by-step reasoning logs.
    """)
else:
    st.sidebar.markdown('<span style="background-color:#475569; color:white; padding:4px 10px; border-radius:12px;">Standard Access</span>', unsafe_allow_html=True)
    st.sidebar.warning("Running standard model layers. Upgrade to unlock full reasoning parameters.")
    
    # Trigger button for the Go Pro with KNA portal
    if st.sidebar.button("🚀 Go Pro with KNA"):
        # Generate an absolute, unique transaction reference for Nigerian Banking rails
        st.session_state.paystack_ref = f"KNA-{uuid.uuid4().hex[:10].upper()}"
        
        # Define user credentials for checkout initialization
        customer_email = "student@kingnathacademy.com"
        tuition_amount_kobo = 500000  # ₦5,000.00 (Paystack measures values in Kobo, so multiply Naira by 100)
        
        # Inject raw Paystack Inline HTML/JS engine block securely into Streamlit frame
        paystack_iframe_code = f"""
        <html>
        <head>
            <script src="https://js.paystack.co/v2/inline.js"></script>
        </head>
        <body style="background-color: transparent; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh;">
            <button onclick="payWithPaystack()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; font-size: 16px; font-weight: bold; border: none; padding: 15px 30px; border-radius: 8px; cursor: pointer; width: 100%; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                Securely Pay ₦5,000 via Paystack
            </button>
            <script>
                function payWithPaystack() {{
                    const popup = new PaystackPop();
                    popup.newTransaction({{
                        key: '{PAYSTACK_PUBLIC_KEY}',
                        email: '{customer_email}',
                        amount: {tuition_amount_kobo},
                        ref: '{st.session_state.paystack_ref}',
                        currency: 'NGN',
                        onSuccess: function(transaction) {{
                            parent.postMessage({{type: 'PAYSTACK_SUCCESS', ref: transaction.reference}}, '*');
                        }},
                        onCancel: function() {{
                            parent.postMessage({{type: 'PAYSTACK_CANCEL'}}, '*');
                        }}
                    }});
                }}
            </script>
        </body>
        </html>
        """
        st.sidebar.components.v1.html(paystack_iframe_code, height=120)

# Listen to structural transaction callbacks coming from our embedded Paystack engine 
if st.session_state.paystack_ref and not st.session_state.is_premium:
    st.sidebar.info("Awaiting payment routing validation details...")
    
    # Verification trigger button to query backend ledgers
    if st.sidebar.button("🔄 Confirm My Payment Status"):
        with st.spinner("Reaching Paystack security ledgers to verify fund transfer..."):
            try:
                # Call Paystack endpoint using the private server key
                headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
                verify_url = f"https://paystack.co{st.session_state.paystack_ref}"
                response = requests.get(verify_url, headers=headers).json()
                
                # Double-check that money actually entered your bank vault successfully
                if response.get("status") and response["data"]["status"] == "success":
                    st.session_state.is_premium = True
                    st.sidebar.success("🎉 Payment verified! Welcome to King Nath Academy Pro!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Paystack records show this payment is incomplete. Please finish the payment window or try again.")
            except Exception as err:
                st.sidebar.error(f"Failed to reach server: {str(err)}")

# Global reset option
if st.sidebar.button("🗑️ Reset Chat Canvas"):
    for key in ["chat_session", "messages"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# =====================================================================
# 5. CORE BRAIN ARCHITECTURE & LOGICAL SYSTEM
# =====================================================================
SYSTEM_PROMPT = f"""
You are the proprietary AI engine for King Nath Academy (KNA), matching elite DeepSeek-level precision.
Your environment layer is currently configured to: {active_model}.
If active_model is 'gemini-2.5-pro', you must show highly advanced, deep academic reasoning, extreme software programming architectures, and precise calculations matching ChatGPT Plus levels.
If active_model is 'gemini-2.5-flash', limit text structures to brief, accurate answers, occasionally advising the user to click 'Go Pro with KNA' in the sidebar to view full breakdowns.
Always interact using a sharp, friendly, smart academic tone with helpful  contextworld wide.
"""

if "chat_session" not in st.session_state or st.session_state.chat_session._model != active_model:
    st.session_state.chat_session = client.chats.create(
        model=active_model,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    )
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display current message chain on layout view
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# Show login screen if they aren't signed in yet
if not st.session_state.authenticated:
    st.title("🔐 King Nath Academy Portal")
    st.subheader("Please sign in to access the intelligence database")
    
    # Simple, clean login input fields
    email_input = st.text_input("Enter your registered email address:", placeholder="name@example.com")
    
    if st.button("Sign In", type="primary"):
        if email_input.strip() != "" and "@" in email_input:
            # Save authentication details to the running session state
            st.session_state.authenticated = True
            st.session_state.user_email = email_input.strip()
            
            # (Optional) Set up premium status based on database or payment records
            st.session_state.is_premium = True 
            
            st.success("Successfully authenticated! Loading terminal matrices...")
            st.rerun()
        else:
            st.error("Please enter a valid email address.")
            
    # Stop executing the rest of the file so the chat stays hidden until logged in
    st.stop()

# --- Everything below this line will only run AFTER they sign in ---
st.sidebar.caption(f"Logged in as: {st.session_state.user_email}")
if st.sidebar.button("Sign Out"):
    st.session_state.authenticated = False
    st.session_state.user_email = ""
    st.rerun()

# Process input channels
import time

from google.genai.errors import APIError

# Initialize state trackers at the top of your script if not already present
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

# Render existing conversation history up to this point
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT HANDLING ---
if user_input := st.chat_input("Interact with King Nath Academy intelligence database..."):
    # 1. Immediately increment the question count
    st.session_state.question_count += 1
    
    # 2. Render the user's question on screen
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 3. Check Gate: If this is their 2nd or later question AND they aren't signed in, BLOCK THEM
    if st.session_state.question_count > 1 and not st.session_state.authenticated:
        with st.chat_message("assistant"):
            st.warning("🔐 You have used your 1 free query. Please sign in to unlock unlimited access and view this answer.")
            
            # Show inline sign-in fields right inside the chat window
            email_input = st.text_input("Enter your registered email address:", key="gate_email", placeholder="name@example.com")
            if st.button("Sign In to Continue", type="primary"):
                if email_input.strip() != "" and "@" in email_input:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email_input.strip()
                    st.success("Successfully authenticated! Processing your query...")
                    st.rerun()
                else:
                    st.error("Please enter a valid email address.")
        st.stop() # Prevents the AI execution until they click the button and pass validation

    # 4. If they pass the check (1st free question OR already logged in), process the response
    with st.chat_message("assistant"):
        with st.status("Processing request matrices...", expanded=True) as status:
            max_retries = 3
            response_text = None
            
            for attempt in range(max_retries):
                try:
                    response = st.session_state.chat_session.send_message(user_input)
                    response_text = response.text
                    status.update(label="Response generated!", state="complete", expanded=False)
                    break 
                except APIError as e:
                    if e.code == 503 and attempt < max_retries - 1:
                        status.update(label=f"Servers busy. Retrying attempt {attempt + 1}/{max_retries}...")
                        time.sleep(2)
                    else:
                        status.update(label="Pipeline error encountered", state="error")
                        st.error(f"Pipeline error: {e.message} (Code {e.code})")
                        break
                except Exception as e:
                    status.update(label="Pipeline error encountered", state="error")
                    st.error(f"Pipeline error: {str(e)}.")
                    break
            
            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                st.error("Could not establish a stable pipeline connection. Please try typing your message again.")
