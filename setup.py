from setuptools import setup, find_packages

setup(
    name="chagu",
    version="0.1.1",
    author="Talex maxim",
    author_email="taimax13@gmail.com",
    description="ChainGuard: A Secure Data Transformation and Transfer Protocol using Blockchain Technology",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/taimax13/chainguard",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'cryptography',
    ],
)
