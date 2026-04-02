# This file is part of modCAM, open source software for Computer Aided
# Manufacturing research.
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
# SPDX-License-Identifier: MPL-2.0

import numpy as np
import modcam.mesh
import pytest


@pytest.fixture
def partial_icosahedron():
    phi = (1.0 + np.sqrt(5.0)) / 2.0
    vertices = np.array(
        [
            [phi, 1.0, 0.0],
            [phi, -1.0, 0.0],
            [-phi, -1.0, 0.0],
            [-phi, 1.0, 0.0],
            [1.0, 0.0, phi],
            [-1.0, 0.0, phi],
            [-1.0, 0.0, -phi],
            [1.0, 0.0, -phi],
            [0.0, phi, 1.0],
            [0.0, phi, -1.0],
            [0.0, -phi, -1.0],
            [0.0, -phi, 1.0],
        ]
    )
    vertices = vertices / np.linalg.norm(vertices, axis=1, ord=2).reshape(
        vertices.shape[0], 1
    )
    faces = np.array(
        [
            [5, 4, 8],
            [4, 5, 11],
            [8, 4, 0],
            [4, 1, 0],
            [4, 11, 1],
            [11, 10, 1],
            [11, 2, 10],
            [5, 2, 11],
            [1, 10, 7],
            [0, 1, 7],
        ]
    )
    return (vertices, faces)


@pytest.fixture
def vertex_normals(partial_icosahedron):
    vertices = partial_icosahedron[0]
    faces = partial_icosahedron[1]
    return modcam.mesh.per_vertex_normals(vertices, faces)


@pytest.mark.parametrize("dim", [(0), (1)])
def test_shape(partial_icosahedron, vertex_normals, dim):
    vertices = partial_icosahedron[0]
    assert vertex_normals.shape[dim] == vertices.shape[dim]


@pytest.mark.parametrize("row", [(1), (4), (11)])
def test_normals(partial_icosahedron, vertex_normals, row):
    vertices = partial_icosahedron[0]
    assert vertex_normals[row, :] == pytest.approx(vertices[row, :])


@pytest.mark.parametrize("row", [(3), (6), (9)])
def test_normals(vertex_normals, row):
    assert np.isnan(vertex_normals[row, :]).all()
