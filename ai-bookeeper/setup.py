from setuptools import setup, find_packages

setup(
    name="ai-bookkeeper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openai"
    ],
    entry_points={
        "console_scripts": [
            "ai-bookkeeper=ai_bookkeeper.cli:main"
        ]
    },
    author="Trevor Poppe",
    description="A CLI tool to interact with your data using SQLite and OpenAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)
