from math import dist
import click
import logging
from rich.logging import RichHandler
from rich.progress import track
from pathlib import Path
import numpy as np
from scipy.spatial.distance import cdist

from ciscode import readers, writers, registration, trianglePoints, icp, barycentric, QmodeK


FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger("ciscode")


@click.command()
@click.option("-d", "--data-dir", default="data", help="Where the data is.")
@click.option("-o", "--output_dir", default="outputs", help="Where to store outputs.")
# @click.option("-n", "--name", default="pa3-debug-a", help="Which experiment to run.")
def main(
    data_dir: str = "data", output_dir: str = "outputs", name: str = "-Debug-SampleReadingsTest.txt"
):
    data_dir = Path(data_dir).resolve()
    output_dir = Path(output_dir).resolve()
    if not output_dir.exists():
        output_dir.mkdir()

    ############Input data files###########################
    ##Surface Mesh Data structure##
    Vertices = readers.Vertices(data_dir / f"Problem5MeshFile.sur")
    logging.info(".....Loading Triangle Mesh......... ")

    # Reading vertices from the mode file
    mode1Vertices = readers.modeVertices(data_dir / f"Problem5Modes.txt")
    m1v = mode1Vertices.m1v
    m2v = mode1Vertices.m2v
    m3v = mode1Vertices.m3v
    m4v = mode1Vertices.m4v
    m5v = mode1Vertices.m5v
    m6v = mode1Vertices.m6v

    #########triangle vetices##############################
    vertices = Vertices.arrVer

    ###########triangle Indices##########################
    Indices = readers.Indices(data_dir / f"Problem5MeshFile.sur")
    triInd = Indices.arrInd
    #########calculation of FA,k and FB,k###########################

    # loading rigid body a file
    RigidBodyA = readers.RigidBody(data_dir / f"Problem5-BodyA.txt")
    RigidBodyB = readers.RigidBody(data_dir / f"Problem5-BodyB.txt")

    # LED coordinates with respect to body frame
    rbA = RigidBodyA.Y
    rbB = RigidBodyB.Y
    tipA = RigidBodyA.tip

    logging.info("Rigid Body A details....")
    logging.info(rbA)
    logging.info(tipA)

    logging.info("Rigid Body B details ")
    logging.info(rbB)

    # Reading sample file

    fileLetter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K']
    for q in track(fileLetter):
        if q == 'G' or q == 'H' or q == 'J' or q == 'K':
            input_file = "PA5-"+q
            name = "-Unknown-SampleReadingsTest.txt"
        else:
            input_file = "PA5-"+q

        if q == 'E' or q == 'F' or q == 'H' or q == 'J':
            iteration = 400
        else:
            iteration = 150
        sampleReading = readers.sampleReading(
            data_dir / f"{input_file}{name}", iteration)

        print("\t \t ----------- Input File :",
              f"{input_file}{name}", "-----------")
        # leds from sample file
        frA = sampleReading.NA_dict  # rigid body A
        frB = sampleReading.NB_dict  # rigid body B

        A = []
        dk = []
        for k in range(iteration):
            Fak, Ra, pa = registration.PointCloud(rbA, frA[k])
            Fbk, Rb, pb = registration.PointCloud(rbB, frB[k])
            Ak = np.matmul(Ra, tipA) + pa

            FbInv, RbInv, pbInv = registration.frameInv(Fbk)

            d = np.matmul(RbInv, Ak) + pbInv

            A.append(Ak)
            dk.append(d)
            # logging.info(Fak)

        A = np.array(A)
        dk = np.array(dk)

        # inital guess of Freg = I
        sk = dk  # define sk

        def FindClosestPointMesh(sk):
            """[It calculates the closest point in triangle mesh]

            Args:
                sk ([3x1 vector]): [description]

            Returns:
                [3x1]: [closest point]
            """
            triVert = Vertices.arrVer  # triangle vertices numpy array
            triInd = Indices.arrInd  # triangle indices numpy array

            # logging.info()
            mS = []  # Coorrdinate Tri Vert U
            mT = []  # Coorrdinate Tri Vert T
            mU = []  # Coorrdinate Tri Vert U
            for i in range(3135):
                ks = triInd[i, 0]
                ku = triInd[i, 1]
                kt = triInd[i, 2]

                ks = int(ks)  # indice "s" of Tri vert
                ku = int(ku)  # indice "u" of Tri vert
                kt = int(kt)  # indice "t" of Tri vert

                S = triVert[ks-1]
                U = triVert[ku-1]
                T = triVert[kt-1]

                mS.append(S)
                mU.append(U)
                mT.append(T)

            mS = np.array(mS)  # coordinates of vertex S of Triangle
            mU = np.array(mU)  # coordinates of vertex U of Triangle
            mT = np.array(mT)  # coordinates of vertex T of Triangle

            ck = trianglePoints.closestPoint(mS, mU, mT, sk)

            return ck

        # ck is closest point on the triangle with respect to sk
        ck, q0k = FindClosestPointMesh(sk)

        # ICP
        # calculation Freg
        Freg, _ = icp.icp(sk, ck)
        # recalculate SK
        Rreg = Freg[0:3, 0:3]
        Preg = Freg[0:3, 3]
        new_sk = []
        new_ck = []
        for l in range(len(sk)):
            new_sk.append(np.matmul(dk[l], Rreg) + Preg)
            new_ck.append(np.matmul(dk[l], Rreg) + Preg)
        sk = np.array(new_sk)
        ck = np.array(new_ck)

        QmodeK.modeInput(triInd, m1v, m2v, m3v, m4v, m5v, m6v, sk, q0k)

        dist_new = []
        for i in range(len(sk)):
            dist_i = np.linalg.norm(sk[i] - ck[i])

            dist_new.append(dist_i)

        dist_new = np.array(dist_new)

        out_list = []
        l1 = []

        for i in range(len(sk)):
            temp = [sk[i, 0], sk[i, 1], sk[i, 2],
                    ck[i, 0], ck[i, 1], ck[i, 2], dist_new[i]]
            l1.append(temp)
            out_list = np.array(l1)

        output = writers.PA5(input_file, out_list, iteration)
        output.save(output_dir)


if __name__ == "__main__":
    main()
