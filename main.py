import os
import sys
import argparse
import textwrap
import subprocess

from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="cmake template cli tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            navigate to destination and run:
            python main.py -n <your-project-name> (REQUIRED)

            script will generate project directory and necessary nested template files
                               """
        ),
    )
    parser.add_argument("-n", "--name", help="project name")

    args = parser.parse_args()

    if not args.name:
        print("Please provide project directory name!")
        sys.exit(1)

    project_name = args.name
    cwd = Path(os.getcwd())
    # create project directory
    print(f"creating project directory: {project_name}...")
    os.mkdir(cwd.joinpath(project_name))

    project_dir_path = Path(cwd.joinpath(project_name))
    cmake_dir_path = Path(project_dir_path.joinpath("cmake"))
    app_dir_path = Path(project_dir_path.joinpath("app"))
    src_dir_path = Path(project_dir_path.joinpath("src"))
    external_dir_path = Path(project_dir_path.joinpath("external"))

    # creating directories
    cmake_dir_path.mkdir()
    print(f"{str(cmake_dir_path)} created")
    app_dir_path.mkdir()
    print(f"{str(app_dir_path)} created")
    src_dir_path.mkdir()
    print(f"{str(src_dir_path)} created")
    external_dir_path.mkdir()
    print(f"{str(external_dir_path)} created")

    # Makefile
    makefile_path = Path(project_dir_path.joinpath("Makefile"))
    makefile_path.touch()
    print(f"{str(makefile_path)} created")
    with open(makefile_path, "wt", encoding="utf-8") as output:
        output.write(
            textwrap.dedent(
                """
                exe_name := task

                all: run

                clean:
                \trm -rf ./build
                \tmkdir build

                build: clean
                \tcmake -S . -B ./build
                \tcmake --build ./build

                run: build
                \t./build/app/Debug/$(exe_name).exe

                pre_generate: clean
                \tcmake -S . -B ./build -GNinja
                \tcmake --build ./build
                \tmv ./build/compile_commands.json .
                
                generate: pre_generate
                \trm -rf ./build
                \tmkdir build
            """
            )
        )
    print("Done creating Makefile")
    # Makefile end

    # root CMakeLists.txt
    root_cmakelists_path = Path(project_dir_path).joinpath("CMakeLists.txt")
    root_cmakelists_path.touch()
    print(f"{str(root_cmakelists_path)} created")
    with open(root_cmakelists_path, "wt", encoding="utf-8") as output:
        output.write(
            textwrap.dedent(
                """
            cmake_minimum_required(VERSION 3.16)

            project(task)

            set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
            set(CMAKE_CXX_STANDARD 17)
            set(CMAKE_CXX_STANDARD_REQUIRED ON)
            set(CMAKE_CXX_EXTENSIONS OFF) 

            set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/")
            include(AddGitSubmodule)

            add_subdirectory(src)
            add_subdirectory(app)
        """
            )
        )
    print("Done creating root CMakeLists.txt")
    # root CMakeLists.txt end

    # AddGitSubmodule.cmake
    add_git_submodule_cmake_path = Path(cmake_dir_path).joinpath(
        "AddGitSubmodule.cmake"
    )
    add_git_submodule_cmake_path.touch()
    print(f"{str(add_git_submodule_cmake_path)} created")
    with open(add_git_submodule_cmake_path, "wt", encoding="utf-8") as output:
        output.write(
            textwrap.dedent(
                """
            function(add_git_submodule dir)
            \tfind_package(Git REQUIRED)

            \tif (NOT EXISTS ${dir}/CMakeLists.txt)
            \t\texecute_process(COMMAND ${GIT_EXECUTABLE}
            \t\t\tsubmodule update --init --recursive -- ${dir}
            \t\t\tWORKING_DIRECTORY ${PROJECT_SOURCE_DIR})
            \tendif()

            \tadd_subdirectory(${dir})
            endfunction() 
        """
            )
        )
    print("Done creating AddGitSubmodule.cmake")
    # AddGitSubmodule.cmake end

    # app/main.cpp
    main_cpp_path = Path(app_dir_path).joinpath("main.cpp")
    main_cpp_path.touch()
    print(f"{str(main_cpp_path)} created")
    with open(main_cpp_path, "wt", encoding="utf-8") as output:
        output.write(
            textwrap.dedent(
                """
            #include <iostream>

            int main() {
                std::cout << "hello from cmake template cli!" << '\\n';
                return 0;
            }
        """
            )
        )
    print("Done creating app/main.cpp")
    # app/main.cpp end

    # app/CMakeLists.txt
    app_cmakelists_txt_path = Path(app_dir_path).joinpath("CMakeLists.txt")
    app_cmakelists_txt_path.touch()
    print(f"{str(app_cmakelists_txt_path)} created")
    with open(app_cmakelists_txt_path, "wt", encoding="utf-8") as output:
        output.write(
            textwrap.dedent(
                """
            set(EXECUTABLE_SOURCES 
                "main.cpp")

            add_executable(${PROJECT_NAME} ${EXECUTABLE_SOURCES})
        """
            )
        )
    print("Done creating app/CMakeLists.txt")
    # app/CMakeLists.txt end

    # src/CMakeLists.txt
    Path(src_dir_path).joinpath("CMakeLists.txt").touch()
    print("Done creating src/CMakeLists.txt")
    # src/CMakeLists.txt end

    # .gitignore
    gitignore_path = Path(project_dir_path).joinpath(".gitignore")
    gitignore_path.touch()
    with open(gitignore_path, "wt", encoding="utf-8") as output:
        output.write(
            textwrap.dedent(
                """
            .ccls-cache/
            external/
            build/
            compile_commands.json
        """
            )
        )
    # gitignore end

    # git init
    os.chdir(project_dir_path)
    result = subprocess.run(["git", "init"], stdout=subprocess.PIPE)
    print(result)

    print("Done generating cmake template project!")


if __name__ == "__main__":
    main()
