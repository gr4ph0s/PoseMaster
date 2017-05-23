class PoseData(object):
    def __init__(self):
        self.pose_id = 0  #the linked pose_id => Pose.py
        self.obj_uid = None  #unique id object
        self.obj_name = None  #obj name
        self.position = None  #obj position
        self.scale = None  #obj scale
        self.rotation = None  #obj rotation
        self.user_data = None  #obj user data
