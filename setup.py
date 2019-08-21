from setuptools import setup

setup(
    name="cloaker",
    version="0.0.1",
    description="Simple keycloak client for python",
    py_modules=["cloaker"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
)
