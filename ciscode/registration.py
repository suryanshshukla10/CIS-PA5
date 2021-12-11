import numpy as np


def PointCloud(A, B):
    '''
    Calculates the least-squares best-fit transform between corresponding 3D points A->B
    Input:
      A: Nx3 numpy array of corresponding 3D points
      B: Nx3 numpy array of corresponding 3D points
    Returns:
      T: 4x4 homogeneous transformation matrix
      R: 3x3 rotation matrix
      t: 3x1 column vector
    '''

    assert len(A) == len(B)

    # translate points to their centroids
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    AA = A - centroid_A
    BB = B - centroid_B

    # rotation matrix
    H = np.dot(AA.T, BB)
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = np.dot(Vt.T, U.T)

    # translation
    t = centroid_B.T - np.dot(R, centroid_A.T)

    # homogeneous transformation
    T = np.identity(4)
    T[0:3, 0:3] = R
    T[0:3, 3] = t

    return T, R, t


def frameInv(T):
    # output -
    """[summary]

    Args:
        T ([T, numpy array 4x4, ]): [homogeneous frame transformation]

    Returns:
        Tinv, inverse of the frame
        Rinv, rotation matrix
        pinv - translation vector 
    """
    T = np.array(T)

    R = T[0:3, 0:3]
    P = T[0:3, 3]

    # Rinv = np.transpose(R)
    Rinv = np.linalg.inv(R)
    Pinv = -np.matmul(Rinv, P)

    Tinv = np.identity(4)
    Tinv[0:3, 0:3] = Rinv
    Tinv[0:3, 3] = Pinv

    return Tinv, Rinv, Pinv
