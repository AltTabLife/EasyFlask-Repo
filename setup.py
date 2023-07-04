from setuptools import setup

setup(
    name='EasyFlask',
    version='1.0',
    description='Flask generator package from a yaml file',
    author='TabBackIn',
    author_email='andrewm@tabbackin.com',
    packages=['EasyFlask'],
    install_requires=['ruamel.yaml', 'pathlib'],
)