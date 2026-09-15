class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes, loading_time, delivery_time, available_time, status, corrected_address, corrected_city, corrected_state, corrected_zip):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.loading_time = loading_time
        self.delivery_time = delivery_time
        self.available_time = available_time
        self.status = status
        self.corrected_address = corrected_address
        self.corrected_city = corrected_city
        self.corrected_state = corrected_state
        self.corrected_zip = corrected_zip

    def __str__(self):
        return (f"Package {self.package_id}: "
                f"{self.address}, "
                f"{self.city}, "
                f"{self.state}, "
                f"{self.zip_code}, "
                f"Notes: {self.notes}, "
                f"Loading Time: {self.loading_time}, "
                f"Delivery Time: {self.delivery_time}, "
                f"Available Time: {self.available_time}, "
                f"Delivery Status: {self.status}")

    def __repr__(self):
        return (f"Package({self.package_id}, "
                f"{self.address}, "
                f"{self.city}, "
                f"{self.state}, "
                f"{self.zip_code}, "
                f"Notes: {self.notes}, "
                f"Load: {self.loading_time}, "
                f"Delivered: {self.delivery_time}, "
                f"Available: {self.available_time}, "
                f"Status: {self.status})")
