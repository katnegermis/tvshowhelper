from utils import logger


def yesno(question):
    logger.info("")
    logger.info(question)
    logger.info("n: No")
    logger.info("y: Yes")
    res = raw_input()
    if not res.lower().startswith("y"):
        return False
    return True


def multipleoptions(question, options, unwrapfunction=None, noneoption=True):
    logger.info("")
    logger.info(question)
    logger.info("")
    for i, option in enumerate(options):
        if unwrapfunction is not None:
            option = unwrapfunction(option)
        logger.info("{}: {}".format(i + 1, option))
    if noneoption:
        logger.info("0: None of the above")
    # check that user inputs a number
    res = None
    while res is None:
        try:
            res = int(raw_input())
        except ValueError:
            logger.warning("Please only type a number")
        if res > len(options):
            res = None
            logger.warning("Please choose a number within the range 1-{}".format(len(options)))
    if res == 0:
        return None
    return options[res - 1]
