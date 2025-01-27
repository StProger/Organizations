from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class OrganizationNotFoundException(LogicException):

    id: str

    @property
    def message(self):
        return f'Организация с таким {self.id} не найден.'