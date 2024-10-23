import streamlit as st

from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

load_dotenv()

import home, movie_recommender, detection, contact, gaze_tracking, image_classification

st.set_page_config(
        page_title="ML Website",
        layout="wide"
)


st.markdown(
    """
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src=f"https://www.googletagmanager.com/gtag/js?id={os.getenv('analytics_tag')}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', os.getenv('analytics_tag'));
        </script>
    """, unsafe_allow_html=True)
print(os.getenv('analytics_tag'))


class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Machine Learning ',
                options=['Home', 'Gaze Tracking','Movie Recommender', 'Detection', 'Image Classification','Contact'],
                icons=['house-fill', 'eye', 'film','person-circle', 'camera2','telephone'],
                menu_icon='robot',
                default_index=0,
                styles={
                        "container": {"padding": "5!important","background-color":'black'},
                        "icon"     : {"color": "white", "font-size": "17px"}, 
                        "nav-link" : {"color":"white","font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#034DAB"},
                        "nav-link-selected": {"background-color": "#379BF9"},
                        "menu-title": {"font-size": "20px", "color": "white"} }
                
                )

        
        if app == "Home":
            home.app()
        if app == "Image Classification":
            image_classification.app()
        if app == "Gaze Tracking":
            gaze_tracking.app()
        if app == "Detection":
            detection.app()    
        if app == "Contact":
            contact.app()  
        if app == "Movie Recommender":
            movie_recommender.app()                  
          
             
    run()            
         