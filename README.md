# YojanaBot — AI Agent for Government Scheme Discovery

> An agentic AI system that helps Indian citizens discover government schemes they are eligible for, answer follow-up questions, and navigate the application process — in their own language.

**Live Demo:** [https://yojanabot-ai.streamlit.app](#)

---

##  Problem Statement

Millions of Indian citizens miss out on government schemes they are eligible for — not because the schemes don't exist, but because:

- Awareness is limited, especially in semi-urban and rural areas
- Government portals are complex and hard to navigate
- Information is scattered across dozens of central and state websites
- Language barriers prevent many citizens from accessing scheme details

There is no single tool that takes a person's situation, matches them to relevant schemes, and answers their follow-up questions in a conversational, accessible way.

---

##  Solution

YojanaBot is a **multi-turn agentic AI system** that:

1. Takes a natural language description of the user's situation
2. Autonomously searches the web for relevant government schemes
3. Matches and explains eligibility in simple language
4. Answers follow-up questions about documents, application process, deadlines, and scheme comparisons
5. Responds in the user's preferred language — English, Hindi, or Marathi

---

##  Agent Design

YojanaBot uses the **ReAct (Reason + Act)** pattern:

```
User Query
    ↓
Thought: What does this user need?
    ↓
Action: Search for relevant schemes
    ↓
Observation: Read and process search results
    ↓
Thought: Do I have enough information?
    ↓
Final Answer: Structured scheme recommendations
```

The agent autonomously decides:
- **What to search** — based on user profile (age, income, state, category, occupation)
- **When to search again** — if the first result is insufficient
- **How to present** — structured format with benefits, eligibility, documents, and official links

This multi-step reasoning is what distinguishes YojanaBot from a simple chatbot or search wrapper.

---

##  Features

- **Scheme Eligibility Matching** — describes situation in natural language, gets matched schemes
- **Multi-turn Conversation** — ask follow-up questions without repeating your profile
- **Document Guidance** — get exact list of documents needed for any scheme
- **Application Process** — step-by-step guidance on how and where to apply
- **Scheme Comparison** — compare two schemes side by side with a recommendation
- **Action Planning** — "What should I do first?" gives a prioritized step-by-step plan
- **Bilingual Support** — responds in English, Hindi, or Marathi based on user's input
- **Example Prompts** — one-click example buttons for common user types

---

##  Tech Stack

| Component | Technology |
|---|---|
| LLM | Google Gemini 2.5 Flash |
| Agent Framework | LangChain 0.3.27 (ReAct Agent) |
| Web Search | SerpAPI |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |
| Language | Python 3.10+ |

---

##  Architecture

```
User (Streamlit UI)
        ↓
    app.py
        ↓
    run_agent()
        ↓
  LangChain ReAct Agent
        ↓
  Gemini 2.5 Flash (LLM)
        ↓
  GovernmentSchemeSearch Tool
        ↓
  SerpAPI → Google Search
        ↓
  Official Government Portals
  (myscheme.gov.in, india.gov.in, .gov.in)
```

---

##  Project Structure

```
yojanabot/
├── agent.py          ← Agent brain (ReAct agent, tools, prompt)
├── app.py            ← Streamlit UI
├── requirements.txt  ← Dependencies
├── .env              ← API keys (not pushed to GitHub)
├── .gitignore
└── README.md
```

---

##  Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/Tejal-Udgave/Yojanabot
cd yojanabot
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up API keys**

Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

Get your keys:
- Gemini API → [aistudio.google.com](https://aistudio.google.com) (free)
- SerpAPI → [serpapi.com](https://serpapi.com) (100 free searches/month)

**5. Run the app**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

##  Example Interactions

**Scheme Discovery:**
```
User: I am a 24 year old woman from Pune, Maharashtra. I want to 
      start a tailoring business from home. Family income below 2 lakhs.

YojanaBot: Based on your profile, here are relevant schemes:

**Pradhan Mantri Mudra Yojana (PMMY)**
• Benefits: Collateral-free loans up to ₹10 lakh (Shishu: up to ₹50,000)
• Why You Are Eligible: Woman starting a micro-enterprise in non-farm sector
• Official Website: mudra.org.in
...
```

**Follow-up Question:**
```
User: What documents do I need for Mudra Loan?

YojanaBot: For Mudra Loan you will need:
• Identity Proof: Aadhaar Card, PAN Card, Voter ID
• Address Proof: Utility bills, Aadhaar
• Business Proof: Registration certificate (if applicable)
• Bank statements: Last 6 months
...
```

**Hindi Support:**
```
User: मुझे सिंचाई के लिए कौन सी योजना मिल सकती है?

YojanaBot: प्रधानमंत्री कृषि सिंचाई योजना (PMKSY) आपके लिए उपयुक्त है...
```

---

##  Future Enhancements

- **RAG Integration** — pre-load official scheme PDFs into a vector database for faster, more accurate responses
- **State-specific filtering** — dedicated search paths for each state's schemes
- **Voice input support** — accessibility for users with low literacy
- **WhatsApp integration** — reach users where they already are
- **Scheme deadline alerts** — notify users of upcoming application deadlines
- **PDF export** — download scheme summary as a document

---

##  Disclaimer

YojanaBot provides information for awareness purposes only. Always verify scheme details on official government portals before applying. Scheme eligibility criteria and benefits may change. For the most accurate information, visit [myscheme.gov.in](https://www.myscheme.gov.in).

---

##  Built By

**Tejal Udgave**
BTech Information Technology, MKSSS Cummins College of Engineering for Women, Pune

---

##  License

This project was built for educational purposes.

⭐ If you found this useful, consider giving it a star!
