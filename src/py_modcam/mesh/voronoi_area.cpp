/*
 * This file is part of modCAM, open source software for Computer Aided
 * Manufacturing research.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
 * SPDX-License-Identifier: MPL-2.0
 */

#include "default_types.h"

#include <modcam/mesh/voronoi_area.h>

#include <nanobind/eigen/dense.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

namespace py = nanobind;
using namespace py::literals;

namespace py_modcam::mesh {

auto voronoi_area(const py::DRef<const Eigen::MatrixXN> &vertices,
                  const py::DRef<const Eigen::MatrixXI> &faces) {
	Eigen::MatrixXN v_area;
	modcam::mesh::voronoi_area(v_area, vertices, faces);
	return v_area;
}

void bind_voronoi_area(py::module_ &m) {
	m.def("voronoi_area", &py_modcam::mesh::voronoi_area, "vertices"_a,
	      "faces"_a,
	      R"(
Compute the Voronoi cell areas for the triangles in a mesh.

Parameters
----------
vertices : array_like
    V-by-3 matrix of vertex positions
faces : array_like
    F-by-3 matrix of face indices

Returns
-------
array_like
    F-by-3 matrix of Voronoi areas
)");
}

} // namespace py_modcam::mesh
