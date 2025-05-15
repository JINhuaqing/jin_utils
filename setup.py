from setuptools import setup, find_packages

setup(
    name='jin_utils',
    version='0.2',
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
    ]
)
