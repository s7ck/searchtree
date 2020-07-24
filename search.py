from imports.linearsearch import LinearSearch
from imports.masterlist import MasterList
from imports.benchmark import Benchmark
from imports.insearch import InSearch
from imports.analyzer import Analyzer
from imports.bsearch import BSearch
from imports.logger import Logger
from pathlib import Path
import multiprocessing
import tabulate
import datetime
import argparse

###############################################################################
# Configuration
###############################################################################
# Arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-w", "--word",
  help = "The word you want to find. Ignored in benchmark mode.")

argparser.add_argument("-m", "--mode",
  help = "Set the search mode: linear or tree",
  type = str.lower,
  default = "linear")

argparser.add_argument("-n", "--num",
  help = "How many test to run for each search mode. Default = 500",
  type = int,
  default = 500)

argparser.add_argument("-s", "--short",
  help = "Use (and, if needed, create) a short version of the master file.",
  action = "store_true",
  default = False)

args = argparser.parse_args()

log = Logger()

# Modes
modes = {
  "in": [InSearch],
  "tree": [BSearch],
  "linear": [LinearSearch],
  "benchmark": [InSearch, BSearch, LinearSearch]
}


###############################################################################
# Program
###############################################################################
def main():
  results = {}
  searchTerms = []
  master = MasterList(usingShort = args.short)
  analyzer = Analyzer()


  if args.mode in modes:
    if args.mode == "benchmark":
      searchTerms = master.benchmarkList(args.num)
    else:
      searchTerms.append(args.word)

    # Loop through the modes and get a new instance of each as they come in.
    for Mode in modes[args.mode]:
      # Add instance of the MasterList to the current Mode
      mode = Mode(master)

      log.write(f"Searching in {mode.name} mode")

      # Setup results for the current mode.
      results[mode.name] = { "tests": [] }

      # Loop through all of our search terms...
      for term in searchTerms:
        #... add the test to our tests list...
        results[mode.name]["tests"].append({
          "term": term,
          "found": False,
          "start": datetime.datetime.now(),
          "end": None
        })

        #... search for the term in the current mode...
        results[mode.name]["tests"][-1]["found"] = mode.find(term)
        if mode.find(term):
          #... if we find it, add the end time to the results.
          results[mode.name]["tests"][-1]["end"] = datetime.datetime.now()
    # end for
    analyzer.analyze(results)
  else:
    log.write(f"'{mode} is not a valid search mode.")


main()