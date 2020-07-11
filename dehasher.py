#!/usr/bin/python3

###########################################################################
#  Made by http://github.com/r4v10l1 for RaidForums.                      #
#  https://raidforums.com/User-FakeRavi0li                                #
#  Thanks to @Dark Lord, you are the best!                                #
#  This script dehashes an MD5 hash using https://md5decrypt.net/en/Api/  #
#  If it's not found, it bruteforces it with hashcat.                     #
###########################################################################

# Try importing stuff
try:
    import sys
    import os
    import requests
    import time
    from bs4 import BeautifulSoup
    from colorama import Fore, Style
except Exception:
    print()
    print(" [!] Error. Libraries not installed.")
    print(" [i] Run: pip install <package name>")
    print(" [i] Required packages: sys, os, requests, bs4, colorama, time.")
    print()
    exit(1)
#--------------------------------------------------------------------------------------------------
# Def the color types
def info_text(text):
    print(" %s%s[i] %s%s" % (Style.RESET_ALL, Fore.BLUE, text, Style.RESET_ALL))
def success_text(text):
    print(" %s%s%s[+] %s%s" % (Style.RESET_ALL, Style.BRIGHT, Fore.GREEN, text, Style.RESET_ALL))
def error_text(text):
    print(" %s%s%s[!] %s%s" % (Style.RESET_ALL, Style.BRIGHT, Fore.RED, text, Style.RESET_ALL))
def warning_text(text):
    print(" %s%s%s[!] %s%s" % (Style.RESET_ALL, Style.BRIGHT, Fore.YELLOW , text, Style.RESET_ALL))
def input_text(text):
    return input(" %s%s%s[*] %s >>%s " % (Style.RESET_ALL, Style.BRIGHT, Fore.BLUE, text, Fore.RESET))
#--------------------------------------------------------------------------------------------------
# FUNCTIONS

# Help message
def help_msg():
    print()
    print(" %s%s[%s%s—%s] Usagge: %s%s <mode> <target>" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.RESET, sys.argv[0]))
    print("  %s│" % Fore.BLUE)
    print("  %s│  │%s -s  --single %s-%s  Use -s for single hash format." % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET))
    print("  %s└──│%s -h  --hash   %s-%s  Use -h for only hash list (txt format) (If more than 400 will use hashcat)." % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET))
    print("  %s│  │%s -e  --email  %s-%s  Use -e for email:hash list (txt format) (It will convert to hash list and then use -h)." % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET))
    print("  %s│" % Fore.BLUE)
    print("  %s│" % Fore.BLUE)
    print("  %s└──│%s <target>     %s-%s  Put here your target (single hash or txt list)%s" % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET, Style.RESET_ALL))
    print()
    print(" %s%s[%s%s*%s] %sExample: %s%spython3 %s -s 1a79a4d60de6718e8e5b326e338ae533" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.WHITE, Style.RESET_ALL, Fore.WHITE, sys.argv[0]))
    print(" %s%s[%s%s*%s] %sExample: %s%spython3 %s -h hashfile.txt" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.WHITE, Style.RESET_ALL, Fore.WHITE, sys.argv[0]))
    print(" %s%s[%s%s*%s] %sExample: %s%spython3 %s -e emailfile.txt" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.WHITE, Style.RESET_ALL, Fore.WHITE, sys.argv[0]))
    print()
    exit(1)

# For -s
def single_mode_action():
    HASH = sys.argv[2]
    URL = "https://md5decrypt.net/en/Api/api.php?hash=%s&hash_type=%s&email=%s&code=%s" % (HASH, "md5", USER_EMAIL, API_CODE)
    PAGE = requests.get(URL, headers=HEADERS)  # Uses requests lib to get the content of the page
    PAGE_CONTENT = BeautifulSoup(PAGE.content, "html.parser").get_text()
    if "ERROR CODE : 001" in PAGE_CONTENT:
        print()
        error_text("Error. Day limit exceded, running hashcat...")
        more_than_400()
        exit(1)
    elif "ERROR CODE : 002" in PAGE_CONTENT:
        print()
        error_text("Error. Wrong email / code.")
        print()
        exit(1)
    elif "ERROR CODE : 005" in PAGE_CONTENT:
        print()
        error_text("Error. Wrong hash tipe. Only MD5 supported.")
        print()
        exit(1)
    if PAGE_CONTENT.strip() == "":
        print()
        error_text("Hash not found.")
        print()
        exit(1)
    else:
        success_text("Success! Hash found.")
        print(" " + HASH + Fore.RED +":" + Style.RESET_ALL + PAGE_CONTENT)
        exit(1)

