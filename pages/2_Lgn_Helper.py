import streamlit as st
import base_functions as bf

def main():
    

    st.header("LGN Helper")
    URL = st.text_input("Enter Landing Page Or Contact Page URL")
    st.subheader("Phone Numbers")
    bf.number_finder(URL)
    st.subheader("CMS")
    bf.cms_finder(URL)
    st.subheader("Google Analytics & Tag Manager")
    bf.find_tags(URL)
    st.subheader("iFrames/Third Parties")
    bf.iframe_finder_with_selenium(URL)

if __name__ == "__main__":
    main()
