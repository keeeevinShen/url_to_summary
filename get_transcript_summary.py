from playwright.sync_api import sync_playwright
import os
import re
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate 
from langchain_ollama import ChatOllama


"""load_dotenv()
unique_name = os.environ.get("UNIQUE_NAME")
password = os.environ.get("PASSWORD")"""

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
        # try: 
        #     page.wait_for_selector('input[id="username"]', timeout=3000)
        #     input_box1 = page.locator('input[id="username"]')
        #     input_box1.type("replace this with your unique name")
        #     input_box2 = page.locator('input[id="password"]')
        #     input_box2.type("replace this with your password")
        #     page.keyboard.press("Enter")
        # except:
        #     print("no need to login, process now")

        
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
        # try: 
        #     page.wait_for_selector('input[id="username"]', timeout=3000)
        #     input_box1 = page.locator('input[id="username"]')
        #     input_box1.type("replace this with your unique name")
        #     input_box2 = page.locator('input[id="password"]')
        #     input_box2.type("replace this with your passowrd")
        #     page.keyboard.press("Enter")
        # except:
        #     print("no need to login, process now")



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

def ask_llama(transcript, user_input= "give me the summary of this info"):
    print("Hello, langchain!")
    information = transcript

    #user_input = input("your prompt (press enter to use default prompt): ")
    #use user_input otherwise just get the summary
    #if user_input is None:
    summary_template = f"for this {information}: {user_input }"
    # else:
    #     summary_template = """
    #     given the information {information}  I want you to give me the summary of the information"""

    input_template  = PromptTemplate(input_variables=["information"], template = summary_template)

 
    llm_ollama = ChatOllama(model="llama3.1",temperature=0)
  
    chain = input_template | llm_ollama 
    res = chain.invoke(input={"information":information})
    return res.content


    
