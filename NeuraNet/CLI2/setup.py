from setuptools import setup, find_packages

setup(
        name="bcloud",
        version="1.0.1",
        packages=find_packages(),
        description = "A CLI tool for file management",
        long_description = "A CLI tool for file management",
        entry_points={
            "console_scripts": [
                "bcloud = bcloud.cli:main",
                ],
            },
        )
