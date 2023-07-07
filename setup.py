from setuptools import setup, find_packages

setup(
    name='EasyFlask',
    version='1.1',
    description='Flask generator package from a yamlish file',
    author='TabBackIn',
    author_email='andrewm@tabbackin.com',
    packages=find_packages(),
    install_requires=['ruamel.yaml', 'pathlib'],
)