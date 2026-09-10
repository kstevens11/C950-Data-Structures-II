class HashTable:
    def __init__(self):
        self.table = [[] for _ in range(10])

    def put(self, package):
        package_hash = package.package_id % 10
        self.table[package_hash].append(package)

    def lookup(self, package_id):
        package_hash = package_id % 10

        for package in self.table[package_hash]:
            if package.package_id == package_id:
                return package
        return None

    def __str__(self):
        return str(self.table)
