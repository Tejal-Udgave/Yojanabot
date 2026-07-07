import streamlit as st
from agent import run_agent

def format_response(text):
    """Clean up agent response formatting for Streamlit."""
    import re
    
    # Fix bullet points — replace * bullets with -
    text = re.sub(r'^\* ', '- ', text, flags=re.MULTILINE)
    text = re.sub(r'^   \* ', '  - ', text, flags=re.MULTILINE)
    text = re.sub(r'^      \* ', '    - ', text, flags=re.MULTILINE)
    
    # Fix bold headers that lost their spacing
    text = re.sub(r'\*\*(.+?)\*\*', r'**\1**', text)
    
    # Remove duplicate blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text


# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="YojanaBot",
    page_icon="🇮🇳",
    layout="centered"
)

# ─── Header ────────────────────────────────────────────────────
st.title("🇮🇳 YojanaBot")
st.caption("Find government schemes you are eligible for — in your language")

# ─── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 How to use YojanaBot")
    st.markdown("""
    **Step 1:** Describe your situation
    - Your age, gender, state
    - Occupation or business idea
    - Annual family income
    - Category (General/SC/ST/OBC)

    **Step 2:** Get matched schemes

    **Step 3:** Ask followup questions
    - What documents do I need?
    - Where do I apply?
    - Compare two schemes
    - What should I do first?

    **Languages supported:**
    🇮🇳 English · Hindi · Marathi
    """)

    st.divider()

    st.markdown("**Try asking:**")
    
    if st.button("👩 Woman entrepreneur, Maharashtra"):
        st.session_state.pending_input = (
            "I am a 26 year old woman from Nashik, Maharashtra. "
            "I want to start a food business from home. "
            "Annual income below 3 lakhs. General category."
        )

    if st.button("🎓 Student needing scholarship"):
        st.session_state.pending_input = (
            "I am a 20 year old SC category student from rural Karnataka. "
            "Studying engineering. Family income below 1 lakh per year."
        )

    if st.button("👨‍🌾 Farmer needing financial help"):
        st.session_state.pending_input = (
            "I am a 45 year old farmer from Vidarbha, Maharashtra. "
            "I own 2 acres of land and need financial help "
            "for irrigation equipment."
        )

    if st.button("🏠 First time home buyer"):
        st.session_state.pending_input = (
            "I am a 30 year old government employee. "
            "Annual salary 4.5 lakhs. "
            "Want to buy my first home in Pune."
        )

    st.divider()
    st.caption(
        "⚠️ Always verify scheme details on official "
        "government portals before applying."
    )

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_history_text = ""
        st.rerun()

# ─── Initialize Session State ──────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history_text" not in st.session_state:
    st.session_state.chat_history_text = ""

if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""

# ─── Display Chat History ──────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─── Handle Input ──────────────────────────────────────────────
user_input = st.chat_input("Describe your situation or ask about a scheme...")

# If sidebar button was clicked, use that as input
if st.session_state.pending_input and not user_input:
    user_input = st.session_state.pending_input
    st.session_state.pending_input = ""

# ─── Process and Respond ───────────────────────────────────────
if user_input:

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching government schemes..."):
            response = run_agent(
                user_input,
                st.session_state.chat_history_text
            )
        st.markdown(format_response(response))

    # Save to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": format_response(response)
    })

    # Update chat history text for context
    st.session_state.chat_history_text += (
        f"[Previous turn - do not copy this language for future replies]\n"
        f"User: {user_input}\nAssistant: {response}\n\n"
    )

    st.rerun()