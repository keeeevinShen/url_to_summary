#this works for no login required websties like eecs398

from playwright.sync_api import sync_playwright

def get_video_url(lecture_url):
    """Use Playwright to get the video URL from Canvas."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False to see the browser actions
        page = browser.new_page()
        
        print(f"🔍 Navigating to: {lecture_url}")
        page.goto(lecture_url)

        # Wait for the video element to load
        page.wait_for_selector("video")

        # Get the src attribute from the video element
        video_url = page.locator("video").get_attribute("src")

        browser.close()

        # Print and return the video URL
        if video_url:
            print(f"🎯 Video URL found: {video_url}")
            return video_url
        else:
            print("⚠️ Video URL not found.")
            return None


# Replace with an actual Canvas lecture URL
lecture_url = input("give me your lecture url")
video_url = get_video_url(lecture_url)

if video_url:
    print("\n✅ Successfully extracted video URL:")
    video_url = "https:" + video_url
    print(video_url)
else:
    print("\n❌ Failed to extract video URL. Check the selector or the page structure.")
