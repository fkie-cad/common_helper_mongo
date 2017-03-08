import os
import subprocess
from setuptools import setup, find_packages

try:
    VERSION = subprocess.check_output(['git', 'describe', '--always'], cwd=os.path.dirname(os.path.abspath(__file__))).strip().decode('utf-8')
except Exception:
    VERSION = "0.x"


setup(
    name="common_helper_mongo",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'pymongo >= 3.2'
    ],
    description="MongoDB helper functions",
    author="Fraunhofer FKIE",
    author_email="peter.weidenbach@fkie.fraunhofer.de",
    url="http://www.fkie.fraunhofer.de",
    license="MIT License"
)
