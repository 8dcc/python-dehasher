# Python dehasher

Uses ```https://md5decrypt.net/en/Api/``` to dehash MD5 hashes.

### Description
Added multiple hash support on .txt format!

If the .txt hash list is > than 400 lines, it uses hashcat.

Added email:hash mode!

Converts that file into a new only-hash file.

The API has a limit of 400 total hashes/day.

### Installation
```bash
git clone https://github.com/r4v10l1/python_dehasher
cd python_dehasher
python3 dehasher.py -h  # View the help
```
