"""Custom Script"""

import numpy as np


def concat(array_one=np.array([]), array_two=np.array([])):
    """Just a custom function"""
    result = np.concatenate((array_one, array_two), axis=0)
    return result


class Dog:
    """Just a custom class"""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Dog {self.name!r}>"

    def change_name(self, name):
        """"""
        self.name = name


def run(params, logger):
    """Custom Script"""
    myarray_one = np.array(range(10))
    myarray_two = np.array(range(200))
    result = concat(array_one=myarray_one, array_two=myarray_two)
    logger.debug("Result: " + np.array_str(result))
    logger.debug("That operation was so cool!")
    pepe = Dog(name="pepe")
    logger.debug("A custom class instance")
    logger.debug(pepe)
    return result
