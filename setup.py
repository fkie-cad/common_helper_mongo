from setuptools import setup, find_packages

VERSION = '0.4.0'

setup(
    name='common_helper_mongo',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'pymongo >= 3.2'
    ],
    description='MongoDB helper functions',
    author='Fraunhofer FKIE',
    author_email='peter.weidenbach@fkie.fraunhofer.de',
    url='http://www.fkie.fraunhofer.de',
    license='GPL-3.0'
)
