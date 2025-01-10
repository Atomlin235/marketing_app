import requests
import re
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

def number_finder(URL:str):
    if URL:
        try:
            # Send GET request to the URL
            response = requests.get(URL, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get all text content from the webpage
            text_content = soup.get_text()

            # Regular expression pattern for phone numbers
            phone_pattern = r'''href=["']tel:\s*     # Match 'tel:' links (with href="tel:")
                    (?:\+?\d{1,3}[-.\s]?)?  # Optional country code, e.g., +1, +91
                    (?:\(?\d{3}\)?[-.\s]?)  # Optional area code, e.g., (123) or 123
                    \d{3}[-.\s]?            # First 3 digits, e.g., 456
                    \d{4}                   # Last 4 digits, e.g., 7890
                    (?:\s?(?:ext|x|extension)\s?\d{1,5})?  # Optional extension
                    ["']                    # Match the closing quote of href attribute
                 |
                 (?:\+?\d{1,3}[-.\s]?)?   # Optional country code for standalone numbers
                 (?:\(?\d{3}\)?[-.\s]?)   # Optional area code
                 \d{3}[-.\s]?             # First 3 digits
                 \d{4}                    # Last 4 digits
                 (?:\s?(?:ext|x|extension)\s?\d{1,5})?   # Optional extension
                '''

            # Find all matches in the text content
            all_matches = re.findall(phone_pattern, soup.prettify(), re.VERBOSE)

            # Separate matches into href tel numbers and standalone numbers
            href_tel_numbers = []
            standalone_tel_numbers = []

            # Iterate through matches and categorize
            for match in all_matches:
                if 'href="tel:' in match:  # Check if the match includes 'href="tel:'
                    href_tel_numbers.append(match.replace('href="tel:', '').strip('\'"'))  # Clean up 'tel:' prefix
                else:
                    standalone_tel_numbers.append(match.strip())

            # Remove duplicates
            unique_href_tel_numbers = list(set(href_tel_numbers))
           # unique_standalone_tel_numbers = list(set(standalone_tel_numbers))

         
           # print("Standalone Tel Numbers:", unique_standalone_tel_numbers
            # If phone numbers are found, return them as a comma-separated string
            if unique_href_tel_numbers:
                clickable_numbers = ', '.join(unique_href_tel_numbers)
                st.write("Clickable Phone Numbers Found:")
                st.write(clickable_numbers)
            else:
                st.write("No clickable phone numbers found on the webpage")

           # if unique_standalone_tel_numbers:
            #    non_clickable_numbers = ', '.join(unique_standalone_tel_numbers)
            #    st.write("Non Clickable Phone Numbers Found:")
            #    st.write(non_clickable_numbers)
           # else:
            #    st.write("No non-clickable phone numbers found on the webpage")

        except requests.RequestException as e:
            st.write(f"Error accessing the webpage: {str(e)}")
        except Exception as e:
            st.write(f"An error occurred: {str(e)}")
    
def cms_finder(URL):
    if URL:
        try:
            # Send GET request to URL
            response = requests.get(URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        
        
            # Check for common CMS indicators
        
            # WordPress indicators
            if soup.find('meta', {'name': 'generator', 'content': lambda x: x and 'WordPress' in x}):
                cms = "WordPress"
            elif soup.find('link', {'rel': 'https://api.w.org/'}):
                cms = "WordPress"
            elif 'wp-content' in response.text or 'wp-includes' in response.text:
                cms = "WordPress"
            
            # Joomla indicators
            elif soup.find('meta', {'name': 'generator', 'content': lambda x: x and 'Joomla' in x}):
                cms = "Joomla"
            elif 'option=com_content' in response.text:
                cms = "Joomla"
            
            # Drupal indicators
            elif 'Drupal.settings' in response.text:
                cms = "Drupal"
            elif soup.find('meta', {'name': 'Generator', 'content': lambda x: x and 'Drupal' in x}):
                cms = "Drupal"
            
            # Wix indicators
            elif 'wix.com' in response.text:
                cms = "Wix"
            
            # Shopify indicators
            elif 'cdn.shopify.com' in response.text:
                cms = "Shopify"
            
            # Magento indicators
            elif 'Mage.Cookies' in response.text:
                cms = "Magento"
            elif soup.find('script', {'type': 'text/x-magento-init'}):
                cms = "Magento"
            
            # Ghost indicators
            elif soup.find('meta', {'name': 'generator', 'content': lambda x: x and 'Ghost' in x}):
                cms = "Ghost"
            
            # Squarespace indicators
            elif 'squarespace.com' in response.text:
                cms = "Squarespace"
            else:
                cms = "unknown or custom"
            st.write(cms)
        except requests.RequestException as e:
            st.write(f"Error accessing the webpage: {str(e)}")
        except Exception as e:
            st.write(f"An error occurred: {str(e)}")
def cms_finder_scan(URL):
    if URL:
        try:
            # Send GET request to URL
            response = requests.get(URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        
        
            # Check for common CMS indicators
        
            # WordPress indicators
            if soup.find('meta', {'name': 'generator', 'content': lambda x: x and 'WordPress' in x}):
                cms = "WordPress"
            elif soup.find('link', {'rel': 'https://api.w.org/'}):
                cms = "WordPress"
            elif 'wp-content' in response.text or 'wp-includes' in response.text:
                cms = "WordPress"
            # GoDaddy Website Builder indicator
            elif soup.find('meta', {'name': 'generator', 'content': lambda x: x and 'go daddy website builder' in x.lower()}):
                cms = "GoDaddy"
            # Joomla indicators
            elif soup.find('meta', {'name': 'generator', 'content': lambda x: x and 'Joomla' in x}):
                cms = "Joomla"
            elif 'option=com_content' in response.text:
                cms = "Joomla"
            
            # Drupal indicators
            elif 'Drupal.settings' in response.text:
                cms = "Drupal"
            elif soup.find('meta', {'name': 'Generator', 'content': lambda x: x and 'Drupal' in x}):
                cms = "Drupal"
            
            # Wix indicators
            elif 'wix.com' in response.text:
                cms = "Wix"
            
            # Shopify indicators
            elif 'cdn.shopify.com' in response.text:
                cms = "Shopify"
            
            # Magento indicators
            elif 'Mage.Cookies' in response.text:
                cms = "Magento"
            elif soup.find('script', {'type': 'text/x-magento-init'}):
                cms = "Magento"
            
            # Ghost indicators
            elif soup.find('meta', {'name': 'generator', 'content': lambda x: x and 'Ghost' in x}):
                cms = "Ghost"
            
            # Squarespace indicators
            elif 'squarespace.com' in response.text:
                cms = "Squarespace"
            else:
                cms = "unknown or custom or go daddy"
            return cms
        except requests.RequestException as e:
            return f"Error"
        except Exception as e:
            return (f"Error")

def find_tags(URL):
    if URL:
        try:
            # Send GET request to URL
            response = requests.get(URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Initialize variables
            ga4_found = False
            gtm_found = False
            ga4_tags = []  # List to store all GA4 tags
            gtm_tags = []  # List to store all GTM tags

            # Search for GA4 and GTM in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                script_text = str(script)

                # Check for GA4
                if 'G-' in script_text:
                    ga4_found = True
                    # Extract all GA4 measurement IDs (G-XXXXXXXXXX)
                    ga4_matches = re.findall(r'G-[A-Z0-9]+', script_text)
                    ga4_tags.extend(ga4_matches)  # Add all found GA4 tags to the list
                elif 'gtag' in script_text or 'google-analytics' in script_text:
                    ga4_found = True
                    ga4_matches = re.findall(r'G-[A-Z0-9]+', script_text)
                    ga4_tags.extend(ga4_matches)  # Add all found GA4 tags to the list
                # Check for GTM
                if 'GTM-' in script_text:
                    gtm_found = True
                    # Extract all GTM IDs (GTM-XXXXXX)
                    gtm_matches = re.findall(r'GTM-[A-Z0-9]+', script_text)
                    gtm_tags.extend(gtm_matches)  # Add all found GTM tags to the list
                elif 'googletagmanager' in script_text:
                    gtm_found = True
                    # Try to extract GTM ID from URL pattern
                    gtm_matches = re.findall(r'GTM-[A-Z0-9]+', script_text)
                    gtm_tags.extend(gtm_matches)  # Add all found GTM tags to the list

            # Also check for GTM in noscript tags (GTM often has a noscript fallback)
            noscript_tags = soup.find_all('noscript')
            for noscript in noscript_tags:
                noscript_text = str(noscript)
                if 'googletagmanager' in noscript_text:
                    gtm_found = True
                    # Try to extract GTM IDs if not found earlier
                    gtm_matches = re.findall(r'GTM-[A-Z0-9]+', noscript_text)
                    gtm_tags.extend(gtm_matches)  # Add all found GTM tags to the list

            # Remove duplicates from the tags
            ga4_tags = list(set(ga4_tags))
            gtm_tags = list(set(gtm_tags))

            # Display results
            st.subheader('GA4 Tags:')
            if ga4_found and len(ga4_tags)>=1:
                
                for ga4_tag in ga4_tags:
                    st.write(ga4_tag)
            else:
                st.write('GA4 Not Found')

            st.subheader('GTM Tags:')
            if gtm_found and len(gtm_tags)>=1:
                
                for gtm_tag in gtm_tags:
                    st.write(gtm_tag)
            else:
                st.write('GTM Not Found')

        except requests.RequestException as e:
            st.write(f"Error accessing the webpage: {str(e)}")
        except Exception as e:
            st.write(f"An error occurred: {str(e)}")

def css_selector(url: str):
    if url:
        try:
            # Parse the HTML
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all form elements
            forms = soup.find_all('form')  # Get all forms in the document

            if forms:
                for index, form in enumerate(forms, start=1):
                    print(f"\nProcessing Form {index}:\n")
                    
                    # Build the CSS selector
                    path_parts = []
                    current = form
                    while current:
                        if current.get('id'):
                            # If an ID is found, it's unique enough; stop here
                            selector = f"#{current['id']}"
                            path_parts.append(selector)
                            break
                        elif current.get('class'):
                            # If no ID, use classes to identify the element
                            selector = current.name  # Tag name
                        else:
                            # Otherwise, use just the tag name
                            selector = current.name
                        path_parts.append(selector)
                        current = current.parent
                    
                   
                    
                    # Reverse the path to start from the root
                    css_selector = ' > '.join(reversed(path_parts))
                    st.write(f"Generated CSS Selector for Form {index}: {css_selector}")
            else:
                print("No form elements found in the HTML.")
        
        except requests.RequestException as e:
            st.write(f"Error accessing the webpage: {str(e)}")
        except Exception as e:
            st.write(f"An error occurred: {str(e)}")
def business_setting(business_name:str):
    if business_name:
        str = f"""
You are a receptionist working for a business called {business_name} and your name is Ella, a virtual secretary. You are British and always use British English, do not use American English. You enjoy helping others. You are not allowed to commit to things but you will note it down instead. Do Not make any Bookings or appointments, do not give advice. Do not schedule anything with the customers. Keep on topic and don't get distracted.

Keep responses to the point. If someone replies with "thanks" or a similar short response, end the conversation. Do not repeat yourself.
"""
        st.write(str)

def ai_prompt(url:str):
    web_address = url

    if web_address:
        prompt = f"I am creating an AI chatbot with the following company: {url}. Please can you give me a summary of the company and what they offer, which I can tell the chatbot to give it more information to work with"
        st.markdown(''':red[Insert Into Chat GPT And Copy The Response]''')
        st.write(prompt)

def add_cms_column(df, column_name, scan_function):
    """
    Adds a new column 'CMS' to the DataFrame by applying a scan function to each URL in the specified column.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column containing URLs.
        scan_function (function): The function to process each URL.

    Returns:
        pd.DataFrame: The DataFrame with the new 'CMS' column.
    """
    # Apply the scan function to each URL in the specified column
    #df['CMS'] = df[column_name].apply(lambda url: scan_function(url) if pd.notna(url) else None)
    # Apply the scan function to each URL in the specified column
    def process_row(url, index):
        print(f"Scanning index: {index}")
        return scan_function(url) if pd.notna(url) else None

    df['CMS'] = [process_row(row[column_name], idx) for idx, row in df.iterrows()]
    return df



