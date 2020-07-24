from imports.logger import Logger
from pathlib import Path
import random
import sys

log = Logger()

class MasterList:
  def __init__(self, usingShort = False):
    self.wordlistPath = Path("wordlists/")
    self.masterList = []
    self.master = None

    if not usingShort:
      self.masterPath = Path(self.wordlistPath, "master.txt")
    else:
      self.masterPath = Path(self.wordlistPath, "master_short.txt")

    if self.masterPath.exists():
      self.openMaster()
    else:
      log.write(f"{self.masterPath} doesn't exist.")
      log.write(f"Run {'shorten.py' if usingShort else 'aggregate.py'} first.")
      sys.exit(0)
  # end __init__


  def getWordCount(self):
    return len(self.masterList)
  # end getWordCount


  def openMaster(self):
    self.master = open(self.masterPath, "r")
    [self.masterList.append(word.replace("\n", "")) for word in self.master.readlines()]
  # end openMaster()


  def benchmarkList(self, count):
    # get a number of random words from the list and return the array
    # using sample() keeps us from getting the same one twice
    return random.sample(self.masterList, k = count)