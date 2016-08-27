''' the tooogle function '''
''' toogle function get one argument: boolean or interger object, True to False, 0 to 1, 1 to 0, False to True '''

__author__ = "MihqailRis"
__version__ = 1.0

def toogle(value):
    if type(value) is bool or type(value) is int:
        return int(not value)
    else:
        raise TypeError("Can't toggle {0} object".format(value))
