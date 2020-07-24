from imports.logger import Logger
from pathlib import Path

log = Logger()

class LinearSearch:
  def __init__(self, master):
    self.name = "Linear"
    self.masterList = master.masterList

  def find(self, word):
    for w in self.masterList:
      if w == word:
        return True
    return False