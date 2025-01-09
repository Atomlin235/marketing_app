import streamlit as st
import pandas as pd
import numpy as np
import base_functions as bf
import matplotlib.pyplot as plt
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

# Plot the bar chart
        plt.figure(figsize=(10, 6))
        cms_counts.plot(kind='bar')

        # Customize the plot
        plt.title("Count of Each CMS In Base", fontsize=16)
        plt.xlabel("CMS", fontsize=14)
        plt.ylabel("Count", fontsize=14)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Show the plot
        plt.tight_layout()
        plt.show()


    
if __name__ == "__main__":
    main()
