from ..Const import Const as Const


class Fr(object):
    def add_string(self, const_id, string_value):
        """
        Add a string to the current string table
        :param const_id: The string id => Const.Language
        :param string_value: The string => str
        :return: None
        """
        str_const = str(const_id)
        self.data[str_const] = string_value

    def __init__(self):
        self.data = dict()
        self.add_string(Const.TEST_STRING, "Fr")
