# Support Ticket Classifier & Auto-Responder

This project is a Streamlit web application that demonstrates an AI-powered system for automatically classifying and responding to customer support tickets. It uses the Groq API for fast inference to categorize tickets and generate draft replies, which can then be reviewed by a support agent on a centralized dashboard.

## Features

-   **Ticket Submission Form:** A simple and intuitive interface for users to submit new support tickets.
-   **AI-Powered Classification:** Uses a large language model (via Groq) to automatically classify tickets into predefined categories (e.g., Billing, Technical Bug, Feature Request) and assign a priority level (Low, Medium, High, Critical).
-   **Automated Reply Drafting:** Generates a professional and empathetic draft response tailored to the user's issue.
-   **Review Dashboard:** A central dashboard where support agents can view all submitted tickets, their classifications, and the AI-drafted replies.

## How It Works

1.  **Raise a Ticket:** A user fills out a form with their name, email, subject, and a description of their issue.
2.  **Classify & Draft:** When the ticket is submitted, the application sends the ticket text to the Groq API.
    -   First, a classification model analyzes the text to determine the ticket's category and priority.
    -   Second, a reply-drafting model uses the original ticket information and the classification to generate a suitable response.
3.  **Display on Dashboard:** The new ticket, along with its classification and the drafted reply, is added to a session-wide dashboard for review.

## Getting Started

### Prerequisites

-   Python 3.7+
-   A Groq API Key. You can get one for free at [https://console.groq.com/](https://console.groq.com/).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Support-Ticket-Classifier.git
    cd Support-Ticket-Classifier
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    -   Create a new file named `.env` in the root of the project directory.
    -   Add your Groq API key to the `.env` file as follows:
        ```
        GROQ_API_KEY="your-groq-api-key"
        ```

### Running the Application

Once the installation is complete, you can run the Streamlit application with the following command:

```bash
streamlit run Dashboard.py
```

The application will open in your default web browser.

## Usage

1.  Navigate to the **Raise Ticket** page from the sidebar.
2.  Fill in the required fields (Name, Email, Subject, Description) and click "Submit Ticket".
3.  Navigate back to the main **Dashboard** page.
4.  You will see your newly created ticket in the "All Tickets Raised" table.
5.  Use the dropdown menu under "Review Details" to select a ticket and view its drafted response.