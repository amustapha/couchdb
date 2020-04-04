import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="couchdb", # Replace with your own username
    version="0.0.4",
    author="Abdulhakeem Mustapha",
    author_email="abdulhakeemmustapha@gmail.com",
    description="A package for handing basic CouchDB Operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aamustapha/couchdb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
    ],
    python_requires='>=3.6',
)