import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ansimpleapi",
    version="0.2.0",
    author="anttin",
    author_email="muut.py@antion.fi",
    description="A very simple api engine framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anttin/apiengine/tree/ansimpleapi",
    packages=setuptools.find_packages(),
    install_requires=[
      'cherrypy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
