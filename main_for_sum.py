import tkinter as tk
from tkinter import END
import threading
from get_video_url import get_video_url
from get_transcript_summary import get_transcript_url, open_trans_url, ask_llama
import re

#for the summary
def run_get_summary():
    """Retrieve the transcript URL and display it."""
    lecture_url = textbox.get("1.0", END).strip()
    user_prompt = textbox3.get("1.0", END).strip()
    if user_prompt == '':
        user_prompt = "give me the summary"

    if not lecture_url:
        update_output("⚠️ Please enter a valid URL.")
        return

    update_output(" Fetching transcript URL, please wait...")
    transcript_url = get_transcript_url(lecture_url)

    # Run Playwright synchronously in the main thread
    try:
        transcript = open_trans_url(transcript_url)
        if transcript_url:
            update_output(f" Transcript URL:\n{transcript_url}")
        else:
            update_output(" Transcript URL not found.")
    except Exception as e:
        update_output(f" Error occurred: {e}")

    try:
        summary = ask_llama(transcript, user_prompt)
        if summary:
            update_output(f"llama: {summary}")
        else:
            update_output("summary: failed to ask llama")
    except Exception as e:
        update_output(f" Error occurred: {e}")


#for lec_url to transcript:
def run_get_transcript():
    lecture_url = textbox.get("1.0", END).strip()
    if not lecture_url:
        update_output("⚠️ Please enter a valid URL.")
        return
    
    update_output(" Fetching transcript URL, please wait...")
    transcript_url = get_transcript_url(lecture_url)

    try:
        transcript = open_trans_url(transcript_url)
        if transcript:
            cleaned_transcript = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', '', transcript)
            cleaned_transcript_space = ', '.join(line.strip() for line in cleaned_transcript.splitlines() if line.strip())
            update_output(f" Transcript URL:\n{cleaned_transcript_space}")
        else:
            update_output(" Transcript URL not found.")
    except Exception as e:
        update_output(f" Error occurred: {e}")






#for the video url:
def run_get_video_url():
    """Retrieve the video URL and display it."""
    lecture_url = textbox.get("1.0", END).strip()  # Get URL from textbox
    if not lecture_url:
        update_output("⚠️ Please enter a valid URL.")
        return

    update_output("🔍 Fetching video URL, please wait...")

    # Run the Playwright function in a separate thread to avoid freezing the UI
    thread = threading.Thread(target=fetch_and_display_video_url, args=(lecture_url,))
    thread.start()

def fetch_and_display_video_url(lecture_url):
    """Fetch the video URL and update the output textbox."""
    video_url = get_video_url(lecture_url)
    if video_url:
        update_output(f"🎯 Video URL:\n{video_url}")
    else:
        update_output("⚠️ Video URL not found.")

#for mystery word
def run_get_mystery_word():
    update_output("Kevin Durant is the best basketball player in the world.")



def update_output(message):
    """Update the output textbox with the provided message."""
    textbox2.config(state=tk.NORMAL)
    textbox2.delete("1.0", tk.END)
    textbox2.insert(tk.END, message)
    textbox2.config(state=tk.DISABLED)

root = tk.Tk()
root.geometry("1000x1000")
root.title("easy lecture(For U-M)")
label = tk.Label(root,text="input your lecture url below:", font = ('Arial',18))
label.pack(padx=10,pady=10) #set padding like html

textbox = tk.Text(root,height=1,font = ('Arial',18))
textbox.pack(padx=10,pady=10)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0,weight = 1)
buttonframe.columnconfigure(1,weight = 1)

button1 = tk.Button(buttonframe,text="ask llama",font = ('Arial',18),command=run_get_summary)
button1.grid(row=0,column=0,sticky=tk.W+tk.E)

button2 = tk.Button(buttonframe,text="url to transcript",font = ('Arial',18),command=run_get_transcript)
button2.grid(row=0,column=1,sticky=tk.W+tk.E)

button3 = tk.Button(buttonframe,text="url to video_url",font = ('Arial',18),command=run_get_video_url)
button3.grid(row=1,column=0,sticky=tk.W+tk.E)

button4 = tk.Button(buttonframe,text="try me",font = ('Arial',18), command = run_get_mystery_word)
button4.grid(row=1,column=1,sticky=tk.W+tk.E)

buttonframe.pack(fill= 'x')

label3 = tk.Label(root,text="ask what you want(by default get summary):", font = ('Arial',18))
label3.pack(padx=10,pady=10)

textbox3 = tk.Text(root,height=3,font = ('Arial',18))
textbox3.pack(padx=10,pady=10)

label2 = tk.Label(root,text="output:", font = ('Arial',18))
label2.pack(padx=10,pady=10)

textbox2 = tk.Text(root,height=15,font = ('Arial',18))
textbox2.pack(padx=10,pady=30)

root.mainloop()