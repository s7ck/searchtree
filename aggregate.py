from pathlib import Path
from time import time
import os
import multiprocessing
import logging
import re

logging.basicConfig(
  format = "%(asctime)s: %(message)s",
  level = logging.INFO,
  datefmt = "%H:%M:%S"
)

class Aggregator:
  def __init__(self):
    self.wordlistDir = Path("wordlists/")
    self.pathToMaster = Path(self.wordlistDir, "master.txt")
    self.files = [] # List of Paths
    self.masterList = []
    self.broken = ""
    self.wordPattern = re.compile("^[A-Za-z]+[A-Za-z-]*$")

    # This is only here because opening the master file for writing with "w"
    # wasn't actually overwriting all of the data in the file for some reason.
    # This bug was noticed on Ubuntu 18 and not tested on any other OS.
    if self.pathToMaster.exists():
      os.remove(self.pathToMaster)

  def fmtNum(self, num):
    return "{:,}".format(num)

  def gatherFiles(self):
    [self.files.append(file) for file in self.wordlistDir.iterdir()]
    logging.info(f"There are {len(self.files)} wordlist files to merge.")


  def getWordsFromFile(self, file):
    wordCount = 0
    words = []

    with open(file, "r") as wordlist:
      logging.info(f"Aggregating {wordlist.name}...")
      for word in wordlist:
        word = word.strip().replace("\r\n", "").lower()
        if self.wordPattern.search(word):
          words.append(word)
          wordCount += 1

      logging.info(f"{file.name} had {self.fmtNum(wordCount)} words")

    return {"name": file.name, "words": words}


  def populateMaster(self, result):
    logging.info(f"Loading from {result.get('name')}")

    for word in result.get("words"):
      self.masterList.append(word)


  def makeUnique(self):
    count = len(self.masterList)
    self.masterList = list(dict.fromkeys(self.masterList))
    logging.info(f"Removed {self.fmtNum(count - len(self.masterList))} duplicates")


  def count(self):
    return len(self.masterList)


  def aggregate(self):
    self.gatherFiles()

    pool = multiprocessing.Pool(processes = 8)

    print("")
    logging.info("Gathering words from files...")
    results = pool.map(self.getWordsFromFile, (file for file in self.files))

    print("")
    logging.info("Merging the results into the master list...")
    [self.populateMaster(result) for result in results]

    print("")
    logging.info("Removing duplicates")
    self.makeUnique()

    print("")
    logging.info("Sorting master list.")
    self.masterList.sort()

    print("")
    with open(self.pathToMaster, "w") as mlist:
      logging.info("Writing to master.txt")

      for word in self.masterList:
        mlist.write(word + "\n")


if __name__ == "__main__":
  os.system("cls")
  startTime = time()

  aggregator = Aggregator()
  aggregator.aggregate()
  logging.info(f"Completed in {time() - startTime}")
  logging.info(f"Total unique words: {aggregator.fmtNum(aggregator.count())}")