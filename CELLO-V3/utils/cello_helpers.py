
def print_centered(text, padding=False):
    length = 88  # Length of the string of slashes
    if padding: print()
    print("/" * length)
    if type(text) == list:
        for t in text:
            print(t.center(length))
    else:
        print(text.center(length))
    print("/" * length)
    if padding: print()
