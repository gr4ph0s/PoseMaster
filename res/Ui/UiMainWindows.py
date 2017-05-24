# ==============================================
#                   Import
# ==============================================
import c4d

from .UiPoseList import UiPoseList
from .UiPoseLibraryView import UiPoseLibraryView
from ..Helper.Const import Const
from ..Helper.Text import Text
# ==============================================
#                   Import
# ==============================================

txt = Text()


class UiMainWindows(c4d.gui.GeDialog):
    """
    This dialog contains the :class:`PoseLibraryView` class and displays
    it in its very own window.
    """

    # Symbolic IDs for parameters in the dialog.
    ID_SCORE = 1000
    ID_POSELIBRARY = 1001
    ID_SLIDER = 1002

    def __init__(self):
        super(UiMainWindows, self).__init__()
        self.poses_list = UiPoseList()
        self.view = UiPoseLibraryView(self.poses_list)

    def Command(self, id, data):
        if id == self.ID_SLIDER:
            self.view.set_tile_size(int(100* self.GetFloat(self.ID_SLIDER)))
            self.view.Redraw()

        return True


    def create_menu(self):
        """Function for creating all the Inline menu of the UI"""

    def create_menu(self):
        self.MenuFlushAll()

        if self.MenuSubBegin(txt.get(Const.MENU_RIG)):

            self.MenuAddString(Const.MENU_RIG_NEW, txt.get(Const.MENU_RIG_NEW))
            self.MenuAddString(Const.MENU_RIG_REFRESH, txt.get(Const.MENU_RIG_REFRESH))
            self.MenuAddString(Const.MENU_RIG_RENAME, txt.get(Const.MENU_RIG_RENAME))
            self.MenuAddString(Const.MENU_RIG_DELETE_CURRENT, txt.get(Const.MENU_RIG_DELETE_CURRENT))
            self.MenuAddString(Const.MENU_RIG_DELETE_ALL, txt.get(Const.MENU_RIG_DELETE_ALL))

            if self.MenuSubBegin(txt.get(Const.MENU_RIG_OPTIONS)):
                self.MenuAddString(Const.MENU_RIG_CHANGE_FOLDER, txt.get(Const.MENU_RIG_CHANGE_FOLDER))
                self.MenuSubEnd()


            self.MenuAddSeparator()
            if self.MenuSubBegin(txt.get(Const.MENU_RIG_OPTIONS_IMPORT)):
                self.MenuAddString(Const.MENU_RIG_OPTIONS_IMPORT_ACTIVE, txt.get(Const.MENU_RIG_OPTIONS_IMPORT_ACTIVE))
                self.MenuAddString(Const.MENU_RIG_OPTIONS_IMPORT_ZIP, txt.get(Const.MENU_RIG_OPTIONS_IMPORT_ZIP))
                self.MenuSubEnd()
            if self.MenuSubBegin(txt.get(Const.MENU_RIG_OPTIONS_EXPORT)):
                self.MenuAddString(Const.MENU_RIG_OPTIONS_EXPORT_ACTIVE, txt.get(Const.MENU_RIG_OPTIONS_EXPORT_ACTIVE))
                self.MenuAddString(Const.MENU_RIG_OPTIONS_EXPORT_ZIP, txt.get(Const.MENU_RIG_OPTIONS_EXPORT_ZIP))
                self.MenuSubEnd()

            self.MenuSubEnd()
        self.MenuFinished()

        if self.MenuSubBegin(txt.get(Const.MENU_HELP)):
            self.MenuAddString(Const.MENU_HELP_CHECK_UPDATE, txt.get(Const.MENU_HELP_CHECK_UPDATE))
            self.MenuAddSeparator()
            self.MenuAddString(Const.MENU_HELP_ABOUT, txt.get(Const.MENU_HELP_ABOUT))
            self.MenuSubEnd()
        self.MenuFinished()

        self.GroupEnd()

    def CreateLayout(self):
        self.SetTitle("Pose Master V{}".format(Const.VERSION))

        # Add the field to display the score in the menu line of
        # the dialog.
        self.create_menu()

        # Add and attach the TFE_View to the main dialog area.
        self.AddUserArea(self.ID_POSELIBRARY, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT)
        self.AttachUserArea(self.view, self.ID_POSELIBRARY)
        self.AddSlider(self.ID_SLIDER, c4d.BFH_SCALEFIT | c4d.BFV_BOTTOM, 10)
        self.SetFloat(self.ID_SLIDER, 1, 0.5, 3, 0.001)
        return True