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
    import sys, os, requests, time, hashlib
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
# Help message
def help_msg():
    print()
    print(" %s%s[%s%s—%s] Usagge: %s%s <mode> <target>" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.RESET, sys.argv[0]))
    print("  %s│" % Fore.BLUE)
    print("  %s│  │%s -s  --single  %s-%s  Use -s for single hash format." % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET))
    print("  %s│  │%s -d  --dehash  %s-%s  Use -d for dehashing a hash list (txt format) using the API (If more than 400 will use hashcat)." % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET))
    print("  %s└──│%s -e  --email   %s-%s  Use -e for email:hash list (txt format) (It will convert to hash list and then use -d)." % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET))
    print("  %s│  │%s -h  --hash    %s-%s  Use -h for hashing a single string or a .txt file with strings." % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET))
    print("  %s│  │%s -c  --check   %s-%s  Use -c for checking if 2 hashes match (see examples)." % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET))
    print("  %s│" % Fore.BLUE)
    print("  %s│" % Fore.BLUE)
    print("  %s└──│%s <target>     %s-%s  Put here your target (single hash or txt list)%s" % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET, Style.RESET_ALL))
    print()
    print(" %s%s[%s%s*%s] %sExample: %s%spython3 %s -s 1a79a4d60de6718e8e5b326e338ae533" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.WHITE, Style.RESET_ALL, Fore.WHITE, sys.argv[0]))
    print(" %s%s[%s%s*%s] %sExample: %s%spython3 %s -d hashfile.txt" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.WHITE, Style.RESET_ALL, Fore.WHITE, sys.argv[0]))
    print(" %s%s[%s%s*%s] %sExample: %s%spython3 %s -e emailfile.txt" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.WHITE, Style.RESET_ALL, Fore.WHITE, sys.argv[0]))
    print(" %s%s[%s%s*%s] %sExample: %s%spython3 %s -h IWantToBeHased" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.WHITE, Style.RESET_ALL, Fore.WHITE, sys.argv[0]))
    print(" %s%s[%s%s*%s] %sExample: %s%spython3 %s -c example:1a79a4d60de6718e8e5b326e338ae533" % (Style.BRIGHT, Fore.BLUE, Style.RESET_ALL, Fore.BLUE, Style.BRIGHT, Fore.WHITE, Style.RESET_ALL, Fore.WHITE, sys.argv[0]))
    print()
    exit(1)
#--------------------------------------------------------------------------------------------------
# No API

