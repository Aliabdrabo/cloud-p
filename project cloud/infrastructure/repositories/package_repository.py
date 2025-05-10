from domain.entities.package import Package
from application.interfaces.package_repository_interface import PackageRepositoryInterface

class InMemoryPackageRepository(PackageRepositoryInterface):
    def __init__(self):
        self.packages = {}

    def save(self, package: Package):
        self.packages[package.package_id] = package

    def get_by_id(self, package_id: str):
        return self.packages.get(package_id)