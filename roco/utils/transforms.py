from roco.utils import mymath as np


def mirror_x():
  return np.diag([-1, 1, 1, 1])

def mirror_y():
  return np.diag([1, -1, 1, 1])

def scale(scale):
  return np.diag([scale, scale, scale, 1])

def rotate_x(angle):
  r = np.array([[1, 0, 0, 0],
                [0, np.cos(angle), -np.sin(angle), 0],
                [0, np.sin(angle),  np.cos(angle), 0],
                [0, 0, 0, 1]])
  return r
roll = rotate_x

def rotate_y(angle):
  r = np.array([[np.cos(angle), 0, np.sin(angle), 0],
                [0, 1, 0, 0],
                [-np.sin(angle), 0,  np.cos(angle), 0],
                [0, 0, 0, 1]])
  return r
oitch = rotate_y

def rotate_z(angle):
  r = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                [np.sin(angle),  np.cos(angle), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
  return r
yaw = rotate_z

def normalize_quat(quat):
  w,x,y,z = quat
  mag = (w**2+x**2+y**2+z**2)**(0.5)
  return (w/mag,x/mag,y/mag,z/mag)

def multiply_quat(quaternion1, quaternion0):
  w0, x0, y0, z0 = quaternion0
  w1, x1, y1, z1 = quaternion1
  return np.array([-x1*x0 - y1*y0 - z1*z0 + w1*w0,
                       x1*w0 + y1*z0 - z1*y0 + w1*x0,
                      -x1*z0 + y1*w0 + z1*x0 + w1*y0,
                       x1*y0 - y1*x0 + z1*w0 + w1*z0])

def inverse_quat(quat):
  w,x,y,z = quat
#  mag = (w**2+x**2+y**2+z**2)**(0.5)
  mag = 1
  return (w/mag,-x/mag,-y/mag,-z/mag)

def quat_2_DCM(quat):
  (a, b, c, d) = quat
  r = np.array([[a**2 + b**2 - c**2 - d**2, 2*b*c - 2*a*d, 2*b*d + 2*a*c, 0],
                [2*b*c + 2*a*d, a**2 - b**2 + c**2 - d**2, 2*c*d - 2*a*b, 0],
                [2*b*d - 2*a*c, 2*c*d + 2*a*b, a**2 - b**2 - c**2 + d**2, 0],
                [0, 0, 0, 1]])
  return r

def move_to_origin(pt):
  return translate([-pt[0], -pt[1], 0])

def rotate_onto_x(pt, pt2=(0,0)):
  dx = pt[0] - pt2[0]
  dy = pt[1] - pt2[1]
  l = np.sqrt(dx * dx + dy * dy)
  dx = dx / l
  dy = dy / l
  r = np.array([[ dx,  dy, 0, 0],
                [-dy,  dx, 0, 0],
                [  0,   0, 1, 0],
                [  0,   0, 0, 1]])
  return r

def rotate_x_to(pt, pt2=(0,0)):
  dx = pt[0] - pt2[0]
  dy = pt[1] - pt2[1]
  l = np.sqrt(dx * dx + dy * dy)
  dx = dx / l
  dy = dy / l
  r = np.array([[ dx, -dy, 0, 0],
                [ dy,  dx, 0, 0],
                [  0,   0, 1, 0],
                [  0,   0, 0, 1]])
  return r

def reflect_across_2D(edge):
    return reflect_across_2D_pts(edge.pts_2D)

def reflect_across_2D_pts(edgepts):
    x1 = edgepts[0][0]
    y1 = edgepts[0][1]
    x2 = edgepts[1][0]
    y2 = edgepts[1][1]

    dx = (x1-x2)
    if dx == 0: #Edge is a vertical line
        shift = np.array([[ 1, 0, 0, -x1],
                          [ 0, 1, 0,   0],
                          [ 0, 0, 1,   0],
                          [ 0, 0, 0,   1]])
        shift2 = np.array([[1, 0, 0, x1],
                           [0, 1, 0,  0],
                           [0, 0, 1,  0],
                           [0, 0, 0,  1]])
        reflect = np.array([[-1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])
        r = np.dot(shift2,np.dot(reflect,shift))

        return r

    m = (y1-y2)/dx
    n = 1 + m * m
    b = y1-(m*x1)
    a = m * -1
    d = 1 + (m*m)

    #Product of two opposite shifts of b in the y direction and a reflection across y = mx
    shift = np.array([[1, 0, 0,  0],
                      [0, 1, 0, -b],
                      [0, 0, 1,  0],
                      [0, 0, 0,  1]])
    shift2 = np.array([[1, 0, 0, 0],
                       [0, 1, 0, b],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
    reflec = np.array([[1-2*(a*a)/n, -2*a/n, 0,    0],
                       [     -2*a/n,   1-2/n, 0,    0],
                       [        0,    0, 1,    0],
                       [        0,    0, 0,    1]])
    return np.dot(shift2,np.dot(reflec,shift))

def move_origin_to(pt):
  return Translate([pt[0], pt[1], 0])

def translate(origin):
  r = np.array([[1, 0, 0, origin[0]],
                [0, 1, 0, origin[1]],
                [0, 0, 1, origin[2]],
                [0, 0, 0, 1]])
  return r

def get_6DOF(dcm):
  sixdof = {}
  sixdof["dx"] = dcm[0,3]
  sixdof["dy"] = dcm[1,3]
  sixdof["dz"] = dcm[2,3]
  for row in range(3):
    for col in range(3):
      sixdof["dcm%d%d" % (row, col)] = dcm[row,col]
  return sixdof

def DCM_2_quat(dcm):
  den = np.array([ 1.0 + dcm[0,0] + dcm[1,1] + dcm[2,2],
                   1.0 + dcm[0,0] - dcm[1,1] - dcm[2,2],
                   1.0 - dcm[0,0] + dcm[1,1] - dcm[2,2],
                   1.0 - dcm[0,0] - dcm[1,1] + dcm[2,2] ])
  #max_index = [x[0] for x in enumerate(list(den)) if x[1] == max(den)][0]
  max_index = 0 # XXX Can't find symbolically?

  q = [0]*4
  q[max_index] = 0.5 * np.sqrt(den[max_index])
  denom = 4.0 * q[max_index]

  if (max_index == 0):
     q[1] = -(dcm[1,2] - dcm[2,1]) / denom
     q[2] = -(dcm[2,0] - dcm[0,2]) / denom
     q[3] = -(dcm[0,1] - dcm[1,0]) / denom
  if (max_index == 1):
     q[0] = -(dcm[1,2] - dcm[2,1]) / denom
     q[2] =  (dcm[0,1] + dcm[1,0]) / denom
     q[3] =  (dcm[0,2] + dcm[2,0]) / denom
  if (max_index == 2):
     q[0] = -(dcm[2,0] - dcm[0,2]) / denom
     q[1] =  (dcm[0,1] + dcm[1,0]) / denom
     q[3] =  (dcm[1,2] + dcm[2,1]) / denom
  if (max_index == 3):
     q[0] = -(dcm[0,1] - dcm[1,0]) / denom
     q[1] =  (dcm[0,2] + dcm[2,0]) / denom
     q[2] =  (dcm[1,2] + dcm[2,1]) / denom

  return q
