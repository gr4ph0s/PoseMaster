# ==============================================
#                   Import
# ==============================================
import collections
import c4d

from ..Helper.Const import Const
# ==============================================
#                   Import
# ==============================================

#Helper tuple for storing GeUserAre coord
Coord = collections.namedtuple('Coord', 'x y')

class UiPoseLibraryView(c4d.gui.GeUserArea):
    """
    This class implements the visual representation of PoseList
    """

    def __init__(self, ui_pose_list, tile_size=Const.UI_MINIATURE_SIZE, tile_space=8, ):
        super(UiPoseLibraryView, self).__init__()
        self.pose_list = ui_pose_list
        self.set_tile_size(tile_size)
        self.tile_space = tile_space

        # only used for speed performance in draw_pose
        self.total_tile_width = 0
        self.max_x_row = 0

    def set_tile_size(self, tile_size):
        self.tile_width = tile_size
        self.tile_height = tile_size * 1.25

    def get_color_vector(self, color_id):
        """
        get_color_vector(color_id) -> c4d.Vector

        Returns a color :class:`c4d.Vector` for *color_id*. The
        existing :meth:`GetColorRGB` method returns a dictionary
        with RGB values in range [0,255] which is rather inconvenient.
        """

        data = self.GetColorRGB(color_id)
        rgbv = c4d.Vector(data['r'], data['g'], data['b'])
        return rgbv ^ c4d.Vector(1.0 / 255.0)

    def calc_pose_pos(self, index):
        """
        Helper function to compute the pixel offset of a miniature.

        :param index: integer representing the order of the miniature
        :return: Coord obj egual to the left top corner of a miniature
        """
        if not self.max_x_row:
            return Coord(0, 0)

        x_row = index % self.max_x_row
        y_row = index // self.max_x_row

        x = (self.tile_space // 2) + ((x_row * self.tile_width) + (x_row * self.tile_space))
        y = (self.tile_space // 2) + ((y_row * self.tile_height) + (y_row * self.tile_space))

        return Coord(x, y)

    def draw_pose(self, pose_id, pose_name, pose_bmp, pose_selected):
        """
        Helper function to draw a pose.

        :param pose_id: integer
            the pose_id in the grid ! 
            Not equivalent to UiPose.id wich is the db one 

        :param pose_name: string
            The actual pose name

        :param pose_bmp: c4d.bitmaps.BaseBitmap
            The bitmap to be used.

        :param pose_selected: Bool
            The state of the selection of the pose

        """

        # Calculate the tile's position on the User Area for both
        # components and convert it to a Coord object immediately.
        pos = self.calc_pose_pos(pose_id)
        size = Coord(self.tile_width, self.tile_height)

        # Draw the top rectangle // Will be BaseBitmpap after
        color = self.get_color_vector(c4d.COLOR_BGFOCUS)
        self.DrawSetPen(color)
        self.DrawRectangle(pos.x, pos.y, pos.x + size.x, pos.y + size.y * 0.75)

        # write pose id
        flags = c4d.DRAWTEXT_HALIGN_CENTER | c4d.DRAWTEXT_VALIGN_CENTER
        self.DrawSetTextCol(c4d.COLOR_TEXT, c4d.COLOR_TRANS)
        self.DrawText(
            str(pose_id), pos.x + size.x / 2, pos.y + (size.y * 0.75) / 2, flags)

        # Draw the bottom rectangle
        color = self.get_color_vector(c4d.COLOR_BGEDIT)
        self.DrawSetPen(color)
        self.DrawRectangle(pos.x, pos.y + size.y * 0.75, pos.x + size.x, pos.y + size.y)

        # Draw the name of the pose
        if pose_selected:
            self.DrawSetTextCol(c4d.COLOR_TEXTFOCUS, c4d.COLOR_TRANS)
        else:
            self.DrawSetTextCol(c4d.COLOR_TEXT, c4d.COLOR_TRANS)

        # reduce the string for matching our block
        while pose_name:
            if self.DrawGetTextWidth(pose_name) > self.tile_width:
                pose_name = pose_name[:-1]
            else:
                break

        self.DrawText(
            str(pose_name), pos.x + size.x / 2, pos.y + size.y * 0.875, flags)

        # Draw outline if selected
        if pose_selected:
            self.DrawBorder(c4d.BORDER_ACTIVE_4, pos.x, pos.y, pos.x + size.x, pos.y + size.y)

    def DrawMsg(self, x1, y1, x2, y2, msg):
        """
        This method is called to render the content of the view.
        """

        # Enables double buffering to avoid flickering.
        self.OffScreenOn()

        # Draw the background.
        self.DrawSetPen(c4d.COLOR_BG)
        self.DrawRectangle(x1, y1, x2, y2)

        # Set the text font, we only need to do this once.
        self.DrawSetFont(c4d.FONT_BOLD)

        # set data for drawing
        self.total_tile_width = self.tile_width + self.tile_space
        self.max_x_row = self.GetWidth() // self.total_tile_width

        # Draw all the poses.
        for tile in self.pose_list.iter_poses():
            self.draw_pose(tile.id, tile.name, tile.bmp, tile.selected)

    def calc_pose_id_by_coord(self, coord):
        """
        Retrieve the actual UiPose id from a coord in UiPoseList.all_poses

        :param coord: the coord in the GeUserArea
        :return: int. Calc_pos_id can retrieve a pose_id which is not into the list ALWAYS CHECK!
        """
        x_row = coord.x // self.total_tile_width
        y_row = coord.y // self.tile_height

        return int(x_row + y_row * self.max_x_row)

    def get_ctrl_shift_alt(self, msg):
        """
        Get if ctrl / shift or alt is pressed
        """
        bc_keyboard = c4d.BaseContainer()
        ctrl = False
        shift = False
        alt = False

        self.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc_keyboard)

        if bc_keyboard[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            ctrl = True

        if bc_keyboard[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            shift = True

        if bc_keyboard[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
            alt = True

        return ctrl, shift, alt

    def get_coord_clicked(self, msg):
        """
        Get where user click in our GeUserArea
        """
        bc_click = c4d.BaseContainer()
        self.GetInputState(c4d.BFM_INPUT_MOUSE, c4d.BFM_INPUT_MOUSELEFT, bc_click)

        # Get position clicked
        base = self.Local2Global()
        coord = Coord(bc_click.GetLong(c4d.BFM_INPUT_X) - base['x'],
                      bc_click.GetLong(c4d.BFM_INPUT_Y) - base['y'])

        return coord

    def Message(self, msg, result):
        if msg.GetId() == c4d.BFM_INPUT:
            # Get state of ctrl / shift / alt
            ctrl, shift, alt = self.get_ctrl_shift_alt(msg)

            # Get position clicked and convert it into pose_id
            pose_id_click = self.calc_pose_id_by_coord(self.get_coord_clicked(msg))

            # Click into a pose
            if self.pose_list.get_number_of_poses() - 1 >= pose_id_click:
                # if only shift is pressed
                if shift and not ctrl and not alt:
                    self.pose_list.toggle_select_pose(pose_id_click)

                # if only ctrl is pressed
                elif ctrl and not shift and not alt:
                    self.pose_list.deselect_pose(pose_id_click)

                # click normal
                else:
                    self.pose_list.deselect_all()
                    self.pose_list.select_pose(pose_id_click)

                # redraw change
                self.Redraw()

            # Click elsewhere on the GeUserArea
            else:
                self.pose_list.deselect_all()
                self.pose_list.select_pose(pose_id_click)
                self.Redraw()

        return super(UiPoseLibraryView, self).Message(msg, result)