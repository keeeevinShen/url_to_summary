from playwright.sync_api import sync_playwright
import requests
import os
import re
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate 
from langchain_ollama import ChatOllama


load_dotenv()
unique_name = os.environ.get("UNIQUE_NAME")
password = os.environ.get("PASSWORD")

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
        try:
            page.wait_for_selector('input[id="username"]', timeout=4000)    #if it needs login 
            input_box1 = page.locator('input[id="username"]')
            input_box1.type("unique_name")
            input_box2 = page.locator('input[id="password"]')
            input_box2.type("password")
            page.keyboard.press("Enter")
        except:
            print("no login require, keep going")

        
        # Locate the <track> element with kind="captions"
        try:
            track_element = page.locator('track[kind="captions"]').first
            transcript_url = track_element.get_attribute('src')
            browser.close()

            if transcript_url:
                # Convert relative URL to absolute
        
                transcript_url = f"https://leccap.engin.umich.edu{transcript_url}"

                print(f" Transcript URL found: {transcript_url}")
                return transcript_url

            else:
                print(" Transcript URL not found.")

        except Exception as e:
            print(f" Failed to find the transcript URL: {e}")
            browser.close()






#repeat what we do on last step to get the content of the transcript

def open_trans_url(url):
    with sync_playwright() as p:
        # Open Chrome with Playwright
        browser = p.chromium.launch(headless=False, executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        page = browser.new_page()
        
        # Navigate to the Canvas lecture page
        print(f"🔍 Visiting: {url}")
        page.goto(url)
        page.wait_for_load_state("networkidle")
        try:
            page.wait_for_selector('input[id="username"]', timeout=4000)
            input_box1 = page.locator('input[id="username"]')
            input_box1.type("unique_name")
            input_box2 = page.locator('input[id="password"]')
            input_box2.type("password")
        except:
            print("no login require, keep going")


        page.keyboard.press("Enter")

        try:
            track_element = page.locator('pre[style="word-wrap: break-word; white-space: pre-wrap;"]').first
            transcript = track_element.inner_text()
            browser.close()

            if transcript:
                # Convert relative URL to absolut

                print(f"🎯 Transcript text found")
                """with open("full_transcript.tex", "w", encoding="utf-8") as f:
                    f.write(transcript)"""
                return transcript
                

            else:
                print(" Transcript URL not found.")

        except Exception as e:
            print(f" Failed to find the transcript URL: {e}")
            browser.close()


#after getting the cleaned data, we can save it to a file
with open("cleaned_transcript.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_transcript)


if __name__ == '__main__':


    lecture_url = input("🔗 Enter the Canvas lecture URL: ").strip()
    trans_url = get_transcript_url(lecture_url) #get the transcript url
    transcript_raw = open_trans_url(trans_url) #get the raw data

#then clean the data using: content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', '', content)
    cleaned_transcript = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', '', transcript_raw)

#after getting the cleaned data, we can save it to a file
    with open("cleaned_transcript.txt", "w", encoding="utf-8") as f:
        f.write(cleaned_transcript)
        
    print("Hello, langchain!")
    information = cleaned_transcript

    user_input = input("your prompt (press enter to use default prompt): ")
    #use user_input otherwise just get the summary

    if user_input:
        summary_template = f"for this {information}: {user_input }"
    else:
        summary_template = """
        given the information {information}  I want you to give me the summary of the information"""

    input_template  = PromptTemplate(input_variables=["information"], template = summary_template)

 
    llm_ollama = ChatOllama(model="llama3.1",temperature=0)
  
    chain = input_template | llm_ollama 
    res = chain.invoke(input={"information":information})
    print(res)
    
