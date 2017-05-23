class PoseList(object):
    def __init__(self):
        self.last_used_pose_id = None
        self.last_inserted_pose_id = None
        self.all_poses = list()
