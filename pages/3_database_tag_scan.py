import streamlit as st
import pandas as pd
import numpy as np
import base_functions as bf

import time


def main():
    st.subheader("Data/Web Scanner")
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
        st.subheader("Current Max Scannable 800")

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
