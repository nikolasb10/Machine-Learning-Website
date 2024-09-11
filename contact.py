import streamlit as st

def app():    
    # Title of the contact page
    st.title("Contact Us")
    
    # Introduction text
    st.write("""
        **We'd love to hear from you!** 

        If you have any questions, feedback, or just want to get in touch, please use the form below. We will get back to you as soon as possible.
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
                st.success("Thank you for your message! We'll get back to you soon.")
                # Here you would typically send the form data to a database or an email address
                # For demonstration, we'll just print it in the console
                print(f"Message from {contact_name} ({contact_email}): {message}")

