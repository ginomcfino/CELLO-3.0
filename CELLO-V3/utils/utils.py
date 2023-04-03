


def print_centered(text):
    length = 50  # Length of the string of slashes
    print()
    print("/" * length)
    if type(text) == list:
        for t in text:
            print(t.center(length))
    else:
        print(t.center(length))
    print("/" * length)
    print()
