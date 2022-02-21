import math


def get_quaternion_from_euler(roll, pitch, yaw):
    qx = (math.sin(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) -
          math.cos(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2))
    qy = (math.cos(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2) +
          math.sin(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2))
    qz = (math.cos(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2) -
          math.sin(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2))
    qw = (math.cos(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) +
          math.sin(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2))

    return [qx, qy, qz, qw]
