from imports.masterlist import MasterList
from pathlib import Path
import argparse

print("""
********************************************************************************
* Use this script to create a short version of master.txt. This can be helpful
* for a variety of reasons.
*
* Do something like:
*   python3 shorten.py 300
*
* This will give you master_short.txt containing only 300 words.
********************************************************************************
""")

# Arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("words",
  type = int,
  help = "The number of words you want to dump to master_short.txt")

args = argparser.parse_args()

def main():
  master = MasterList()
  shortListPath = Path(master.wordlistPath, "master_short.txt")
  shortList = master.makeShortVersion(args.words)
  shortList.sort()

  with open(shortListPath, "w") as shortFile:
    for word in shortList:
      shortFile.write(word + "\n")
  print(f"{shortListPath} created.")
main()