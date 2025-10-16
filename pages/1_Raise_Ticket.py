import streamlit as st
import pandas as pd
import re
import time
from ticket_agent import classify_ticket, draft_reply


EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

st.set_page_config(layout="wide")
st.title("🎫 Raise a New Support Ticket")

if 'tickets_df' not in st.session_state:
    st.session_state.tickets_df = pd.DataFrame(columns=['Name', 'Email', 'Subject', 'Description', 'Category', 'Priority', 'Drafted Reply'])

with st.form("ticket_form"):
    st.subheader("Customer Details")
    c1, c2 = st.columns(2)
    name = c1.text_input("Name (Required)", key="name_input")
    email = c2.text_input("Email (Required)", key="email_input")
    
    st.subheader("Issue Details")
    subject = st.text_input("Subject (Required)", key="subject_input")
    description = st.text_area("Detailed Issue Description (Required)", height=200, key="desc_input")
    
    submitted = st.form_submit_button("Classify & Draft Reply")

if submitted:
    if not name or not email or not subject or not description:
        st.error("Please fill in all required fields.")
    elif not re.match(EMAIL_REGEX, email.strip()):
        st.error("Invalid email format. Please include '@' and a domain (e.g., example@domain.com).")
    else:
        full_ticket_text = f"Subject: {subject.strip()}\nBody: {description.strip()}"
        user_info = {
            "name": name.strip(),
            "email": email.strip(),
            "subject": subject.strip()
        }
        
        with st.spinner("Classifying ticket and drafting reply with Groq..."):
            
            classification_result = classify_ticket(full_ticket_text)
            
            drafted_reply = draft_reply(full_ticket_text, classification_result, user_info)
            
        new_ticket = {
            'Name': user_info['name'],
            'Email': user_info['email'],
            'Subject': user_info['subject'],
            'Description': description.strip(),
            'Category': classification_result['category'],
            'Priority': classification_result['priority'],
            'Drafted Reply': drafted_reply,
            'Timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        st.session_state.tickets_df = pd.concat(
            [st.session_state.tickets_df, pd.Series(new_ticket).to_frame().T], 
            ignore_index=True
        )

        st.success("Ticket Classified, Drafted, and Stored Successfully! See the 'Ticket List' page.")
        
        st.subheader("LLM Analysis Summary")
        st.markdown(f"**Category:** `{classification_result['category']}` | **Priority:** `{classification_result['priority']}`")
        st.markdown(f"**Summary:** {classification_result['summary']}")
        
        st.subheader("Drafted Response")
        st.code(drafted_reply, language="text")