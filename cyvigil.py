#!/usr/bin/env python3

import google.generativeai as genai
import os
import sys
import re # Import regex module for cleaning text
from dotenv import load_dotenv

# --- ANSI Color Codes ---
# These codes allow you to print colored text in the terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m' # Resets the color to default

# --- Configuration ---
# Construct the path to the .env file relative to the script's location
# This ensures the script can be run from any directory
dotenv_path = os.path.join(os.path.dirname(__file__), 'api', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Retrieve API key from environment variable
# It's crucial that your API key is defined in api/.env as GEMINI_API_KEY="YOUR_KEY"
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print(f"{RED}Error: GEMINI_API_KEY environment variable not found.{RESET}", file=sys.stderr)
    print(f"{YELLOW}Please ensure your API key is set in 'api/.env' like this:{RESET}", file=sys.stderr)
    print(f"{YELLOW}  GEMINI_API_KEY=\"YOUR_ACTUAL_API_KEY_HERE\"{RESET}", file=sys.stderr)
    sys.exit(1)

# Configure the Generative AI client with your API key
genai.configure(api_key=API_KEY)

# Define the Gemini model to use
# Based on your finding from AI Studio's curl command, 'models/gemini-2.0-flash' is the correct one.
GEMINI_MODEL = 'models/gemini-2.0-flash'

# --- Text Cleaning Function ---
def clean_response_text(text: str) -> str:
    """
    Removes common Markdown formatting characters (like stars for lists/bold)
    and cleans up extra whitespace for a plain text output.
    """
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove leading list stars and hyphens with optional spaces (e.g., "* Item", "- Item")
        line = re.sub(r'^\s*[\*\-]\s*', '', line).strip()
        
        # Remove bold markdown (**text**)
        # This regex replaces **text** with text. Handles cases where ** might be inside a line.
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line) 
        
        # Remove any remaining single asterisks if they seem like emphasis, being careful not to remove all
        # This is a bit more aggressive and might remove legitimate asterisks.
        # Consider if you truly want ALL asterisks gone, or just markdown ones.
        # For this request, we'll aim to remove common markdown *bold* and *italic*
        line = re.sub(r'\*(.*?)\*', r'\1', line) # Removes *italic* around text

        # Remove multiple spaces
        line = re.sub(r'\s+', ' ', line).strip()
        
        if line: # Only add non-empty lines
            cleaned_lines.append(line)
            
    # Join lines with a single newline, and filter out any empty lines that might result from stripping
    return '\n'.join(cleaned_lines)


# --- Gemini Interaction Function ---
def get_gemini_response(prompt_text: str) -> str:
    """
    Sends a prompt to the configured Gemini model and returns the response text.
    Handles potential API errors.
    """
    try:
        # Initialize the Generative Model with the specified model name
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Send the prompt to the model to generate content
        response = model.generate_content(prompt_text)
        
        # Return the generated text content
        # Check if response.text exists before returning
        if response and hasattr(response, 'text'):
            return response.text
        else:
            return "No text content received from Gemini."
    except Exception as e:
        # Catch any exceptions that occur during the API call and return an error message
        return f"An error occurred while getting a response from Gemini: {e}"

# --- Main Program Logic ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        # --- Interactive Mode ---
        print(f"{BLUE}--- Welcome to Your Gemini Assistant ---{RESET}")
        print(f"{BLUE}---Github: By MrpasswordTz---{RESET}")
        print(f"{BLUE}Type your prompt below or '{RED}exit{BLUE}' to quit.{RESET}")
        print(f"{BLUE}--------------------------------------{RESET}")

        while True:
            try:
                user_input = input(f"\n{YELLOW}You: {RESET}") # User input prompt
                
                if user_input.lower() in ['exit', 'quit']:
                    print(f"{MAGENTA}Exiting Gemini Assistant. Goodbye!{RESET}")
                    break

                if not user_input.strip():
                    print(f"{RED}Please enter a prompt.{RESET}")
                    continue

                print(f"{CYAN}Sending prompt to Gemini ({GEMINI_MODEL}): '{user_input}'...{RESET}")
                print(f"{CYAN}Thinking...{RESET}")

                gemini_output = get_gemini_response(user_input)
                cleaned_output = clean_response_text(gemini_output) # Clean the output

                print(f"\n{GREEN}--- Gemini's Response ---{RESET}")
                print(f"{WHITE}{cleaned_output}{RESET}") # Print cleaned response in white
                print(f"{GREEN}------------------------{RESET}")

            except EOFError: # Handles Ctrl+D (end of file)
                print(f"\n{MAGENTA}Exiting Gemini Assistant. Goodbye!{RESET}")
                break
            except KeyboardInterrupt: # Handles Ctrl+C
                print(f"\n{MAGENTA}Exiting Gemini Assistant. Goodbye!{RESET}")
                break
            except Exception as e:
                print(f"{RED}An unexpected error occurred: {e}{RESET}")

    else:
        # --- Command-Line Argument Mode (for single prompts) ---
        user_prompt = " ".join(sys.argv[1:])

        print(f"{CYAN}Sending prompt to Gemini ({GEMINI_MODEL}): '{user_prompt}'...{RESET}")
        print(f"{CYAN}Thinking...{RESET}")

        gemini_output = get_gemini_response(user_prompt)
        cleaned_output = clean_response_text(gemini_output) # Clean the output

        print(f"\n{GREEN}--- Gemini's Response ---{RESET}")
        print(f"{WHITE}{cleaned_output}{RESET}") # Print cleaned response in white
        print(f"{GREEN}------------------------{RESET}")
