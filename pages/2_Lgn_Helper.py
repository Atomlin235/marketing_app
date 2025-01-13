import streamlit as st
import base_functions as bf
import json

def instructions():
        st.markdown("""
            INSTRUCTIONS

                    Download Container File

                    Download the container JSON file (right-click on the link and click “Save Link As” or “Save Target As” to save the JSON file to your computer).

                    Import JSON File into GTM

                    Log into the clients Google Tag Manager account and head to the Admin section. Under Container options, select Import Container. Read this blog post for more details about importing a container file.
                    (https://www.analyticsmania.com/how-to-import-google-tag-manager-container/)
                    Insert your own GA4 measurement ID

                    In the GA4 event tag, you will find a field called “Measurement ID”. In this field, enter your GA4 property’s measurement ID.


                    Preview & Publish

                    Use the Preview options to test this container on your own site. Try testing each of the events to make sure they’re working properly. If everything looks good, go ahead and publish!

        """
        )    

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
    bf.iframe_finder(URL)
    st.subheader("Container Download")

    container = st.radio(
    "Select A GTM Container",
    ["***Basic GTM***","***Calendy***",  "***TBC***"],
    index=None,horizontal=True

    )
    
    if container =="***Basic GTM***":
        with open("basic_gtm_setup.json", "r") as file:
            data = json.load(file)
            json_string = json.dumps(data, indent=4)

        # Create the download button
        st.download_button(
            label="Download Basic GTM",
            data=json_string,
            file_name="basic_gtm.json",
            mime="application/json"
        )

        instructions()






    if container =="***Calendy***":
        with open("calendly.json", "r") as file:
            data = json.load(file)

# Convert the data to a JSON string with proper formatting
        json_string = json.dumps(data, indent=4)

        # Create the download button
        st.download_button(
            label="Download Calendly JSON",
            data=json_string,
            file_name="calendly_export.json",
            mime="application/json"
        )
        instructions()


    

if __name__ == "__main__":
    main()