# For -h
def text2md5_beautiful(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return success_text("Your text (%s%s%s%s%s%s) has been hashed: %s%s%s%s" % (Style.RESET_ALL, Fore.WHITE, text, Style.RESET_ALL, Style.BRIGHT, Fore.GREEN, Style.RESET_ALL, Style.BRIGHT, Fore.WHITE, m.hexdigest()))  # Why the fuck I didn't think of this at that time...

# For -h with text and -c
def text2md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    result = str(m.hexdigest())
    return result

# For -h with txt
def text2md5_txt():
    print()
    info_text("Hashing. This might take a while...")
    str_file = str(sys.argv[2])
    os.system("echo "" > hashing_results.txt")
    with open(str_file, "r") as reader:  # Yo like this is the root_flag.txt from life man. Thanks Dark Lord
        while True:
            line = reader.readline()
            if not line:  # This too u_u
                break
            string2hash = line.strip()
            md5hash = text2md5(string2hash)
            with open("hashing_results.txt", "a") as add_text:
                add_text.write("{}:{}\n".format(string2hash, md5hash))
    os.system("echo "" >> hashing_results.txt")
    success_text("All done! Results sent to hashing_results.txt [text:hash]")
    warning_text("Make sure to move hashing_results.txt if you are going to run the script again. It will delete the actual one!")
    print()
    exit(1)

# For -c
def hashStringCheck(text):
    not_hash = str(text.split(":")[0])
    hash = str(text.split(":")[1])
    if len(hash) != 32:
        print()
        error_text("Error. The hash you entered was not MD5.")
        print()
        exit(1)
    md5hash = text2md5(not_hash)
    if md5hash == hash:
        print()
        success_text("The hash match with the text!")
        print()
    else:
        print()
        error_text("The hash does not match with the text...")
        print()
    exit(1)

#--------------------------------------------------------------------------------------------------
# Banner and loading animation for more API ussage

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
# Loading (not necessary tho)
def loading():
    chars = "/—\|"
    for char in chars:
        sys.stdout.write('\r'+' [i] Loading...'+char)
        time.sleep(.1)
        sys.stdout.flush()
# Loading animation
def loading_4():
    n = 4
    for i in range(n):
        loading()
    sys.stdout.write('\r')
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

# Check the file lenght
def check_more_than_400():
    COUNT_LINES = sum(1 for line in open(str(sys.argv[2])))
    if COUNT_LINES > 400:
        if sys.argv[1] == "-d":
            info_text("The hash list is too long. Using hashcat.")
            more_than_400()
            exit(1)
        elif sys.argv[1] == "-e":
            print()
            error_text("Error. More than 400 lines/day are not suported in email mode.")
            print()
            exit(1)
        else:
            print()
            error_text("Unknown error. Code: 3")
            print()
            exit(1)
#--------------------------------------------------------------------------------------------------
# API modes

### NOT USEFUL ###
# Email code
# USER_EMAIL = ""
# API_CODE = ""
# def email_code():
#     HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173"}  # You can replace here your user agent.
#     try:
#         USER_EMAIL = input_text("Your email")
#         data = {'email_api':USER_EMAIL}
#         try:
#             r = requests.post("https://md5decrypt.net/en/Api/", data=data)
#         except Exception:
#             error_text("Error. Request failed.")
#             print()
#             exit(1)
#         input(" %s%s[i] A verification code has been sent for the use of the API. %sPress Enter to continue..." % (Style.RESET_ALL, Fore.BLUE, Fore.RESET))
#         API_CODE = input(" %s%s[*] Your code >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.RESET))
#     except KeyboardInterrupt:
#         print()
#         error_text("Detected Ctrl+C. Shutting down...")
#         exit(1)
#################

# For -s
def single_mode_action():
    try:
        banner()
        loading_4()
        check_more_than_400()
    except KeyboardInterrupt:
        print()
        error_text("Detected Ctrl+C. Shutting down...")
        exit(1)
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173"}  # You can replace here your user agent.
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

# For -d
def hash_list_action():
    try:
        banner()
        loading_4()
        check_more_than_400()
    except KeyboardInterrupt:
        print()
        error_text("Detected Ctrl+C. Shutting down...")
        exit(1)
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173"}  # You can replace here your user agent.
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
    info_text("Checking the hashes. This might take a while...")
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
                    with open("results.txt", "a") as add_text: # THANKS DARK LORD I LOVE YOU <3<3<3<3<3<3<3
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

# For -e
def email_list_action():
    try:
        banner()
        loading_4()
    except KeyboardInterrupt:
        print()
        error_text("Detected Ctrl+C. Shutting down...")
        exit(1)
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173"}  # You can replace here your user agent.
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
# Check for argument errors
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
    if "-s" in str(sys.argv[1]).strip():
        if ".txt" in str(sys.argv[2]):
            print()
            error_text("Error. Type -d to use a hash list.")
            print()
            exit(1)
        elif len(str(sys.argv[2])) != 32:
            print()
            error_text("Error. Invalid hash type (only md5).")
            print()
            exit(1)
    elif "-d" in str(sys.argv[1]).strip():
        if ".txt" not in str(sys.argv[2]):
            print()
            error_text("Error. Type -s to check a single hash.")
            print()
            exit(1)
    elif "-e" in str(sys.argv[1]).strip() and ".txt" not in str(sys.argv[2]):
        print()
        error_text("Error. Type -s to check a single hash.")
        print()
        exit(1)
    elif "-c" in str(sys.argv[1]).strip():
        if ".txt" in str(sys.argv[2]):
            print()
            error_text("Error. Can't check files. Type -h to see the full help.")
            print()
            exit(1)
        elif ":" not in str(sys.argv[2]):
            print()
            error_text("Error. You must use text:hash format")
            print()
            exit(1)
elif len(sys.argv) > 3:
    print()
    error_text("Error. Too many arguments.")
    print()
    exit(1)
#--------------------------------------------------------------------------------------------------
# Check sys.argv[1] (MAIN)

# Check the if sys.argv is -s
if "-s" in sys.argv[1]:
    single_mode_action()
# Check the if sys.argv is -d
elif "-d" in sys.argv[1]:
    hash_list_action()
# Check the if sys.argv is -e
elif "-e" in sys.argv[1]:
    email_list_action()
# Check the if sys.argv is -h
elif "-h" in sys.argv[1]:
    if ".txt" not in str(sys.argv[2]):
        text2md5_beautiful(str(sys.argv[2]))
    elif ".txt" in str(sys.argv[2]):
        text2md5_txt()
    else:
        error_text("Unknown error. Code: 1")
# Check the if sys.argv is -c
elif "-c" in sys.argv[1]:
    hashStringCheck(str(sys.argv[2]))
else:
    error_text("Unknown error. Code: 2")

exit(1)
