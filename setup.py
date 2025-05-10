from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rdframework",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A framework for creating modern web applications with React (TanStack Router) and Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rdframework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.2.0",
        "djangorestframework>=3.14.0",
        "django-cors-headers>=4.3.0",
        "psycopg2-binary>=2.9.9",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "rdframework=rdframework.__main__:main",
        ],
    },
) 