# For -h
def hash_list_action():
    info_text("Checking the hashes. %sThis might take a while...")
    HASH_FILE = str(sys.argv[2])
    os.system("echo "" > results.txt")
    with open(HASH_FILE, "r") as reader:
        while True:
            line = reader.readline()
            if not line:
                break
            HASHED = line.strip()
            URL = "https://md5decrypt.net/en/Api/api.php?hash=%s&hash_type=md5&email=%s&code=%s" % (HASHED, USER_EMAIL, API_CODE)
            try:
                PAGE = requests.get(URL, headers=HEADERS)  # Uses requests lib to get the content of the page
                PAGE_CONTENT = BeautifulSoup(PAGE.content, "html.parser").get_text()
            except Exception as e:
                error_text("Exception happened while connecting to md5decrypt: ") + e
            if PAGE_CONTENT.strip() != "":
                if "error" not in PAGE_CONTENT.lower():
                    with open("results.txt", "a") as add_text: # this is better
                        add_text.write("{}:{}".format(HASHED, PAGE_CONTENT))
                elif "ERROR CODE : 002" in PAGE_CONTENT:
                    os.system("rm results.txt")
                    print()
                    print(" %s%s[!] Error. Wrong email / code.%s" % (Style.RESET_ALL, Fore.RED, Style.RESET_ALL))
                    print()
                    exit(1)
    os.system("echo "" >> results.txt")
    success_text("All done! Results sent to results.txt [hash:text]")
    warning_text("Make sure to move results.txt if you are going to run the script again. It will delete the actual one!")
    print()
    exit(1)

# For -e ### WORKING ON IT
def email_list_action():
    info_text("Installing awk if not installed...")
    os.system("apt-get -qq install -y awk 2> /dev/null")
    HASH_FILE = str(sys.argv[2])
    info_text("Changing email:hash to hash...")
    os.system("awk -F: \'{print $2}\' %s > only_hahes.txt" % HASH_FILE)
    HASH_FILE = "only_hahes.txt"
    os.system("echo "" > results.txt")
    info_text("Checking the hashes. This might take a while...")
    with open(HASH_FILE, "r") as reader:
        while True:
            line = reader.readline()
            if not line:
                break
            HASHED = line.strip()
            URL = "https://md5decrypt.net/en/Api/api.php?hash=%s&hash_type=md5&email=%s&code=%s" % (HASHED, USER_EMAIL, API_CODE)
            try:
                PAGE = requests.get(URL, headers=HEADERS)  # Uses requests lib to get the content of the page
                PAGE_CONTENT = BeautifulSoup(PAGE.content, "html.parser").get_text()
            except Exception as e:
                error_text("Exception happened while connecting to md5decrypt: ") + e
            if PAGE_CONTENT.strip() != "":
                if "error" not in PAGE_CONTENT.lower():
                    with open("results.txt", "a") as add_text: # this is better
                        add_text.write("{}:{}".format(HASHED, PAGE_CONTENT))
                elif "ERROR CODE : 002" in PAGE_CONTENT:
                    os.system("rm results.txt")
                    print()
                    print(" %s%s[!] Error. Wrong email / code.%s" % (Style.RESET_ALL, Fore.RED, Style.RESET_ALL))
                    print()
                    exit(1)
    os.system("echo "" >> results.txt")
    success_text("All done! Results sent to results.txt [hash:text]")
    warning_text("Make sure to move results.txt if you are going to run the script again. It will delete the actual one!")
    print()
    exit(1)
#--------------------------------------------------------------------------------------------------
# Parse the arguments
if len(sys.argv) == 1:
    help_msg()
elif len(sys.argv) == 2:
    if "-h" in sys.argv[1]:
        help_msg()
    else:
        print()
        error_text("Error. Not enough arguments.")
        print()
        exit(1)
