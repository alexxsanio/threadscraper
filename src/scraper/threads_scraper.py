import json
from typing import Dict

import jmespath
from parsel import Selector
from playwright.sync_api import sync_playwright
from nested_lookup import nested_lookup
from .parser import ThreadsParser

# Note: we'll also be using parse_thread function we wrote earlier:
# from parser import parse_thread, parse_profile


class ThreadsScraper:
    def __init__(self, settings: Dict, config_dir: str, data_dir: str):
        self.settings = settings
        self.config_dir = config_dir
        self.data_dir = data_dir
        self.parser = ThreadsParser()

    def fetch_user_threads(self, username: str) -> dict:
        """Scrape Threads profile and their recent posts from a given URL"""
        url = f"{self.settings.get('base_url')}@{username}"
        with sync_playwright() as pw:
            # start Playwright browser
            browser = pw.chromium.launch()
            context = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = context.new_page()

            page.goto(url)
            # wait for page to finish loading
            # Get viewport dimensions
            viewport = page.viewport_size

            # Click near the bottom-right corner
            x = viewport["width"] - 20
            y = viewport["height"] - 20

            page.mouse.click(x, y)
            # page.wait_for_selector("[data-pressable-container=true]")
            selector = Selector(page.content())
        parsed = []
        # find all hidden datasets
        hidden_datasets = selector.css('script[type="application/json"][data-sjs]::text').getall()
        for hidden_dataset in hidden_datasets:
            # skip loading datasets that clearly don't contain threads data
            if '"ScheduledServerJS"' not in hidden_dataset:
                continue
            is_profile = 'follower_count' in hidden_dataset
            is_threads = 'thread_items' in hidden_dataset
            if not is_profile and not is_threads:
                continue
            data = json.loads(hidden_dataset)
            if is_profile:
                user_data = nested_lookup('user', data)
                user = self.parser.parse_profile(user_data[0])
            if is_threads:
                thread_items = nested_lookup('thread_items', data)
                threads = [
                    self.parser.parse_thread(t) for thread in thread_items for t in thread
                ]
                parsed = [user | thread for thread in threads]
        print(f"Scraped {len(parsed)} threads for @{username}")
        return parsed
    
    def fetch_users_threads(self) -> dict:
        usernames = self.settings.get('usernames')
        all_threads = []
        for username in usernames:
            threads = self.fetch_user_threads(username=username)
            all_threads.extend(threads)
        return all_threads
