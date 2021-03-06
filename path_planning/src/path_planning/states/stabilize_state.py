import numpy as np
from path_planning.states.base_state import BaseState
from aquadrone_math_utils.angle_math import abs_angle_difference


class StabilizeState(BaseState):
    """
    This state does not interact with the depth control system. It sends a single command to the orientation stability
    system during initialization (which will remain active after finalization as well).
    """

    def __init__(self, roll=0, pitch=0, yaw=0, tolerance_degrees=5, velocity_tolerance_degrees=2):
        self.r = roll
        self.p = pitch
        self.y = yaw
        self.tolerance = np.radians(tolerance_degrees)
        self.velocity_tolerance = np.radians(velocity_tolerance_degrees)
        self.completed = False

    def __repr__(self):
        return self.state_name()

    def state_name(self):
        return "stabilize_state"

    def initialize(self, t, controls, sub_state, world_state, sensors):
        self.completed = False
        controls.set_orientation_goal(roll=self.r, pitch=self.p, yaw=self.y)
        print(self.state_name(), 'starting to stabilize to (r, p, y)=(', self.r, ',', self.p, ',', self.y, ')')

    def process(self, t, controls, sub_state, world_state, sensors):
        state = sub_state.get_submarine_state()
        if abs_angle_difference(self.r, state.orientation_rpy.x) < self.tolerance and \
                abs_angle_difference(self.p, state.orientation_rpy.y) < self.tolerance and \
                abs_angle_difference(self.y, state.orientation_rpy.z) < self.tolerance and \
                state.angular_velocity.magnitude() < self.velocity_tolerance:
            self.completed = True
            print(self.state_name(), 'stabilized!')

    def has_completed(self):
        return self.completed
