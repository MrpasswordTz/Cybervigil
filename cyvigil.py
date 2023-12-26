import openai
import time
from openai import ChatCompletion
import pyfiglet
from getpass import getpass  # getpass for secure input
from colorama import Fore, Style

def print_typewriter_coloured(text):
    # Font size escape sequence
    font_size = "\033[2m" # This sets the font size to a smaller value, adjust according to your preference
    
    for char in text:
        color = Fore.RED #you can use anything
        print(f"{font_size}{color}{char}{Style.RESET_ALL}", end='', flush=True)
        time.sleep(0.01)    

text = "CyberVigil ...."
ascii_art = pyfiglet.figlet_format(text)
print_typewriter_coloured(ascii_art)

creator = "Created By: MrpasswordTz"
print(f"\n\n{creator}\n\n")

api_key = getpass(prompt='Enter your OpenAI API key: ')
openai.api_key = api_key

while True:
    print("Ask Anything:")
    user_input = input().strip()
    messages = [
        {"role": "system", "content": "You: " + user_input}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        generated_text = response.choices[0].message.content.strip()
        print_typewriter_coloured(generated_text)

        inp = input("\n\n\n\n\n\nPress q to quit, c to continue: ")
        if inp == "q":
            contr = Fore.GREEN + "Great Thank To BongoCoders" + Style.RESET_ALL
            print(contr)
            break
        else:
            continue

    except Exception as e:
        print(f"An error occurred: {e}")