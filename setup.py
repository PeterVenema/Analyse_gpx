from setuptools import setup, find_packages

setup(
    name="analyzeGPX",
    version="0.0.1",
    author="Peter Venema",
    description="Analyse GPX tracks. First basic version.",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas"
    ]
)
