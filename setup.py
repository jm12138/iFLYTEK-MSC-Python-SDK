from setuptools import setup


setup(
    name='msc',
    version='0.2.0',
    description='A package for IFLYTEK MSC.',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    author='jm12138',
    author_email='2286040843@qq.com',
    url='https://github.com/jm12138/iFLYTEK-MSC-Python-SDK',
    packages=['msc'],
    license='Apache License 2.0',
    requires=['pyaudio']
)