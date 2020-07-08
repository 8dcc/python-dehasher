#!/usr/bin/python3

###########################################################################
#  Made by http://github.com/r4v10l1 for RaidForums.                      #
#  https://raidforums.com/User-FakeRavi0li                                #
#  This script dehashes an MD5 hash using https://md5decrypt.net/en/Api/  #
#  If it's not found, it bruteforces it with hashcat.                     #
###########################################################################
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
    print(" [i] Required packages: sys, os, requests, bs4, colorama, time")
    print()
    exit(1)

#CHECK-ARGS-ARE-CORRECT----------------------------------------------------------------

if len(sys.argv) == 1:
    print(" %s%s[-] Usagge: %s%s -e <target>" % (Style.BRIGHT, Fore.BLUE, Fore.RESET, sys.argv[0]))
    print("  %s│" % Fore.BLUE)
    print("  %s│  │%s -s  --single %s-%s  Use -s for single hash format." % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET))
    print("  %s└──│%s%s COMING SOON..." % (Fore.BLUE, Style.DIM, Fore.RESET))
    print("  %s│  │%s%s COMING SOON..." % (Fore.BLUE, Style.DIM , Fore.RESET))
    print("  %s│" % Fore.BLUE)
    print("  %s│" % Fore.BLUE)
    print("  %s└──│%s <target>     %s-%s  Put here your target (single hash, list comming soon)%s" % (Fore.BLUE, Fore.RESET, Fore.BLUE, Fore.RESET, Style.RESET_ALL))
    print()
    exit(1)
elif len(sys.argv) == 2:
    print()
    print(" %s%s[!] Error. Not enough arguments.%s" % (Style.BRIGHT, Fore.RED, Fore.RESET))
    print()
    exit(1)
elif len(sys.argv) == 3:
    if "-s" not in str(sys.argv[1]).strip():
        print()
        print(" %s%s[!] Error. Type -s for single hash. Multiple hashes comming soon.%s" % (Style.BRIGHT, Fore.RED, Fore.RESET))
        print()
        exit(1)
    elif ".txt" in str(sys.argv[2]):
        print()
        print(" %s%s[!] Error. Multiple hashes not supported in this version.%s" % (Style.BRIGHT, Fore.RED, Fore.RESET))
        print()
        exit(1)
    elif len(str(sys.argv[2])) != 32:
        print()
        print(" %s%s[!] Error. Invalid hash type. Only supported md5.%s" % (Style.BRIGHT, Fore.RED, Fore.RESET))
        print()
        exit(1)
elif len(sys.argv) > 3:
    print()
    print(" %s%s[!] Error. Too many arguments.%s" % (Style.BRIGHT, Fore.RED, Fore.RESET))
    print()
    exit(1)
#--------------------------------------------------------------------------------------------------

# Banner
def banner():
    os.system("clear")
    print("%s%s ___  ________ _____ " % (Style.BRIGHT, Fore.WHITE))
    print(" |  \/  |  _  \  ___|        __     __               __   %sby @r4v10l1%s" % (Style.DIM, Style.BRIGHT))
    print(" | .  . | | | |___ \    ____/ /__  / /_  ____ ______/ /_  ___  _____")
    print(" | |\/| | | | |   \ \  / __  / _ \/ __ \/ __ `/ ___/ __ \/ _ \/ ___/")
    print(" | |  | | |/ //\__/ / / /_/ /  __/ / / / /_/ (__  ) / / /  __/ /")
    print(" \_|  |_/___/ \____/  \__,_/\___/_/ /_/\__,_/____/_/ /_/\___/_/%s" % Fore.BLUE)
    print()
    print()

banner()
#--------------------------------------------------------------------------------------------------

# Loading
def loading():
    chars = "/—\|"
    for char in chars:
        sys.stdout.write('\r'+' [i] Loading...'+char)
        time.sleep(.1)
        sys.stdout.flush()

n = 4
for i in range(n):
    loading()
sys.stdout.write('\r')
#--------------------------------------------------------------------------------------------------

# Email code
try:
    USER_EMAIL = input(" %s%s[*] Your email >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.RESET))
    data = {'email_api':USER_EMAIL}
    try:
        r = requests.post("https://md5decrypt.net/en/Api/", data=data)
    except Exception:
        print(" %s%s[!] Error. Request failed.%s" % (Style.BRIGHT, Fore.RED, Fore.RESET))
        print()
        exit(1)
    input(" %s%s[i] A verification code has been sent for the use of the API. %sPress Enter to continue..." % (Style.RESET_ALL, Fore.BLUE, Fore.RESET))
    API_CODE = input(" %s%s[*] Your code >> %s" % (Style.BRIGHT, Fore.BLUE, Fore.RESET))
except KeyboardInterrupt:
    print()
    print(" %s%s[!] Detected Ctrl+C. Shutting down...%s" % (Style.RESET_ALL, Fore.BLUE, Style.RESET_ALL))
    exit(1)
#--------------------------------------------------------------------------------------------------

# Request
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.173"}  # You can replace here your user agent.
def make_request() :
    URL = "https://md5decrypt.net/en/Api/api.php?hash=%s&hash_type=%s&email=%s&code=%s" % (HASH, "md5", USER_EMAIL, API_CODE)
    PAGE = requests.get(URL, headers=HEADERS)  # Uses requests lib to get the content of the page
    PAGE_CONTENT = BeautifulSoup(PAGE.content, "html.parser").get_text()
#--------------------------------------------------------------------------------------------------

# Check the if sys.argv is -s
if sys.argv[1] == "-s":
    HASH = sys.argv[2]
    URL = "https://md5decrypt.net/en/Api/api.php?hash=%s&hash_type=%s&email=%s&code=%s" % (HASH, "md5", USER_EMAIL, API_CODE)
    PAGE = requests.get(URL, headers=HEADERS)  # Uses requests lib to get the content of the page
    PAGE_CONTENT = BeautifulSoup(PAGE.content, "html.parser").get_text()
    if "ERROR CODE : 001" in PAGE_CONTENT:
        print()
        print(" %s%s[!] Error. Day limit exceded, running hashcat...%s" % (Style.RESET_ALL, Fore.RED, Style.RESET_ALL))
        more_than_400()
        exit(1)
    elif "ERROR CODE : 002" in PAGE_CONTENT:
        print()
        print(" %s%s[!] Error. Wrong email / code.%s" % (Style.RESET_ALL, Fore.REED, Style.RESET_ALL))
        print()
        exit(1)
    elif "ERROR CODE : 005" in PAGE_CONTENT:
        print()
        print(" %s%s[!] Error. Wrong hash tipe. Only MD5 supported.%s" % (Style.RESET_ALL, Fore.RED, Style.RESET_ALL))
        print()
        exit(1)
    if PAGE_CONTENT.strip() == "":
        print()
        print(" %s%s[!] Hash not found.%s" % (Style.RESET_ALL, Fore.RED, Style.RESET_ALL))
        print()
        exit(1)
    else:
        print(" %s%s[+] Success! Hash found.%s" % (Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL))
        print(" " + HASH + Fore.RED +":" + Style.RESET_ALL + PAGE_CONTENT)
        exit(1)

exit(1)
