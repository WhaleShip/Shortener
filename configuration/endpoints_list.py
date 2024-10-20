from enum import Enum


class EndpointsList(str, Enum):
    shortner = "/shortner"
    redirect = "/redirect"
    registration = "/register"
    login = "/token"
    users_links = "/links"


    def __str__(self):
        return str(self.value)
