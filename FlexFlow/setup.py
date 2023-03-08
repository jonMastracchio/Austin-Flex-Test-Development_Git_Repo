import os
from setuptools import setup, find_packages

setup(
    name='flexflow',
    version='0.0.1.1',
    packages=find_packages(),
    url='',
    license='Flex LLC.',
    author='Jon Mastracchio',
    author_email='Jonathon.Mastracchio1@flex.com',
    description='FlexFlow Webservice Module. Initial Release [0.0.1]',
    python_requires='>=3.7'
)

f = open('dependencies.txt','r')
items = f.readlines()
f.close()
for element in items:
	os.system('pip install '+element.strip())
	
os.system('pip list')