class Package:
    def __init__(self, package_id, city, state, zip, deadline, weight, loading_time, delivery_time):
        self.package_id = package_id
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.loading_time = loading_time
        self.delivery_time = delivery_time

    def __str__(self):
        print(self.package_id)
        print(self.city)
        print(self.state)
        print(self.zip)
        print(self.deadline)
        print(self.weight)
        print(self.loading_time)
        print(self.delivery_time)

    def __repr__(self):
        print(self.package_id)
        print(self.city)
        print(self.state)
        print(self.zip)
        print(self.deadline)
        print(self.weight)
        print(self.loading_time)
        print(self.delivery_time)