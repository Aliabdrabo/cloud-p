from abc import ABC, abstractmethod
from domain.entities.package import Package

class PackageRepositoryInterface(ABC):
    @abstractmethod
    def save(self, package: Package):
        pass

    @abstractmethod
    def get_by_id(self, package_id: str):
        pass
