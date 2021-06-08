import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ilusive-moose-shop-client",
    version="0.0.1",
    author="Adam Ivansky",
    author_email="illusive.moose.shop@gmail.com",
    description="Client for the Illusive Moose online marketplace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snow884/illusive_moose_api_client",
    project_urls={
        "Bug Tracker": "https://github.com/snow884/illusive_moose_api_client/issues",
        "Website": "https://http://shop.illusive-moose.ca"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)