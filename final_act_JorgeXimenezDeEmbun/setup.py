from setuptools import setup

setup(
    name="my_app",
    version="0.1",
    packages=["my_app"],
    install_requires=["requests", "matplotlib", "sqlite3"],
    entry_points={
        "console_scripts": [
            "my_app = my_app.__main__:main"
        ]
    }
)