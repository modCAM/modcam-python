import os
from typing import Optional


class Module:
    """Module attributes for generating Python binding boilerplate code.

    This class recursively traverses a directory tree to build up a Python
    module tree. Subdirectories correspond to submodules. Module function names
    are derived from C++ source (.cpp) files in those directories. Each
    directory should contain a "doc" file with the module docstring.

    Attributes
    ----------
    name : str
            The name of the module.
    doc : str
            Short module description.
    version : str
            Module version.
    supermodule : Module
            The parent module that contains this module.
    funcs : list[str]
            List of functions in the module.
    submodules : list[Module]
            List of submodules in this module.
    """

    name: str
    doc: str
    version: str
    supermodule: Optional["Module"]
    funcs: list[str]
    submodules: list["Module"]

    def __init__(
        self,
        root_dir: str,
        build_dir: str,
        name: str = "",
        version="",
        supermodule: Optional["Module"] = None,
    ):
        """Generate Python binding boilerplate code.

        Given a root directory, this constructor recurses the subdirectories to
        create a tree representation of Python modules. The module binding code
        is written to C++ source files in the given build directory.

        Parameters
        ----------
        root_dir : str
                The root directory.
        build_dir : str
                Write C++ files to this directory.
        name : str
                Override the module name. If unspecified, the module name is set to
                the corresponding directory name. Since the constructor works
                recursively, only the root module name can be overridden.
        version : str
                The module version (for example, "2.12.3"). If unspecified, the
                module will not contain version info.
        supermodule : Module, optional
                The parent module that contains this module. The user should leave
                this parameter unspecified.
        """
        self.dir_name = os.path.basename(root_dir)
        if name:
            self.name = name
        else:
            self.name = self.dir_name
        self.doc = ""
        with open(os.path.join(root_dir, "doc"), "r") as f:
            self.doc = f.read().strip()
        self.version = version
        self.supermodule = supermodule
        self.funcs = [
            f.name[:-4]
            for f in os.scandir(root_dir)
            if f.is_file() and f.name.endswith(".cpp")
        ]
        self.submodules = [
            Module(f.path, build_dir, supermodule=self)
            for f in os.scandir(root_dir)
            if f.is_dir()
        ]

        os.makedirs(build_dir, exist_ok=True)
        with open(f"{build_dir}/bind_{self.name}.cpp", "w") as f:
            f.write(self.boilerplate())

    def module_chain(self, join_char: str = "_") -> str:
        """Chain together this module name and its parents' names.

        This method is helpful for creating unique names for binding functions.

        Parameters
        ----------
        join_char : str, default="_"
                The character that goes between the module names.
        """
        module = self
        mod_chain = module.name
        while module.supermodule:
            mod_chain = module.supermodule.name + join_char + mod_chain
            module = module.supermodule
        return mod_chain

    def dir_chain(self, join_char: str = "::") -> str:
        """Chain together this module directory name and its parents' directory
        names.

        This method is helpful for namespacing functions.

        Parameters
        ----------
        join_char : str, default="::"
                The character that goes between the module directory names.
        """
        module = self
        mod_chain = module.dir_name
        while module.supermodule:
            mod_chain = module.supermodule.dir_name + join_char + mod_chain
            module = module.supermodule
        return mod_chain

    def boilerplate(self) -> str:
        """Generate binding boilerplate code."""
        if not self.supermodule:
            return self._boilerplate_root()
        return self._boilerplate()

    def _boilerplate_root(self) -> str:
        # Avoid problem with backslashes in f-strings
        newline_char = "\n"
        tab_char = "\t"
        quote_char = '"'

        code = f"""
#include <nanobind/nanobind.h>
namespace py = nanobind;

namespace {self.dir_chain()} {{

{"// Functions" if self.funcs else ""}
{newline_char.join(f"void bind_{func}(py::module_ &m);" for func in self.funcs)}

}} // namespace {self.dir_chain()}

{"// Submodules" if self.submodules else ""}
{newline_char.join(f"void bind_{submod.module_chain()}(py::module_ &m);" for submod in self.submodules)}

NB_MODULE({self.name}, m) {{
	{f'm.attr("__version__") = "{self.version}";' if self.version else ""}

	m.doc() = R"pydoc(\n{self.doc}\n)pydoc";

	{"// Function bindings" if self.funcs else ""}
{newline_char.join(f"{tab_char}{self.dir_chain()}::bind_{func}(m);" for func in self.funcs)}

	{"// Submodule bindings" if self.submodules else ""}
{newline_char.join(f"{tab_char}py::module_ {submod.name}_m = m.def_submodule({quote_char}{submod.name}{quote_char}, R{quote_char}pydoc({newline_char}{submod.doc}{newline_char})pydoc{quote_char});{newline_char}{tab_char}bind_{submod.module_chain()}({submod.name}_m);" for submod in self.submodules)}
}}
"""
        return code

    def _boilerplate(self) -> str:
        # Avoid problem with backslashes in f-strings
        newline_char = "\n"
        tab_char = "\t"
        quote_char = '"'

        code = f"""
#include <nanobind/nanobind.h>
namespace py = nanobind;

namespace {self.dir_chain()} {{

{"// Functions" if self.funcs else ""}
{newline_char.join(f"void bind_{func}(py::module_ &m);" for func in self.funcs)}

}} // namespace {self.dir_chain()}

{"// Submodules" if self.submodules else ""}
{newline_char.join(f"void bind_{submod.module_chain()}(py::module_ &m);" for submod in self.submodules)}

void bind_{self.module_chain()}(py::module_ &m) {{
	{"// Function bindings" if self.funcs else ""}
{newline_char.join(f"{tab_char}{self.dir_chain()}::bind_{func}(m);" for func in self.funcs)}

	{"// Submodule bindings" if self.submodules else ""}
{newline_char.join(f"{tab_char}py::module_ {submod.name}_m = m.def_submodule({quote_char}{submod.name}{quote_char}, R{quote_char}pydoc({newline_char}{submod.doc}{newline_char})pydoc{quote_char});{newline_char}{tab_char}bind_{submod.module_chain()}({submod.name}_m);" for submod in self.submodules)}
}}
"""
        return code


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Python binding boilerplate code"
    )
    parser.add_argument(
        "root_dir", help="The root directory of the module bindings source files."
    )
    parser.add_argument(
        "build_dir", help="Where to place the generated boilerplate files."
    )
    parser.add_argument(
        "--name",
        default="",
        help="The module name. If unspecified, it defaults to the directory name.",
    )
    parser.add_argument(
        "--version",
        default="",
        help="The module version. If unspecified, the module will not contain version info.",
    )
    args = parser.parse_args()
    print(args.root_dir)
    print(args.build_dir)
    print(args.name)
    print(args.version)
    root = Module(args.root_dir, args.build_dir, name=args.name, version=args.version)
