import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genderComputer", 
    version="0.1",
    author="tue-mdse",
    author_email="help@help.org",
    description="Infer gender from name and location",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tue-mdse/genderComputer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License version 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
        'genderComputer': ['nameLists/*.*'],
    },
    include_package_data=True,
    install_requires = ['unidecode==1.3.2','nameparser==1.0.6'],
    zip_safe=False
)
