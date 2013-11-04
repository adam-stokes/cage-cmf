import logging
import traceback

def handleError(self, record):
    traceback.print_stack()

logging.Handler.handleError = handleError

logger = logging.getLogger("CAGE")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s :: %(message)s",
                              datefmt='%m.%d.%Y %I:%M:%S %p')
ch.setFormatter(formatter)
logger.addHandler(ch)
