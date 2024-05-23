import requests
import argparse
import sys
import threading
import time
import signal
from utilities import ANSI_color, loading_animation, banner

def fetch_user_data(repository_username):
    url = f"https://codeberg.org/api/v1/users/{repository_username}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        print(f"{ANSI_color.DARKRED}\n[!] Failed to fetch user data. Status code: {response.status_code}{ANSI_color.RESET}")
        return None

def count_languages(user_data):
    languages = {}
    for repo in user_data:
        language = repo['language']
        if language:
            languages[language] = languages.get(language, 0) + 1
    return languages

def exit_program(signal, frame):
    print(f"\n{ANSI_color.DARKRED}[-] Exiting the program ...{ANSI_color.RESET}")
    loading_complete.set()  # Set the event to exit the loading thread
    sys.exit(0)

# Read version and coder from file
def read_version_and_coder():
    version = None
    coder = None
    try:
        with open("version", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("version"):
                    version = line.split("=")[1].strip()
                elif line.startswith("coder"):
                    coder = line.split("=")[1].strip()
    except FileNotFoundError:
        print(f"{ANSI_color.DARKRED}Error: File 'version' not found.{ANSI_color.RESET}")
    except Exception as e:
        print(f"{ANSI_color.DARKRED}Error occurred while reading 'version': {str(e)}{ANSI_color.RESET}")
    return version, coder

version, coder = read_version_and_coder()
if version is None or coder is None:
    exit()

def main():
    global loading_complete
    loading_complete = threading.Event()

    signal.signal(signal.SIGINT, exit_program)
    signal.signal(signal.SIGTSTP, exit_program)

    parser = argparse.ArgumentParser(description="Fetch user data from Codeberg API")
    parser.add_argument("--user", type=str, help="Codeberg username")
    args = parser.parse_args()

    print(banner.BANNER)  # Print the banner

    # Print coder and version in different colors
    if version is not None and coder is not None:
        print(f"{ANSI_color.YELLOW}Coder: {coder:<50}{ANSI_color.GREEN}{version:>27}{ANSI_color.GREEN}")
    else:
        print(f"{ANSI_color.DARKRED}Error: Version or coder not found.{ANSI_color.RESET}")
        exit()

    
    if args.user:
        codeberg_api_url = f"https://codeberg.org/api/v1/users/{args.user}/repos"
        print(f"{ANSI_color.GREY}\n[~] Fetching data from: {codeberg_api_url}{ANSI_color.RESET}")
        loading = threading.Thread(target=loading_animation.loading_animation, args=(loading_complete,))
        loading.start()
        user_data = fetch_user_data(args.user)
        loading_complete.set()  # Stop the loading animation
        loading.join(timeout=0)  # Wait for the loading animation thread to finish
        sys.stdout.write("\r                                          \n")  # Clear loading animation
        if user_data:
            print(f"{ANSI_color.GREEN}[+] Retrieved {len(user_data)} Repositories{ANSI_color.RESET}")
            
            # Counting languages used across all repositories
            languages = count_languages(user_data)
            print(f"{ANSI_color.GREEN}[+] {args.user} has used {len(languages)} Language(s){ANSI_color.RESET}")
            for language, repository_count in languages.items():
                print(f"{ANSI_color.GREEN}[+] {language} has {repository_count} repositories using{ANSI_color.RESET}")

            print("\nListing all the repositories:\n")
            for repo in user_data:
                print(f"{ANSI_color.GREY}Full Name: {ANSI_color.RESET}{repo['full_name']}")
                print(f"{ANSI_color.GREY}Description: {ANSI_color.RESET}{repo['description'] if repo['description'] else 'NULL'}")
                print(f"{ANSI_color.GREY}Language: {ANSI_color.RESET}{repo['language'] if repo['language'] else 'NULL'}")
                print(f"{ANSI_color.GREY}Website: {ANSI_color.RESET}{repo['website'] if repo['website'] else 'NULL'}")
                print(f"{ANSI_color.GREY}Stars Count: {ANSI_color.RESET}{repo['stars_count']}")
                print(f"{ANSI_color.GREY}Forks Count: {ANSI_color.RESET}{repo['forks_count']}")
                print(f"{ANSI_color.GREY}Created At: {ANSI_color.RESET}{repo['created_at']}")
                print(f"{ANSI_color.GREY}Updated At: {ANSI_color.RESET}{repo['updated_at']}")
                print(f"{ANSI_color.GREY}{'-'*50}{ANSI_color.RESET}")  # Separating each repository with dashes
                time.sleep(0.1)
        else:
            print(f"{ANSI_color.GREY}The user {args.user} has no repositories.{ANSI_color.RESET}")
    else:
        print(f"{ANSI_color.GREY}Please provide a username using --user option.{ANSI_color.RESET}")

if __name__ == "__main__":
    main()
