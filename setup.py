from glob import glob
from os.path import basename, splitext
from setuptools import find_packages, setup


setup(
    name="icare_client",
    version="0.1",
    description="iCare Childcare Client",
    author="Ben Hearsum",
    author_email="ben@hearsum.ca",
    include_package_data=True,
    install_requires=["click", "jinja2", "requests"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    url="https://github.com/bhearsum/icare_client",
    license="MPL-2.0",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "icare = icare_client.cli:cli",
        ],
    },
)
