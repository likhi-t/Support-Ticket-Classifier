import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 Support Ticket Dashboard")
st.markdown("This dashboard displays all tickets raised during this session.")

if 'tickets_df' not in st.session_state:
    st.session_state.tickets_df = pd.DataFrame(columns=['Name', 'Email', 'Subject', 'Description', 'Category', 'Priority', 'Drafted Reply'])

if st.session_state.tickets_df.empty:
    st.info("No tickets have been raised yet. Navigate to 'Raise Ticket' to submit one.")
else:
    display_cols = ['Timestamp', 'Name', 'Email', 'Subject', 'Category', 'Priority']
    
    st.subheader("All Tickets Raised")
    st.dataframe(
        st.session_state.tickets_df[display_cols],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Review Details")
    
    selection = st.selectbox(
        "Select a Ticket Subject to View the Drafted Reply:",
        st.session_state.tickets_df['Subject'].tolist()
    )
    
    if selection:
        selected_row = st.session_state.tickets_df[st.session_state.tickets_df['Subject'] == selection].iloc[0]
        
        st.markdown("---")
        st.markdown(f"**Selected Ticket:** `{selected_row['Subject']}`")
        st.markdown(f"**Classified Priority:** `{selected_row['Priority']}`")
        st.markdown("### Drafted Response (Ready to Send)")
        st.code(selected_row['Drafted Reply'], language='text')