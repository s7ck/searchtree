import logging

class Logger:
  def __init__(self):
    logging.basicConfig(
      format = "%(asctime)s: %(message)s",
      level = logging.INFO,
      datefmt = "%H:%M:%S"
    )

  def write(self, message):
    logging.info(message)