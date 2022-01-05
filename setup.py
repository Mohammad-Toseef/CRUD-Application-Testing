import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crud-application-toseef",
    version="0.0.6",
    author="Mohammad Toseef",
    author_email="mohammad@codeops.tech",
    description="CRUD Application to upload csv file and perform CRUD Operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "HTTPServer"},
    packages=setuptools.find_packages(where="HTTPServer"),
    include_package_data=True,
    package_data={'': ['data/*', 'templates/*', 'static/*']},
    python_requires=">=3.6",
    install_requires=[
                        "python-dotenv",
                        "Flask",
                        "mysql-connector-python"
                        ]
)
