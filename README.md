Ask llama with your lecture url(for U-M student)



#use bash shell
chsh -s /bin/bash 

#download homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


#add to PATH
echo 'PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile   



step1:    chmod +x install.sh

step2:     bash install.sh

step3:      open vscode and run the main_for_sum.py 



PS: since this is running locally, the llm might be a little stupid, if you like, you could choose to get the transcript and ask AI yourself. 

To get the transcript just select one word in transcript and then press (command + a) 


for cs students, You can also modify the get_transcript_summary.py to achieve auto login and use your own API key (why didn't i set it up? yeah... im not paying for that shoot)



