from playwright.sync_api import sync_playwright
import requests
from datetime import datetime

def get_transcript_url(url):
    """
    Open the Canvas lecture URL, find the transcript URL, download, clean, and save it.
    """
    with sync_playwright() as p:
        # Open Chrome with Playwright
        browser = p.chromium.launch(headless=False, executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        page = browser.new_page()
        
        # Navigate to the Canvas lecture page
        print(f"🔍 Visiting: {url}")
        page.goto(url)
        page.wait_for_load_state("networkidle")

        # Save the fully-rendered HTML for debugging
        html_content = page.content()
        with open("full_rendered.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print("✅ Full rendered HTML saved to full_rendered.html")

        # Locate the <track> element with kind="captions"
        try:
            track_element = page.locator('track[kind="captions"]').first
            transcript_url = track_element.get_attribute('src')
            browser.close()

            if transcript_url:
                # Convert relative URL to absolute
        
                transcript_url = f"https://leccap.engin.umich.edu{transcript_url}"

                print(f"🎯 Transcript URL found: {transcript_url}")
                return transcript_url

            else:
                print("❌ Transcript URL not found.")

        except Exception as e:
            print(f"❌ Failed to find the transcript URL: {e}")
            browser.close()



# Run the function
lecture_url = input("🔗 Enter the Canvas lecture URL: ").strip()
get_transcript_url(lecture_url)