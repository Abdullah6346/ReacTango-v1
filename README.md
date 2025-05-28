# React Tango Creator (`create-react-tango`)

[![PyPI version](https://img.shields.io/pypi/v/react-tango-creator.svg)](https://pypi.org/project/react-tango-creator/)
[![Python Version](https://img.shields.io/pypi/pyversions/react-tango-creator.svg)](https://pypi.org/project/react-tango-creator/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Optional: Add build status, coverage, etc. if you set up CI -->
<!-- [![Build Status](https://travis-ci.org/your-username/react-tango-creator.svg?branch=main)](https://travis-ci.org/your-username/react-tango-creator) -->

`reactango` is a command-line utility designed to quickly bootstrap new full-stack projects using the **ReactTangoTemplate**. This template combines a React frontend (with TanStack Router and Vite) with a Django backend, providing a modern, type-safe, and containerized development experience.

This CLI tool automates the initial project setup by:

1. Cloning the [ReactTangoTemplate](https://github.com/Abdullah6346/ReactTangoTemplate).
2. Removing the template's Git history.
3. Initializing a fresh Git repository for your new project.
4. Making an initial commit with the template files, so you can start your work immediately.

## Features

- **Rapid Project Scaffolding**: Create a new React + Django project in seconds.
- **Clean Git History**: Starts your project with a fresh Git repository, independent of the template's history.
- **Customizable**: Choose a specific branch of the template if needed.
- **Flexible**: Option to skip automatic Git initialization.
- **Easy to Use**: Simple command-line interface.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python**: Version 3.7 or higher.
- **pip**: Python package installer (usually comes with Python).
- **Git**: Version control system.

## Installation

### Option 1: From PyPI (Recommended for Users)

The easiest way to install `reactango` is from the Python Package Index (PyPI):

```bash
pip install react-tango-creator



python3 -m venv venv
source venv/bin/activate
   pip install -e .
```
