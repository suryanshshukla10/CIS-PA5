import numpy as np


def barycentric_coordinates(point, a, b, c):
    """It calcualtes the barycentric coordinates using the least square method        
    point = l1*a + l2*b + l3*c

    Args:
        point ([np array]): [point on the triangle]
        a ([np array 2D or 3D]): [triangle vertiex 1]
        b ([np array 2D or 3D]): [triangle vertiex 2]
        c ([np array 2D or 3D]): [triangle vertiex 3]

    Returns: (l1,l2,l3)
        returns the barycentric coordinate of the triangle 
    """
    T = np.hstack(((a - c)[:, None], (b - c)[:, None]))
    z = np.linalg.lstsq(T, point - c, rcond=1)[0]
    l1 = z[0]
    l2 = z[1]
    l3 = 1 - (l1 + l2)
    return l1, l2, l3


#####Additioanl Barycentric Coordinate calcualtion ####

# def barycentric_coordinates2(point, a, b, c):
#     v0 = b-a
#     v1 = c-a
#     v2 = point-a

#     d00 = np.dot(v0, v0)
#     d01 = np.dot(v0, v1)
#     d11 = np.dot(v1, v1)
#     d20 = np.dot(v2, v0)
#     d21 = np.dot(v2, v1)

#     denom = d00*d11 - d01*d01
#     v = (d11 * d20 - d01 * d21) / denom
#     w = (d00 * d21 - d01 * d20) / denom
#     u = 1 - (v + w)

#     print(u, v, w)
#     print(u*(a) + v * (b) + w*(c))
