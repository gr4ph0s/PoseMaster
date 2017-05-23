class UiPose(object):
    """
    This class represents a pose in the GeUserArea.

    .. attribute:: id
        The id of the pose in the DB

    .. attribute:: bmp
        c4d.bitmaps.BaseBitmap of the pose

    .. attribute:: name
        The name of the pose. Can be shrinked in the display function according the size of a miniature

    .. attribute:: selected
        True if the pose is actually selected on the GeUserArea

    """

    __slots__ = ('id', 'bmp', 'name', 'selected')

    def __init__(self, id, bmp, name):
        super(UiPose, self).__init__()
        self.id = id
        self.bmp = bmp
        self.name = name
        self.selected = False

    def __repr__(self):
        return str(self.name)

    def setId(self, id):
        self.id = id

    def setBmp(self, bmp):
        self.bmp = bmp

    def setName(self, name):
        self.name = name

    def select(self):
        self.selected = True

    def toggle_select(self):
        self.selected = not bool(self.selected)

    def deselect(self):
        self.selected = False

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getBmp(self):
        return self.bmp

    def getSelect(self):
        return self.select()