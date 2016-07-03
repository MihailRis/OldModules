''' the tooogle function '''
''' toogle function get oen argument: boolean or interger object, True to False, 0 to 1, 1 to 0, False to True '''

__autor__ = "MihqailRis"
__version__ = 1.0

def toogle(value):
    toogled = False
    if type(value) == bool:
        toogled = True
        if value:
            return False
        else:
            return True
    if type(value) == int:
        toogled = True
        if value == 1:
            return 0
        elif value == 0:
            return 1
    if not toogled:
        del toogled
        raise TypeError, "not boolean object not toogled"