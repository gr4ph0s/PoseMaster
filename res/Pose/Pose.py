class Pose(object):
    """
    Class for routing to PoseData or AnimationData
    It's also link a Pose beetween Group / picture.
    """
    def __init__(self):
        self.pose_id = 0  #Unique pose_id, used for sorting, used in DB
        self.pose_name = "Pose"  #Pose name
        self.group_id = 0  #Group_id, used for linking a pose to a group => ../Group/Group.py
        self.picture_id = 0  #Picture_id, used for linking a bmp => ../Util/Bitmap.py
        self.is_animation = False  #Used to determine if we read PoseData or AnimationData
        self.start_animation = 0  #Only set when is is_animation is True
        self.end_animation = 0  #Only set when is is_animation is True
