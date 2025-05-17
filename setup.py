from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="RAGonSagemaker",
    version="0.1.0",
    author="MahammadRafi",
    author_email="mrafi@uw.edu",
    description="A production-ready RAG system built on AWS SageMaker with MongoDB Atlas integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/RAGwithSagemaker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ragon=RAGwithSagemaker.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "RAGwithSagemaker": ["config/*.yaml", "templates/*"],
    },
)
