import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid_metrics-elliottohara",
    version="0.0.1",
    author="Elliott O'Hara",
    author_email="github@elliottohara.com",
    description="Tracks various Covid19 metrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elliottohara/covid_metrics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
