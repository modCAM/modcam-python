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


def test_equilateral_triangle():
    vertices = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, np.sqrt(3.0) / 2.0, 0.0]]
    )
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area(vertices, faces)
    assert weights == pytest.approx(0.14433757)


def test_obtuse_triangle():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.1, 0.0]])
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area(vertices, faces)
    assert (weights == np.array([[0.0125, 0.0125, 0.025]])).all()


def test_colocated_vertices():
    vertices = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area(vertices, faces)
    assert (weights == 0.0).all()


def test_face_singularity():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.1, 0.0]])
    faces = np.array([[0, 0, 0]])
    weights = modcam.mesh.voronoi_area(vertices, faces)
    assert (weights == 0.0).all()


def test_colinear_vertices():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.0, 0.0]])
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area(vertices, faces)
    assert (weights == 0.0).all()


def test_empty_face_array():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.1, 0.0]])
    faces = np.array([[]])
    weights = modcam.mesh.voronoi_area(vertices, faces)
    assert (weights == 0.0).all()


def test_empty_vertex_array():
    vertices = np.array([[]])
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area(vertices, faces)
    assert (weights == 0.0).all()


def test_2D_vertex_array():
    vertices = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 0.1]])
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area(vertices, faces)
    assert (weights == np.array([[0.0125, 0.0125, 0.025]])).all()


def test_improperly_sized_face_array():
    with pytest.raises(ValueError):
        vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.1, 0.0]])
        faces = np.array([[0, 1]])
        modcam.mesh.voronoi_area(vertices, faces)
