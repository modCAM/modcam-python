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

#include "modcam/mesh/per_vertex_basis.h"
#include "modcam/mesh/per_vertex_normals.h"
#include "modcam/mesh/principal_curvature.h"
#include "modcam/mesh/voronoi_area.h"

#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

void bind_mesh(py::module &m)
{
	m.def("per_vertex_basis", &modcam::mesh::per_vertex_basis,
		  py::arg_v("vertex_normals", "V-by-3 array of floats"),
		  "Compute an orthonormal set of basis vectors where the z-axis is the "
		  "vertex normal. Returns a tuple of three V-by-3 arrays of floats.");
	m.def("per_vertex_normals", &modcam::mesh::per_vertex_normals,
		  py::arg_v("vertices", "V-by-3 array of floats"),
		  py::arg_v("faces", "F-by-3 array of ints"),
		  "Compute the normal vector at each vertex in a triangle mesh. "
		  "Returns V-by-3 array of floats.");
	m.def("principal_curvature", &modcam::mesh::principal_curvature_rus2004,
		  py::arg_v("vertices", "V-by-3 array of floats"),
		  py::arg_v("faces", "F-by-3 array of ints"),
		  "Computes the principal curvature values and their directions.");
	m.def("voronoi_area", &modcam::mesh::voronoi_area,
		  py::arg_v("vertices", "V-by-3 array of floats"),
		  py::arg_v("faces", "F-by-3 array of ints"),
		  "Compute the Voronoi cell areas for the triangles in a mesh. Returns "
		  "F-by-3 array of floats.");
}
