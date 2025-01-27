from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class OrganizationNotFoundException(LogicException):

    id: str

    @property
    def message(self):
        return f'Организация с таким {self.id} не найден.'

@dataclass(eq=False)
class OrganizationWithActivityNotFoundException(LogicException):

    activity_name: str

    @property
    def message(self):
        return f'Деятельности с названием "{self.activity_name}" нет.'


@dataclass(eq=False)
class OrganizationWithNameNotFoundException(LogicException):

    name: str

    @property
    def message(self):
        return f'Организаций с названием "{self.name}" нет.'


@dataclass(eq=False)
class OrganizationWithBuildingNotFoundException(LogicException):

    pk_building: str

    @property
    def message(self):
        return f'Организаций в здании "{self.pk_building}" нет.'
