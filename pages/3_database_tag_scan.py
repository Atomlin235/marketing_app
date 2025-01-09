import streamlit as st
import pandas as pd
import numpy as np
import base_functions as bf

import time


def main():
    uploaded_file = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=False
    )
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        num_rows = df.shape[0]
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(num_rows):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1.5)
            my_bar.empty()
        st.dataframe(df)
        updated_df = bf.add_cms_column(df, 'Website Url', bf.cms_finder_scan)
        st.dataframe(updated_df)

        cms_counts = updated_df['CMS'].value_counts()
        st.dataframe(cms_counts)

# Plot the bar chart
        

    
if __name__ == "__main__":
    main()
