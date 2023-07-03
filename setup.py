from setuptools import setup, find_packages

setup(
    name="liteplay",
    version="1.0.0",
    packages=(
        find_packages()
        + find_packages(where="./utils")
        + find_packages(where="./modules")
    ),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "liteplay = main:cli",
        ],
    },
)
