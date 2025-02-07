import re
import requests
from bs4 import BeautifulSoup
import streamlit as st

class WebScraper:
    def __init__(self, driver_path=None):
        self.driver_path = driver_path

    def get_url_text(self):
        """
        Uses requests to fetch the HTML from the travel destination URL.
        """
        url = 'https://www.travelandleisure.com/wba-2024-cities-world-8660857'
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error fetching page: HTTP {response.status_code}")
        return response.text

    def extract_ranked_cities(self):
        """
        Uses the cached function to extract ranked cities.
        """
        return get_cached_ranked_cities(self.driver_path)

    @staticmethod
    def return_cached_cities(driver_path=None):
        """
        Returns cached ranked cities using the optional driver_path.
        """
        return get_cached_ranked_cities(driver_path)

@st.cache_data(show_spinner=False)
def get_cached_ranked_cities(driver_path=None):
    """
    Instantiates a WebScraper (using the optional driver_path), fetches the HTML,
    parses it with BeautifulSoup, extracts text, applies regex to capture ranked cities,
    and returns the list.
    """
    scraper = WebScraper(driver_path)
    html = scraper.get_url_text()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator="\n")
    pattern = r"(?m)^(\d+)\.\s+(.*?),\s+(.*)$"
    matches = re.findall(pattern, text)
    results = [f"{rank} - {city}, {country}" for (rank, city, country) in matches]
    return results
