# Standard Python libraries
import os

# Load environment variables from .env
from dotenv import load_dotenv

# Gemini LLM
from langchain_google_genai import ChatGoogleGenerativeAI

# Google Search (SerpAPI)
from langchain_community.utilities import SerpAPIWrapper

# Tool wrapper
#from langchain.tools import Tool
from langchain_core.tools import Tool

# LangChain Agent
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)

# Prompt Template
from langchain.prompts import PromptTemplate
#from langchain import hub

# Load variables from .env
load_dotenv()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

# Initialize SerpAPI search
search = SerpAPIWrapper(
    serpapi_api_key=os.getenv("SERPAPI_API_KEY")
)

SYSTEM_PROMPT = """
You are YojanaBot, an AI assistant that helps Indian citizens discover
and understand Central and State Government schemes they may be eligible for.

=========================
YOUR RESPONSIBILITIES
=========================

1. Understand the user's profile by identifying:
   - Age
   - Gender
   - Occupation
   - State
   - Annual Income
   - Category (General/SC/ST/OBC/EWS)
   - Any other relevant information

2. Find the most relevant government schemes based on the user's profile.

3. Clearly explain WHY the user is eligible (or possibly eligible).

4. Answer follow-up questions about:
   - Required documents
   - Application process
   - Official application portals
   - Benefits
   - Eligibility criteria
   - Scheme comparisons
   - "What should I do first?"

5. Maintain context across the conversation so users do not need to repeat
   their information.

=========================
SEARCH BEHAVIOR
=========================

You have access to search tools.

Whenever current or scheme-specific information is required,
use the available search tool.

When searching, prioritize information in this order:

1. myscheme.gov.in
2. india.gov.in
3. Official Government Ministry websites (.gov.in)
4. Official State Government websites (.gov.in)

Avoid relying on blogs, forums, news articles, or unofficial websites unless
no official information is available.

=========================
RESPONSE GUIDELINES
=========================

- Respond in the SAME language the user writes in.
- Use simple, clear language anyone can understand.
- Explain eligibility instead of simply saying "Eligible" or "Not Eligible."
- Never invent or guess information.
- If information cannot be verified, clearly mention that.
- Include official website links whenever available.
- Prefer structured responses over long paragraphs.

=========================
OUTPUT FORMAT
=========================

For scheme recommendations:

**Scheme Name**

• Benefits:
• Why You Are Eligible:
• Eligibility Criteria:
• Required Documents:
• How to Apply:
• Official Website:

-------------------------

For comparisons:

| Feature | Scheme A | Scheme B |
|---------|----------|----------|
| Benefits | | |
| Eligibility | | |
| Financial Assistance | | |
| Required Documents | | |
| Best Suited For | | |

After the comparison, recommend the better option based on the user's profile.

-------------------------

For "What should I do first?" questions:

Provide a numbered action plan.

For example:

1. Collect required documents.
2. Verify eligibility.
3. Visit the official portal.
4. Complete the application.
5. Track the application status.

=========================
IMPORTANT RULES
=========================

- Be honest about uncertainty.
- Never fabricate scheme details.
- Never fabricate eligibility conditions.
- Never fabricate official websites.
- Always encourage users to verify important information on official
  government portals before applying.

End every response with:

"What would you like to know more about?"
"""

tools = [
    Tool(
        name="GovernmentSchemeSearch",
        func=search.run,
        description=SYSTEM_PROMPT + """
        Use this tool to search for Indian government schemes,eligibility criteria, required documents,
        application process, official portals,
        and government notifications.

        Always prefer official government websites such as:
        - myscheme.gov.in
        - india.gov.in
        - official ministry websites (.gov.in)

        Ignore blogs and unofficial websites whenever possible.
        """
    )
]

#prompt = PromptTemplate.from_template(
#    SYSTEM_PROMPT + """

#Available Tools:
#{tools}

#Tool Names:
#{tool_names}

#Conversation History:
#{chat_history}

#User:
#{input}

#{agent_scratchpad}
#"""
#)

#prompt = hub.pull("hwchase17/react",dangerously_pull_public_prompt=True)
#os.environ["LANGCHAIN_HUB_UNSAFE_DESERIALIZATION"] = "true"
#prompt = hub.pull("hwchase17/react")

react_template = """You are a helpful assistant. Answer the following question using the tools available.

You have access to the following tools:

{tools}

STRICT FORMAT RULES - YOU MUST FOLLOW THIS EXACTLY:

Thought: [your reasoning]
Action: [tool name from {tool_names}]
Action Input: [input to tool]
Observation: [tool result]
Thought: [reasoning after observation]
Final Answer: [your complete answer here]

IMPORTANT: Always end with "Final Answer:" followed by your complete response.
Never skip the "Final Answer:" line.
Never respond outside this format.

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(react_template)

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=3,
    handle_parsing_errors="Check your output and make sure it follows the correct format. Use Action: and Action Input: properly."
)

def run_agent(user_input, chat_history=""):
    """
    Runs the YojanaBot agent and returns the response.
    """

    try:
        result = agent_executor.invoke(
            {
                "input": user_input,
                "chat_history": chat_history
            }
        )

        return result["output"]

    except Exception as e:
        error_str = str(e)
        # Extract answer from parsing error if present
        if "Could not parse LLM output:" in error_str:
            start = error_str.find("`") + 1
            end = error_str.rfind("`")
            if start > 0 and end > start:
                return error_str[start:end]
            
        print(e)   # useful while debugging
        return (
            "Sorry! Something went wrong while processing your request. "
            "Please try again."
        )