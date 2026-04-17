"""
Setup script for Data Scooper
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="data-scooper",
    version="1.0.0",
    author="",
    description="Data pipeline for converting Excel/PDF to RAG and LLM integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=2.1.4",
        "openpyxl>=3.1.2",
        "PyPDF2>=3.0.1",
        "pdfplumber>=0.10.3",
        "requests>=2.31.0",
        "httpx>=0.25.2",
        "google-generativeai>=0.3.2",
        "numpy>=1.26.2",
        "scikit-learn>=1.3.2",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.2",
        "pydantic-settings>=2.1.0",
        "aiohttp>=3.9.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "data-scooper=main:main",
        ],
    },
)
