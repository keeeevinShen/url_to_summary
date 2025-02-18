Ask llama with your lecture url(for U-M student)(only works when your lecture have trnscript provided)



#use bash shell

Part1: if you are alreay using bash shell and have homebrew installed, skip and go to Part2

1:#switch to bash


chsh -s /bin/bash     


and close and reopen terminal


2:#download homebrew


/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


3:#add to PATH


echo 'PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile   




Part2:


Go to browser and download Ollama.  then add to your application. then open it. and install ollama. 


step1:    chmod +x install.sh

step2:     bash install.sh


then you can just run the main_for_sum.py file ( using ide or simply run in terminal)

to run in terminal:

python3 main_for_sum.py



PS: since this is running locally, the llm might be a little stupid, if you like, you could choose to get the transcript and ask AI yourself. 


To get the transcript just select one word in transcript and then press (command + a) 


You can also modify the get_transcript_summary.py to achieve auto login and use your own API key (why didn't i set it up? yeah... im not paying for that shoot)



