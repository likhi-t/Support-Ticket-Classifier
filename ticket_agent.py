import os
import json
from groq import Groq
from groq.types.chat import ChatCompletion
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv


load_dotenv()
try:
    client = Groq()
except Exception:
    pass 

CLASSIFICATION_MODEL = "openai/gpt-oss-120b"
REPLY_DRAFTING_MODEL = "llama-3.3-70b-versatile" 
COMPANY_NAME = "Prospello.ai (pls dont sue)"


TicketCategory = Literal["Billing", "Technical_Bug", "Feature_Request", "Account_Issue", "General_Inquiry"]
PriorityLevel = Literal["Low", "Medium", "High", "Critical"]

class TicketClassification(BaseModel):
    """Schema for classifying a support ticket."""
    category: TicketCategory = Field(description="The primary category of the support issue.")
    priority: PriorityLevel = Field(description="The severity and urgency of the ticket.")
    summary: str = Field(description="A concise one-sentence summary of the user's request.")


def classify_ticket(ticket_text: str) -> dict:
    category_guide = """
    ## REFERENCE CATEGORY GUIDE (Use these definitions for classification)
    - **Billing:** Issues related to payments, double charges, refund status, or incorrect invoices.
    - **Technical_Bug:** Unexpected software behavior, crashes, broken links, or API failures.
    - **Feature_Request:** Suggestions for new functionality, UI/UX improvements, or missing features.
    - **Account_Issue:** Problems with login, password reset failure, user profile updates, or deletion requests.
    - **General_Inquiry:** Questions about general policies, product availability, or non-technical support.
    """
    
    schema_guide = json.dumps(TicketClassification.model_json_schema(), indent=2)

    system_prompt = (
        "You are an expert support ticket classifier. Analyze the user's support query. "
        "Use the provided Category Guide to strictly assign the correct Category and Priority. "
        "Your ENTIRE response MUST be a JSON object that strictly adheres to the provided schema. "
        "Do not include any other text, explanation, or markdown wrappers."
        f"\n\n{category_guide}" 
        f"\n\nSCHEMA:\n{schema_guide}"
    )
    
    try:
        response: ChatCompletion = client.chat.completions.create(
            model=CLASSIFICATION_MODEL, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Classify this ticket: '{ticket_text}'"}
            ],
            response_format={"type": "json_object"}, 
            temperature=0.0
        )
        
        json_content = response.choices[0].message.content.strip()
        classification_data = json.loads(json_content)
        TicketClassification.model_validate(classification_data)
        
        return classification_data

    except Exception:
        return {"category": "Classification_Failed", "priority": "Critical", "summary": "Automatic classification failed, requires human review."}


def draft_reply(ticket_text: str, classification: dict, user_info: dict) -> str:
    category = classification.get('category', 'N/A')
    priority = classification.get('priority', 'N/A')
    summary = classification.get('summary', 'The issue described.')
    
    user_name = user_info.get('name', 'Valued Customer')
    user_email = user_info.get('email', '[Email Not Provided]')
    
    system_prompt = (
        f"You are a professional and empathetic Level 2 Customer Support Agent. The customer's name is {user_name} (Email: {user_email}). "
        f"The ticket is classified as **{category}** with **{priority}** priority. "
        "Draft a helpful, polite, and detailed initial response. "
        f"The user's core issue is: '{summary}'."
        "Acknowledge the specific issue, apologize for the inconvenience, and "
        "explain the next clear step (e.g., 'I have escalated this,' or 'Please try X'). "
        "Maintain a helpful, human-like tone, and sign off professionally using only the company name."
        f"\n\n**COMPANY SIGNATURE:**\nBest regards,\n{COMPANY_NAME}"
    )
    
    user_prompt = f"Original Customer Subject: {user_info.get('subject')}\nOriginal Customer Issue Description: {ticket_text}"
    
    try:
        response: ChatCompletion = client.chat.completions.create(
            model=REPLY_DRAFTING_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    except Exception:
        return "Error: Could not draft reply. Please check API credentials and Groq status."