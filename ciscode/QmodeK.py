import numpy as np


def modeInput(triInd, m1v, m2v, m3v, m4v, m5v, m6v, sk, q0k):
    # Coorrdinate Tri Vert U for 6 modes
    m1S = []
    m2S = []
    m3S = []
    m4S = []
    m5S = []
    m6S = []
    # Coorrdinate Tri Vert T for 6 modes
    m1T = []
    m2T = []
    m3T = []
    m4T = []
    m5T = []
    m6T = []

    # Coorrdinate Tri Vert U for 6 moes
    m1U = []
    m2U = []
    m3U = []
    m4U = []
    m5U = []
    m6U = []

    for i in range(3135):
        ks = triInd[i, 0]
        ku = triInd[i, 1]
        kt = triInd[i, 2]

        ks = int(ks)  # indice "s" of Tri vert
        ku = int(ku)  # indice "u" of Tri vert
        kt = int(kt)  # indice "t" of Tri vert

        S1 = m1v[ks-1]
        U1 = m1v[ku-1]
        T1 = m1v[kt-1]

        S2 = m2v[ks-1]
        U2 = m2v[ku-1]
        T2 = m2v[kt-1]

        S3 = m3v[ks-1]
        U3 = m3v[ku-1]
        T3 = m3v[kt-1]

        S4 = m4v[ks-1]
        U4 = m4v[ku-1]
        T4 = m4v[kt-1]

        S5 = m5v[ks-1]
        U5 = m5v[ku-1]
        T5 = m5v[kt-1]

        S6 = m6v[ks-1]
        U6 = m6v[ku-1]
        T6 = m6v[kt-1]

        m1S.append(S1)
        m1U.append(U1)
        m1T.append(T1)

        m2S.append(S2)
        m2U.append(U2)
        m2T.append(T2)

        m3S.append(S3)
        m3U.append(U3)
        m3T.append(T3)

        m4S.append(S4)
        m4U.append(U4)
        m4T.append(T4)

        m5S.append(S5)
        m5U.append(U5)
        m5T.append(T5)

        m6S.append(S6)
        m6U.append(U6)
        m6T.append(T6)

    # Mode 1 Tri cord.
    m1S = np.array(m1S)  # vertex S
    m1U = np.array(m1U)  # vertex U
    m1T = np.array(m1T)  # vertex T

    # Mode 2 Tri cord.
    m2S = np.array(m2S)  # vertex S
    m2U = np.array(m2U)  # vertex U
    m2T = np.array(m2T)  # vertex T

    # Mode 3 Tri cord.
    m3S = np.array(m3S)  # vertex S
    m3U = np.array(m3U)  # vertex U
    m3T = np.array(m3T)  # vertex T

    # Mode 4 Tri cord.
    m4S = np.array(m4S)  # vertex S
    m4U = np.array(m4U)  # vertex U
    m4T = np.array(m4T)  # vertex T

    # Mode 5 Tri cord.
    m5S = np.array(m5S)  # vertex S
    m5U = np.array(m5U)  # vertex U
    m5T = np.array(m5T)  # vertex T

    # Mode 6 Tri cord.
    m6S = np.array(m6S)  # vertex S
    m6U = np.array(m6U)  # vertex U
    m6T = np.array(m6T)  # vertex T

    # least square problem
    a = sk - q0k
    b = q0k + 1


# return q1k, q2k, q3k, q4k, q5k, q6k
