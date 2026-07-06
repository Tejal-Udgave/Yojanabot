import time
from agent import run_agent

print("=" * 70)
print("TEST 1: Scheme Eligibility")
print("=" * 70)

response = run_agent(
    "I am a 24-year-old woman from Pune, Maharashtra. "
    "I want to start a tailoring business from home. "
    "My annual family income is below ₹2 lakh."
)

print(response)

print("\n\n")

print("=" * 70)
#time.sleep(90) 
#print("TEST 2: Follow-up Question")
#print("=" * 70)

#response = run_agent(
#    "What documents do I need for Mudra Loan?",
#    chat_history="""
#User: I am a 24-year-old woman from Pune.
#Assistant: Suggested Mudra Loan and PMEGP.
#"""
#)

#print(response)

#print("\n\n")

#print("=" * 70)
#time.sleep(90) 
#print("TEST 3: Scheme Comparison")
#print("=" * 70)

#response = run_agent(
#    "Compare PMEGP and Mudra Loan.",
#    chat_history="""
#User: I want to start a tailoring business.
#"""
#)

#print(response)