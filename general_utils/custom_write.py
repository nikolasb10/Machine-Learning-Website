import streamlit as st

def custom_write(text,size = 20):
    st.markdown(
                    f"""
                    <h1 style='font-size:{size}px;'>
                        {text}
                    </h1>
                    """,
                    unsafe_allow_html=True
                )