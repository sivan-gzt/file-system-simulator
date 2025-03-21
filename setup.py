from setuptools import setup, find_packages

setup(
    name="file-system-simulator",  # This is the name of your package
    version="1.0.0",
    packages=find_packages(where="src"),  # Finds packages in the "src" directory
    package_dir={"": "src"},  # Maps the "src" directory as the root for packages
    entry_points={
        "console_scripts": [
            "file-system-simulator=file_system_simulator.cli:main",  # Defines the CLI command
        ],
    },
    install_requires=[],
)