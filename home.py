import streamlit as st
import requests
import re
from bs4 import BeautifulSoup

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

            # Regular expression pattern for phone numbers including 'tel:'
            phone_pattern = r'''(?:
                tel:\s*                # Match 'tel:' prefix optionally followed by spaces
                (?:\+?\d{1,3}[-.\s]?)? # Optional country code, e.g., +1, +91
                (?:\(?\d{3}\)?[-.\s]?) # Optional area code, e.g., (123) or 123
                \d{3}[-.\s]?           # First 3 digits, e.g., 456
                \d{4}                  # Last 4 digits, e.g., 7890
                (?:\s?(?:ext|x|extension)\s?\d{1,5})?  # Optional extension, e.g., ext123 or x12345
                |
                (?:\+?\d{1,3}[-.\s]?)? # Optional country code for standalone numbers
                (?:\(?\d{3}\)?[-.\s]?) # Optional area code
                \d{3}[-.\s]?           # First 3 digits
                \d{4}                  # Last 4 digits
                (?:\s?(?:ext|x|extension)\s?\d{1,5})?  # Optional extension
            )'''

            # Find all phone numbers in the text
            phone_numbers = re.findall(phone_pattern, text_content, re.VERBOSE)

            # Clean up phone numbers by removing extra whitespace
            phone_numbers = [number.strip() for number in phone_numbers]

            # Using a set to only keep unique numbers
            unique_numbers = list(set(phone_numbers))

            # If phone numbers are found, return them as a comma-separated string
            if unique_numbers:
                Output1 = ', '.join(unique_numbers)
                st.write("Phone Numbers Found:")
                st.write(Output1)
            else:
                st.write("No phone numbers found on the webpage")

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
        


def main():
    home = st.Page("home.py", title="Home", icon=":material/add_circle:")
    about = st.Page("about.py", title="about", icon=":material/delete:")

    pg = st.navigation([home, about])

    URL = st.text_input("input url")
    st.subheader("Phone Numbers")
    number_finder(URL)
    st.subheader("CMS")
    cms_finder(URL)
    find_tags(URL)






if __name__ == "__main__":
    main()