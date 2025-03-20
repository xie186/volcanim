from setuptools import setup, find_packages
    
setup(
    name="volcanim",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "manim==0.19.0",
        "pandas==1.3.3",
        "numpy==1.21.2",
        "pytest==8.3.5",
        "pytest-cov==4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "volcanim=volcanim.cli:main",
        ],
    },
    author="Shaojun Xie",
    author_email="xieshaojun0526@gmail.com",
    description="A command-line tool and library for generating animated Enhanced Volcano plots with Manim",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xie186/volcanim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
