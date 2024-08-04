# This file is part of modCAM, open source software for Computer Aided
# Manufacturing research.
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
# SPDX-License-Identifier: MPL-2.0

pybind11_add_module(
	modCAM_python 
	"${CMAKE_CURRENT_SOURCE_DIR}/bind_modcam.cpp" 
	"${CMAKE_CURRENT_SOURCE_DIR}/bind_mesh.cpp" 
)
target_link_libraries(
	modCAM_python 
	PRIVATE 
		Eigen3::Eigen 
		modCAM::mesh 
)
set_target_properties(
	modCAM_python PROPERTIES 
	LIBRARY_OUTPUT_NAME "modcam"
)

install(
	TARGETS modCAM_python 
	LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
