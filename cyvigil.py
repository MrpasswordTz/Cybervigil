import openai
import time
from openai import ChatCompletion
from getpass import getpass  # getpass for secure input

text = """ ⣿⣿⣿⣿⣿⣿⣿⣿⡋⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠋⠉⠉⠀⢁⣠⣀⣤⠁⠈⢻⣿⡇⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠰⣿⠉⠹⠋⠘⠛⠛⠛⠛⠛⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣀⡤⠀⠐⠋⠉⢛⡛⠻⣿⣤⡘⣿⣿⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⠟⢻⠉⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠉⢿⣿⣿⣿⣿⣿⣏⠄⣠⠀⠀⢀⣀⠈⢑⣿⣿⣿⣿⣿⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣧⠆⠚⠦⠐⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠓⠀⠀⢀⠀⠀⢹⠀⣀⠊⠀⠀⠀⢀⣀⣤⣴⣄⣰⣆⢈⣿⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣤⣷⣾⣿⣿⣿⣿⣿⠀⢰⣿⡟⣿⣿⣿⣿⣿⣿⣿⠀⢰⣆⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢰⣦⠀⡀⠈⠀⠀⢪⣾⣿⣷⣷⣶⣾⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢻⣟⣴⣿⣿⣿⣿⣿⣿⣿⣧⠈⠻⣷⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⠿⠿⠿⣿⣿⣿⡟⢠⠍⠀⣷⠀⠀⠀⠘⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⢀⣀⣀⣀⣉⣋⣭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣤⣤⡄⠄⠀⠀⠀⠀⣠⡏⠀⠀⠋⣇⠀⢢⠀⠙⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡄⢸⠟⢡⣿⣿⣿⡿⢛⣋⣥⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠁⠃⠀⠀⠀⠈⠆⠹⡅⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢠⣿⣿⡟⠁⠀⠟⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠹⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⠘⠋⢹⣿⠟⠉⢉⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⣿⠟⠋⠀⠀⠀⠀⠈⠛⠃⠁⢿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⣧⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣴⣄⣀⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣄⣾⣧⣧⣯⣿⣿⠿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏
⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⠻⠿⠿⠿⠛⠛⠛⠛⢛⣻⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢀⣠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣠⣴
⣿⣿⣿⣿⣿⣶⣦⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⣯⣿⣿⣿⣿⣿⣿⣷⣶⣤⣠⣴⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⢀⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣰⣿⣿⣿
⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠘⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢉⢦⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣶⣍⢻⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠑⢁⡟⣸⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣆⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠈⠉⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⣠⡞⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⢼⠀⢉⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⠈⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⣀⠀⠀⢀⣠⠀⠀⠀⠀⠉⠛⢿⣿⣿⣿⠻⡿⣿⡿⠿⠋⠁⠀⠠⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣇⠸⣿⣿⣿⣿⣿⡟⠁⠀⠀⣿⠀⢠⣿⣿⣧⣀⠀⠀⠀⠀⠀⠀⠀⠠⢀⠀⠔⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢹⣿⣿⣿⣿⡇⠀⠀⠀⣿⡄⣼⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣸⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠈⣿⣿⣿⣿⣷⣧⣻⡆⣿⣷⡘⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣧⢸⣿⣷⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠘⣿⣿⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠐⠆⠀⠀⠀⠈⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ """

print(text)

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