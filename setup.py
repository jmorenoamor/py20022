from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='py20022',
    version='0.1',
    description='py20022 order generator',
    long_description=readme(),
    url='http://github.com/jmoreno/py20022',
    author='Jesús Moreno Amor',
    author_email='jesus@morenoamor.com',
    license='MIT',
    packages=['py20022'],
    install_requires=[
        'dexml',
    ],
    zip_safe=False)
