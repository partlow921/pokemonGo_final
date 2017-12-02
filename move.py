class Move(object):

    """
    Attribute List
    name  : (string) name of the move
    power : (float) pokemon's power
    """

    def __init__(self, name="Default Attack", power=1.0, type="Normal"):
        """Return the name for a specific move and its corresponding power"""
        self.name   = name
        self.power  = power
        self.type   = type

    def __str__(self):
        """defines string value for move object when print function used"""
        return str(self.name)
