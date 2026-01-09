"""Setup configuration for TinyBigCorp Backend package."""

from setuptools import setup, find_packages

# Read requirements
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

with open("requirements-dev.txt") as f:
    dev_requirements = [line.strip() for line in f if line.strip() and not line.startswith("#") and not line.startswith("-r")]

# Read README
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tinybigcorp-backend",
    version="0.1.0",
    author="anhhoangdev",
    author_email="anhhoang.021203@gmail.com",  # Update this
    description="Enterprise backend with Clean Architecture and SOLID principles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CkoThuw11/AdventureWork-ERP-backend",
    project_urls={
        "Bug Tracker": "https://github.com/CkoThuw11/AdventureWork-ERP-backend/issues",
        "Documentation": "https://github.com/CkoThuw11/TinyBigCorp/tree/main/docs",
        "Source Code": "https://github.com/CkoThuw11/AdventureWork-ERP-backend",
    },
    packages=find_packages(where=".", include=["src", "src.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: FastAPI",
        "Typing :: Typed",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    entry_points={
        "console_scripts": [
            "tinybigcorp-api=src.api.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
