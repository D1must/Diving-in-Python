class Value:
    def __get__(self, obj, obj_type):
        return self.gaf

    def __set__(self, obj, gaf):
        self.gaf = gaf * (1 - obj.commission)


# class Account:
#     amount = Value()
#
#     def __init__(self, commission):
#         self.commission = commission
