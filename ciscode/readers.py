import numpy as np
from pathlib import Path


class Vertices:
    """Read vertices
    """

    def __init__(self, path: str):
        self.path = path
        with open(path, "r") as f:
            line = next(f)
            toks = line.replace(" ", "").split(",")

            self.N_vertices = int(toks[0])

        arrVer = np.loadtxt(path, delimiter=" ", skiprows=1,
                            max_rows=self.N_vertices)
        self.arrVer = arrVer


class modeVertices:
    """Read vertices
    """

    def __init__(self, path: str):
        self.path = path
        with open(path, "r") as f:
            line = next(f)
            toks = line.replace(" ", "").split(",")

        m0v = np.loadtxt(path, delimiter=",", skiprows=2,
                         max_rows=1568)

        m1v = np.loadtxt(path, delimiter=",", skiprows=1571, max_rows=1568)

        m2v = np.loadtxt(path, delimiter=",", skiprows=3140, max_rows=1568)

        m3v = np.loadtxt(path, delimiter=",", skiprows=4709, max_rows=1568)

        m4v = np.loadtxt(path, delimiter=",", skiprows=6278, max_rows=1568)

        m5v = np.loadtxt(path, delimiter=",", skiprows=7847, max_rows=1568)

        m6v = np.loadtxt(path, delimiter=",", skiprows=9416, max_rows=1568)

        # print("m1v")
        # print(m1v[0])
        # print(m1v[1567])
        # print("----")

        # print("m2v")
        # print(m2v[0])
        # print(m2v[1567])
        # print("----")

        # print("m3v")
        # print(m3v[0])
        # print(m3v[1567])
        # print("----")

        # print("m4v")
        # print(m4v[0])
        # print(m4v[1567])
        # print("----")

        # print("m5v")
        # print(m5v[0])
        # print(m5v[1567])
        # print("----")

        # print("m6v")
        # print(m6v[0])
        # print(m6v[1567])
        # print("----")

        self.m1v = m1v
        self.m2v = m2v
        self.m3v = m3v
        self.m4v = m4v
        self.m5v = m5v
        self.m6v = m6v


class Indices:
    """Read Indices
    """

    def __init__(self, path: str):
        self.path = path
        with open(path, "r") as f:
            line = next(f)
            toks = line.replace(" ", "").split(",")

            self.N_vertices = int(toks[0])

        arrInd = np.loadtxt(path, delimiter=" ", skiprows=self.N_vertices+2, usecols=(0, 1, 2)
                            )
        self.arrInd = arrInd


class RigidBody:
    """Parses the rigid body A and body B LED and tip coordinate in body coordinate: data."""

    def __init__(self, path: str):
        self.path = path
        with open(path, "r") as f:
            line = next(f)
            toks = line.replace(" ", "").split(",")

        arr = np.loadtxt(path, skiprows=1)
        Y = arr[:6]
        self.Y = Y
        tip = arr[-1]
        self.tip = tip


class sampleReading:
    """Parses the sample reading data."""

    def __init__(self, path: str, keys):
        self.path = path
        with open(path, "r") as f:
            line = next(f)
            toks = line.replace(" ", "").split(",")
        arr = np.loadtxt(path, delimiter=",", skiprows=1, dtype=np.float64)
        # NA1 = arr[:6]
        # self.NA1 = NA1
        # NB1 = arr[6:12]
        # self.NB1 = NB1
        # NA1 = []
        # NA1 = arr[:6]
        # NA1.append(12)
        # self.NA1 = NA1
        self.keys = keys
        NA_dict = {}
        NB_dict = {}
        NA_dict[0] = arr[0:6]
        NB_dict[0] = arr[6:12]

        # keys = range(150)
        for i in range(keys):
            k = i + 1
            x_a = k * 10 + k*6
            y_a = k*10 + (k+1)*6
            x_b = y_a
            y_b = x_b+6
            NA_dict[i+1] = arr[x_a:y_a]
            NB_dict[i+1] = arr[x_b:y_b]

        # logging.info(NA_dict[0])
        self.NA_dict = NA_dict
        self.NB_dict = NB_dict
