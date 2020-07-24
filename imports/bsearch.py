from imports.logger import Logger
from pathlib import Path

log = Logger()

class BSearch:
  def __init__(self, master):
    self.name = "Tree"
    self.masterList = master.masterList

  def find(self, word):
    return word in self.masterList