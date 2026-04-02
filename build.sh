#!/bin/bash

usage() {
    echo "Usage: $0 [-t] MODCAM_INSTALL_DIR"
	echo "  or:  $0 -h"
	echo "Build the modCAM python bindings"
	echo ""
    echo "Options:"
    echo "  -t          Build with pytest tests"
    echo "  -h          Display the help message"
	echo ""
	echo "MODCAM_INSTALL_DIR is the modCAM installation directory, which contains the "
	echo "CMake config files."
}

build_with_tests=""
while getopts ':ht' option; do
	case "${option}" in
		t) build_with_tests='[test]'
		   ;;
		h) # Help option
		   usage
		   exit 0
		   ;;
		\?) # Invalid option
		    echo "Invalid option: -$OPTARG"
		    usage
		    exit 1
		    ;;
  esac
done
shift $((OPTIND - 1))

modcam_install_path="$1" #"../modcam/build/install"
echo "${modcam_install_path}"
export CMAKE_PREFIX_PATH=$modcam_install_path

# Copy the VERSION file to a local directory so that we can use it in 
# pyproject.toml.
version_path="external/modcam/include"
cmake -E make_directory $version_path
cp $modcam_install_path/include/VERSION $version_path

# cmake -S . -B build/ -DCMAKE_TOOLCHAIN_FILE:FILEPATH="$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake"
python -m pip install -e .${build_with_tests}
