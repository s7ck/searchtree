from imports.logger import Logger
from pathlib import Path

log = Logger()

class InSearch:
  def __init__(self, master):
    self.name = "In"
    self.masterList = master.masterList

  def find(self, word):
    return word in self.masterList