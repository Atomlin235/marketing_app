import streamlit as st
import base_functions as bf



def main():
  

    st.header("Say Hello Helper")
    business_name = st.text_input("Enter Business Name")
    
    URL = st.text_input("Enter Landing Page Or Contact Page URL")
    st.subheader("Phone Numbers")
    bf.number_finder(URL)
    st.subheader("CMS")
    bf.cms_finder(URL)
    st.subheader("Google Analytics & Tag Manager")
    bf.find_tags(URL)
    st.subheader("Form CSS")
    bf.css_selector(URL)
    st.subheader("Business Settings Set Up")
    bf.business_setting(business_name)
    st.subheader("Ai Assitant Personality Prompt Generator")
    bf.ai_prompt(URL)
    

if __name__ == "__main__":
    main()