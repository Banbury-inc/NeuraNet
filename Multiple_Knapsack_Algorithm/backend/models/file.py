class File:
    def __init__(self, id, name, size, file_type, priority, frequency_visited, location, cid):
        self.id = id
        self.name = name
        self.size = size
        self.file_type = file_type
        self.priority = priority
        self.frequency_visited = frequency_visited
        self.location = location
        self.cid = cid

    def __repr__(self):
        return f"File(id={self.id}, name='{self.name}', size={self.size})"
