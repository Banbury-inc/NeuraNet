class Device:
    def __init__(self, id, name, storage_capacity, online_time, power_consumption):
        self.id = id
        self.name = name
        self.storage_capacity = storage_capacity
        self.online_time = online_time
        self.power_consumption = power_consumption
        self.files = []

    def add_file(self, file):
        self.files.append(file)

    def __repr__(self):
        return f"Device(id={self.id}, name='{self.name}', storage_capacity={self.storage_capacity})"
