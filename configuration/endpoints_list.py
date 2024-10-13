from enum import Enum


class EndpointsList(str, Enum):
    shortner = "/shortner"
    redirect = "/redirect/"