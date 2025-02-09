# for scraping website
import requests
from bs4 import BeautifulSoup
import time

def scrape_physiopenang(url):
    """
    Scrapes textual data from all pages of physiopenang.com.
    """

    all_text = []

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from all relevant HTML elements
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a', 'li', 'div']): # Added 'div' and 'li'
            text = element.get_text(strip=True)
            if text:  # Avoid empty strings
                all_text.append(text)


        # Find and follow links to other pages on the same domain
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/') or href.startswith(url):  # Relative or absolute link on same domain
                absolute_url = href
                if href.startswith('/'):
                    absolute_url = url + href  # Construct absolute URL

                if absolute_url not in visited_urls and url in absolute_url:  #Avoid external link
                    print(f"Following link: {absolute_url}")
                    visited_urls.add(absolute_url)  # Add to visited URLs
                    time.sleep(1)  # Respectful delay
                    all_text.extend(scrape_physiopenang(absolute_url)) #Recursive call

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {url} - {e}")
    except Exception as e:
        print(f"Error processing URL: {url} - {e}")

    return all_text

# --- Main Execution ---
base_url = "https://lophysio.com/"
visited_urls = {base_url}  # Keep track of visited URLs to avoid loops

all_scraped_text = scrape_physiopenang(base_url)

# Print or save the scraped text
for text in all_scraped_text:
    print(text)

# Optionally, save to a file:
with open("physiopenang_data.txt", "w", encoding="utf-8") as f:
    for text in all_scraped_text:
        f.write(text + "\n")

print("Scraping complete.  Data saved to physiopenang_data.txt")