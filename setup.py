from setuptools import setup
from msc import __version__


setup(
    name='msc',
    version=__version__,
    description='A package for IFLYTEK MSC.',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    author='jm12138',
    author_email='2286040843@qq.com',
    url='https://github.com/jm12138/iFLYTEK-MSC-Python-SDK',
    packages=['msc'],
    license='Apache License 2.0',
    data_files=[('bin', ['msc/bin/msc_x64.dll', 'msc/bin/msc_x86.dll', 'msc/bin/msc_x64.so', 'msc/bin/msc_x86.so'])],
    platforms=['win32', 'win-amd64', 'linux-i686', 'linux-x86_64']
)