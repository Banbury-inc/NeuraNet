
class Lookup:
    def __init__(self):
        pass
    def reverse_lookup(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
        return None

    def reverse_lookup_list(self, dictionary, value):
        for key, sockets in dictionary.items():
            if value in sockets:
                return key
        return None

