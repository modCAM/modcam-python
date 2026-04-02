# This file is part of modCAM, open source software for Computer Aided
# Manufacturing research.
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
# SPDX-License-Identifier: MPL-2.0

import igl
import numpy as np
import modcam.mesh
import pooch
import pytest


@pytest.fixture
def sphere_mesh():
    sphere_file = pooch.retrieve(
        url="https://github.com/modCAM/modcam-data/raw/main/mesh/sphere.stl",
        known_hash="sha256:502ed3c6aa892e0ff4e7d36ae575ce0e44bf564df6c208a0a8cf924299432109"
    )
    vertices, faces = igl.read_triangle_mesh(sphere_file)
    vertices, faces = igl.remove_duplicates(vertices, faces, 1.0e-7)
    for i in range(3):
        center = (vertices[:, i].max() - vertices[:, i].min()) / 2.0
        vertices[:, i] -= center
    vertices /= np.linalg.norm(vertices, ord=2, axis=1, keepdims=True)
    radius = 11.37
    vertices *= radius
    return vertices, faces, radius


def test_sphere_principal_curvature(sphere_mesh):
    vertices = sphere_mesh[0]
    faces = sphere_mesh[1]
    pv1, pv2, _, _ = modcam.mesh.principal_curvature(vertices, faces)
    radius = sphere_mesh[2]
    assert (pv1, pv2) == (pytest.approx(1.0 / radius), pytest.approx(1.0 / radius))


def test_empty_face_array():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 1.0, 0.0]])
    faces = np.empty((0, 3))
    pv1, pv2, pd1, pd2 = modcam.mesh.principal_curvature(vertices, faces)
    assert (pv1.size, pv2.size, pd1.size, pd2.size) == (0, 0, 0, 0)


def test_empty_vertex_array():
    vertices = np.empty((0, 3))
    faces = np.array([[0, 1, 2]])
    pv1, pv2, pd1, pd2 = modcam.mesh.principal_curvature(vertices, faces)
    assert (pv1.size, pv2.size, pd1.size, pd2.size) == (0, 0, 0, 0)
