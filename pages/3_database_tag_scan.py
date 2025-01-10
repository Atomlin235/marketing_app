import streamlit as st
import pandas as pd
import numpy as np
import base_functions as bf

import time


def main():
    st.subheader("Data/Web Scanner")
    st.subheader("Current Max Scannable 800 0.7s ->1.2s per row")
    st.write("This application will scan through any data in CSV format and will scrape a column called Website Url and append a new column to the table with the CMS of each web address.")
    uploaded_file = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=False
    )
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        updated_df = bf.add_cms_column(df, 'Website Url', bf.cms_finder_scan)
        st.dataframe(updated_df)

        cms_counts = updated_df['CMS'].value_counts()
        st.bar_chart(cms_counts,use_container_width=True)
    

# Plot the bar chart
    st.markdown('''
List of CMS:
WordPress
GoDaddy
Joomla
Drupal
Wix
Shopify
Magento
Ghost
Squarespace
unknown or custom or go daddy  
                ''')
        

    
if __name__ == "__main__":
    main()
