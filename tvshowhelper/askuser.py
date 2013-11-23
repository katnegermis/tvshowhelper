from tvshowhelper import logger


def yesno(question):
    print("")
    print(question)
    print("n: No")
    print("y: Yes")
    res = raw_input()
    return res.lower().startswith("y")


def multipleoptions(question, options, unwrapfunction=None, noneoption=True):
    print("")
    print(question)
    print("")
    for i, option in enumerate(options):
        if unwrapfunction is not None:
            option = unwrapfunction(option)
        print("{}: {}".format(i + 1, option))
    if noneoption:
        print("0: None of the above")
    # check that user inputs a number
    res = None
    while res is None:
        try:
            res = int(raw_input())
        except ValueError:
            print("Please only type a number")
        if res > len(options):
            res = None
            print("Please choose a number within the range 1-{}".format(len(options)))
    if res == 0:
        return None
    return options[res - 1]
