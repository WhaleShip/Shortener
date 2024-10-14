from enum import Enum


class EndpointsList(str, Enum):
    shortner = "/shortner"
    redirect = "/redirect"

    def __str__(self):
        return str(self.value)
