from abc import ABC, abstractmethod

from dataclasses import dataclass


@dataclass
class BaseOrganizationRepository(ABC):

    @abstractmethod
    async def get_organization_list(self):
        ...