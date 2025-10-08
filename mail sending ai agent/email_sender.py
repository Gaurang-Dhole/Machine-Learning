import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Streamlit app title
st.title("Email Sender App")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel file with email addresses", type=["xlsx"])
emails = []
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    if "Email" in df.columns:
        emails = df["Email"].tolist()
        st.write("Emails loaded:", emails)
    else:
        st.error("Excel file must contain an 'Email' column.")

# Input email content
subject = st.text_input("Email Subject", "Test Email")
body = st.text_area("Email Body", "This is a test email sent from the Streamlit app.")

# Sender credentials
sender_email = "testivus01@gmail.com"
app_password = st.text_input("Enter Gmail App Password", type="password")

# Send email button
if st.button("Send Emails"):
    if not emails:
        st.error("No emails loaded. Please upload a valid Excel file.")
    elif not app_password:
        st.error("Please enter the Gmail App Password.")
    else:
        try:
            # Set up the SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)

            # Send email to each recipient
            for recipient in emails:
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = recipient
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                server.send_message(msg)
                st.write(f"Email sent to {recipient}")

            server.quit()
            st.success("All emails sent successfully!")
        except Exception as e:
            st.error(f"Failed to send emails: {str(e)}")
