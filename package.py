class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, loading_time, delivery_time, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.loading_time = loading_time
        self.delivery_time = delivery_time
        self.status = status

    def __str__(self):
        return f"Package {self.package_id}: {self.address}, {self.city}, {self.state}, {self.zip_code}, Loading Time: {self.loading_time}, Delivery Time: {self.delivery_time}, Delivery Status: {self.status}"


    def __repr__(self):
        return f"Package({self.package_id}, {self.address}, {self.city}, {self.state}, {self.zip_code}, Load: {self.loading_time}, Delivered: {self.delivery_time}, Status: {self.status})"