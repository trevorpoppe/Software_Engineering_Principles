from setuptools import setup, find_packages

setup(
    name="geo-matcher",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "geo-matcher=geo_matcher.cli:main"
        ]
    },
    author="Your Name",
    description="A simple tool to match coordinates using the haversine formula",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
