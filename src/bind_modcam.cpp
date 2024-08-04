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

#include <pybind11/pybind11.h>

namespace py = pybind11;

void bind_mesh(py::module &);

PYBIND11_MODULE(modcam, m)
{
	m.doc() =
		"Open source software for Computer Aided Manufacturing (CAM) research";

	py::module mesh_m =
		m.def_submodule("mesh", "Tools for working with triangle mesh data");
	bind_mesh(mesh_m);
}