elif len(sys.argv) == 3:
    if "-s" in str(sys.argv[1]).strip() and ".txt" in str(sys.argv[2]):
        print()
        error_text("Error. Type -h to use a hash list.")
        print()
        exit(1)
    if "-h" == str(sys.argv[1]).strip() and ".txt" not in str(sys.argv[2]):
        print()
        error_text("Error. Type -s to check a single hash.")
        print()
        exit(1)
    if "-e" == str(sys.argv[1]).strip() and ".txt" not in str(sys.argv[2]):
        print()
        error_text("Error. Type -s to check a single hash.")
        print()
        exit(1)
elif len(sys.argv) > 3:
    print()
    error_text("Error. Too many arguments.")
    print()
    exit(1)
#--------------------------------------------------------------------------------------------------
# Banner
def banner():
    os.system("clear")
    print("%s%s ___  ________ _____ " % (Style.BRIGHT, Fore.WHITE))
    print(" |  \/  |  _  \  ___|        __     __               __   %sby @r4v10l1 %s%s%s" % (Style.DIM, Style.RESET_ALL, Style.BRIGHT, Fore.WHITE))
    print(" | .  . | | | |___ \    ____/ /__  / /_  ____ ______/ /_  ___  _____")
    print(" | |\/| | | | |   \ \  / __  / _ \/ __ \/ __ `/ ___/ __ \/ _ \/ ___/")
    print(" | |  | | |/ //\__/ / / /_/ /  __/ / / / /_/ (__  ) / / /  __/ /")
    print(" \_|  |_/___/ \____/  \__,_/\___/_/ /_/\__,_/____/_/ /_/\___/_/%s" % Fore.BLUE)
    print()
    print()
try:
    banner()
except KeyboardInterrupt:
    print()
    error_text("Detected Ctrl+C. Shutting down...")
    exit(1)
#--------------------------------------------------------------------------------------------------
# Loading (not necessary tho)
def loading():
    chars = "/—\|"
    for char in chars:
        sys.stdout.write('\r'+' [i] Loading...'+char)
        time.sleep(.1)
        sys.stdout.flush()
n = 4
try:
    for i in range(n):
        loading()
    sys.stdout.write('\r')
except KeyboardInterrupt:
    print()
    error_text("Detected Ctrl+C. Shutting down...")
    exit(1)
#--------------------------------------------------------------------------------------------------
# Hashcat
def more_than_400():
    try:
        WORDLIST = input(" %s%s[*] Wordlist path >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.RESET))
        info_text("Running hashcat, this may take a while...")
        HASH = str(sys.argv[2])
        os.system("hashcat -m 0 -a 0 %s %s 2>&1 /dev/null" % (HASH, WORDLIST))
        os.system("hashcat -m 0 -a 0 %s %s --show > results.txt" % (HASH, WORDLIST))
        info_text("All done, results are in \"results.txt\"")
        print()
        exit(1)
    except KeyboardInterrupt:
        print()
        error_text("Detected Ctrl+C. Shutting down...")
        exit(1)

if sys.argv[1] != "-s":
    COUNT_LINES = sum(1 for line in open(str(sys.argv[2])))
    if COUNT_LINES > 400:
        if sys.argv[1] == "-h":
            info_text("The hash list is too long. Using hashcat.")
            more_than_400()
            exit(1)
        elif sys.argv[1] == "-e":
            print()
            error_text("Error. More than 400 lines/day are not suported in email mode.")
            print()
            exit(1)
#--------------------------------------------------------------------------------------------------
# Email code
try:
    USER_EMAIL = input_text("Your email")
    data = {'email_api':USER_EMAIL}
    try:
        r = requests.post("https://md5decrypt.net/en/Api/", data=data)
    except Exception:
        error_text("Error. Request failed.")
        print()
        exit(1)
    input(" %s%s[i] A verification code has been sent for the use of the API. %sPress Enter to continue..." % (Style.RESET_ALL, Fore.BLUE, Fore.RESET))
    API_CODE = input(" %s%s[*] Your code >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.RESET))
except KeyboardInterrupt:
    print()
    error_text("Detected Ctrl+C. Shutting down...")
    exit(1)
#--------------------------------------------------------------------------------------------------
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173"}  # You can replace here your user agent.

# Check the if sys.argv is -s
if sys.argv[1] == "-s":
    single_mode_action()
#--------------------------------------------------------------------------------------------------
# Check the if sys.argv is -h
if sys.argv[1] == "-h":
    hash_list_action()
#--------------------------------------------------------------------------------------------------
# Check the if sys.argv is -e
if sys.argv[1] == "-e":
    email_list_action()

exit(1)
