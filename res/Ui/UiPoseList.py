# ==============================================
#                   Import
# ==============================================
from UiPose import UiPose
# ==============================================
#                   Import
# ==============================================

class UiPoseList(object):
    """
    This class hold all :class: UiPose
    """

    def __init__(self):
        super(UiPoseList, self).__init__()
        self.all_poses = list()

    def reset(self):
        self.all_poses = list()

    def add_pose(self, pose_id, pose_bmp, pose_name):
        """
        Add a UiPose in the list all_poses.

        Returns True if the pose were created
        """
        self.all_poses.append(UiPose(pose_id, pose_bmp, pose_name))

        return True

    def select_pose(self, pose_id):
        if self.get_number_of_poses() <= pose_id:
            return False

        self.all_poses[pose_id].select()

    def deselect_pose(self, pose_id):
        if self.get_number_of_poses() <= pose_id:
            return False

        self.all_poses[pose_id].deselect()

    def toggle_select_pose(self, pose_id):
        if self.get_number_of_poses() <= pose_id:
            return False

        self.all_poses[pose_id].toggle_select()

    def deselect_all(self):
        for pose in self.iter_poses():
            pose.deselect()

    def get_number_of_poses(self):
        return len(self.all_poses)

    def iter_poses(self):
        """
        iter_poses() -> iterator of UiPose

        Use this function to iterate over all poses
        """

        for pose in self.all_poses:
                yield pose