from setuptools import setup, find_packages

setup(
    name='create-cmake-app',
    version='1.0.0',
    license='MIT',
    author="River2056",
    author_email='chen0625tung@gmail.com',
    packages=find_packages(),
    entry_points= {
        "console_scripts": ["cca=cca.create_cmake_app:main"]
    },
    url='https://github.com/River2056/create-cmake-app',
)
