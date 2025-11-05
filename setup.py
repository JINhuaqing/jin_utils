from setuptools import setup, find_packages
from jin_utils.version import __version__

setup(
    name='jin_utils',
    version=__version__,
    author='Huaqing Jin',
    author_email='kevinjin0423@gmail.com',
    description='The package contains some useful functions for my daily work',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'numpy>=1.18.0',
        'pandas>=1.0.0', 
        'easydict',
        'matplotlib',
        'rpy2',
        'pyyaml',
    ]
)
