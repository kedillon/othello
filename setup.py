from setuptools import setup

setup(
    name='othello',
    version='0.1.0',
    packages=['simulator', 'client', 'lib'],
    include_package_data=True,
    install_requires=[
        'pycodestyle==2.5.0',
        'pydocstyle==4.0.1',
        'pylint==2.3.1',
        'pytest==5.1.2',
        'sh==1.12.14',
        'numpy==1.17.3',
        'torch==1.3.0.post2'
        'Click==7.0'
    ],
)
