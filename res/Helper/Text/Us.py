from ..Const import Const as Const


class Us(object):
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

        self.add_string(Const.MENU_RIG,                 u"Rig")
        self.add_string(Const.MENU_RIG_NEW,             u"New")
        self.add_string(Const.MENU_RIG_REFRESH,         u"Refresh all rigs")
        self.add_string(Const.MENU_RIG_RENAME,          u"Rename current rig")
        self.add_string(Const.MENU_RIG_DELETE_CURRENT,  u"Delete current rig")
        self.add_string(Const.MENU_RIG_DELETE_ALL,      u"Delete all rigs")
        self.add_string(Const.MENU_RIG_CHANGE_FOLDER,   u"Change folder location")

        self.add_string(Const.MENU_RIG_OPTIONS,                 u"Options")
        self.add_string(Const.MENU_RIG_OPTIONS_IMPORT,          u"Import")
        self.add_string(Const.MENU_RIG_OPTIONS_IMPORT_ACTIVE,   u"Import rig")
        self.add_string(Const.MENU_RIG_OPTIONS_IMPORT_ZIP,      u"Import multiple rigs")

        self.add_string(Const.MENU_RIG_OPTIONS_EXPORT,          u"Export")
        self.add_string(Const.MENU_RIG_OPTIONS_EXPORT_ACTIVE,   u"Export rig")
        self.add_string(Const.MENU_RIG_OPTIONS_EXPORT_ZIP,      u"Export multiple rigs")
