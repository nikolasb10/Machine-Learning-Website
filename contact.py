import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def send_email(contact_email, contact_name, message):
    # Email settings
    sender_email = os.getenv('SENDER_EMAIL')  # Your email address
    sender_password = os.getenv('SENDER_PASSWORD')  # Your email password (use App Password if using Gmail 2FA)
    receiver_email = os.getenv('RECEIVER_EMAIL')  # The email address where you want to receive the messages
    print(sender_email,sender_password,receiver_email)
    # Create email
    subject = f"New message from {contact_name}"
    body = f"Name: {contact_name}\nEmail: {contact_email}\n\nMessage:\n{message}"
    
    # Set up the email details
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    print(msg)
    # Connect to Gmail's SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)  # Login to the email account
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)  # Send the email
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
        return False

def app():    
    # Title of the contact page
    st.title("Contact Me")
    
    # Introduction text
    st.write("""
        **I'd love to hear from you!** 

        If you have any questions, feedback, or just want to get in touch, please use the form below. I'll get back to you as soon as possible.
    """)
    
    # Contact Form
    with st.form(key='contact_form'):
        # Form fields
        contact_email = st.text_input("Your Email", placeholder="example@domain.com")
        contact_name = st.text_input("Your Name", placeholder="John Doe")
        message = st.text_area("Your Message", placeholder="Type your message here...")

        # Submit button
        submit_button = st.form_submit_button(label='Send Message')
        
        if submit_button:
            # Basic validation
            if not contact_email or not contact_name or not message:
                st.error("Please fill out all fields before submitting.")
            else:
                # Send email
                email_sent = send_email(contact_email, contact_name, message)
                
                if email_sent:
                    st.success("Thank you for your message! We'll get back to you soon.")
                else:
                    st.error("There was an issue sending your message. Please try again later.")
