import copy

import numpy as np

from liegroups import SO2


def test_identity():
    C = SO2.identity()
    assert isinstance(C, SO2)


def test_mul():
    C = np.array([[0, -1],
                  [1, 0]])
    C2 = C.dot(C)
    assert np.allclose((SO2(C) * SO2(C)).mat, C2)


def test_wedge():
    phi = 1
    Phi = SO2.wedge(phi)
    phis = [1, 2]
    Phis = SO2.wedge(phis)
    assert np.array_equal(Phi, -Phi.T)
    assert np.array_equal(Phis[0, :, :], SO2.wedge(phis[0]))
    assert np.array_equal(Phis[1, :, :], SO2.wedge(phis[1]))


def test_wedge_vee():
    phi = 1
    Phi = SO2.wedge(phi)
    phis = [1, 2]
    Phis = SO2.wedge(phis)
    assert phi == SO2.vee(Phi)
    assert np.array_equal(phis, SO2.vee(Phis))


def test_exp_log():
    C = SO2.exp(np.pi / 4)
    assert np.allclose(SO2.exp(SO2.log(C)).mat, C.mat)


def test_exp_log_zeros():
    C = SO2.exp(0)
    assert np.allclose(SO2.exp(SO2.log(C)).mat, C.mat)


def test_perturb():
    C = SO2.exp(np.pi / 4)
    C_copy = copy.deepcopy(C)
    phi = 0.1
    C.perturb(phi)
    assert np.allclose(C.as_matrix(), (SO2.exp(phi) * C_copy).as_matrix())


def test_normalize():
    C = SO2.exp(np.pi / 4)
    C.mat += 0.1
    C.normalize()
    assert SO2.is_valid_matrix(C.mat)


def test_inv():
    C = SO2.exp(np.pi / 4)
    assert np.allclose((C * C.inv()).mat, np.identity(2))


def test_adjoint():
    C = SO2.exp(np.pi / 4)
    assert C.adjoint() == 1.


def test_transform_multiple():
    C = SO2.exp(np.pi / 4)
    pt1 = np.array([1, 2])
    pt2 = np.array([4, 5])
    pts = np.array([pt1, pt2]).T  # 2x2
    Cpt1 = C * pt1
    Cpt2 = C * pt2
    Cpts = C * pts
    assert(
        np.allclose(Cpt1, Cpts[:, 0])
        and np.allclose(Cpt2, Cpts[:, 1])
    )
