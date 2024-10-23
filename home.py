import streamlit as st
import requests
from streamlit_lottie import st_lottie
from general_utils.custom_write import custom_write

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    
    return r.json()

def app():
    st.title("Machine Learning Website")
    custom_write("Welcome to Nikolaos Benetos' Machine Learning Hub!",25)
    st.write("---")

    lottie_animation = load_lottie_url("https://lottie.host/b6f3a7a3-b91e-49d0-9368-931082f489ff/vCgGLoQyzt.json")
    # lottie_person    = load_lottie_url("https://lottie.host/b57aad79-f4ba-4821-a3f7-f10afe2c34f5/0Fc7YqAZAd.json")
    lottie_person    = load_lottie_url("https://lottie.host/48892f05-d1ce-4675-b72c-30808993a341/RIdZOg5x25.json")

    with open("./Benetos_CV.pdf", 'rb') as file:
        resume = file.read()

    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st_lottie(lottie_person,height=250)
        with right_column:
            st.write("""
                        A few words about myself: 

                        - **Education** : Electrical and Computer Engineering, NTUA (GPA: 8.3)
                        - **Focus**: Machine Learning, Computer Vision, Robotics, Software Development, Computer Architecture
                        - **Hard Skills**: Python, Java, C, C++, HTML/CSS, Node + React JavaScript, SQL, Streamlit, Flutter                        
                        """)
            st.download_button(label="📄 Download Resume", data=resume, file_name="Benetos_Resume.pdf",mime="application/octet-stream")
 
    st.write("---")
            
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown("""
                            At  Nikolaos Benetos' Hub, you'll find:
                            - **Interactive Demos**: Test out machine learning models and witness their capabilities firsthand.
                            - **Insights**: Learn about the underlying technologies and methodologies that power these models.
                            - **Real-World Applications**: See how machine learning is applied in various domains and industries.

                            Feel free to navigate through the site, try out different models, and don’t hesitate to reach out with any questions or feedback. Enjoy exploring the future of AI!
                        """)
        with right_column:
            st_lottie(lottie_animation, height=300)

#        Dive into a world of innovation and explore a variety of interactive machine learning models designed to showcase the power and potential of modern AI technology. Whether you're interested in predictive analytics, natural language processing, or computer vision, our demos provide a hands-on experience to see these models in action.

