from setuptools import setup, find_packages

setup(
    name="ms_lifestyle_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "plotly",
    ],
)