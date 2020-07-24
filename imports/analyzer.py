from tabulate import tabulate

class Analyzer:
  def __init__(self):
    self.missingList = []
    self.statistics = []
  # end __init__


  def getDuration(self, test):
    try:
      return (test.get("end") - test.get("start")).microseconds
    except:
      return -1
  # end getDuration


  def displayResults(self):
    speed = 0

    headers = ["Algorithm", "Total", "Average"]

    self.statistics.sort(key = lambda x: x[2])

    # This is uglier than it needs to be but it was fun to write so I kept it.
    # This is a map() inside a list comprehension. We map() the lists inside the
    # outer list. If the values aren't strings, we assume they're numeric and we
    # format it with commas: 1234.56 becomes 1,234.56
    table = [
      map(lambda x: "{:,}".format(x) if type(x) != str else x, val)
        for val in self.statistics
    ]

    print(tabulate(
      table,
      headers = headers
    ))
  # end displayResults()

  def analyze(self, results):
    testCount = 0

    # Loop through the available modes...
    for mode, tests in results.items():
      totalTime = 0
      testCount = 0

      self.statistics.append([mode])

      #... then loop through the tests for that mode...
      for stat in tests.get("tests"):
        testCount += 1
        totalTime += self.getDuration(stat)

        if not stat.get("found"):
          self.missingList.append(stat.get("term"))

      self.statistics[-1].append(totalTime)
      self.statistics[-1].append((totalTime / testCount))

    self.displayResults()
  # end analyze()
# end class Analyzer