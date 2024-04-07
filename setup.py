from setuptools import setup

from src import Constants

setup(
    name='pym3u8downloaderui',
    version=Constants.APP_VERSION,
    package_dir={'': 'src'},
    url='https://github.com/coldsofttech/pym3u8downloaderui',
    license='MIT',
    author='coldsofttech',
    description='',
    entry_points={
        'console_scripts': [
            'pym3u8downloaderui = src.__init__:main'
        ]
    },
    install_requires=[
        'requests',
        'pym3u8downloader@ git+https://github.com/coldsofttech/pym3u8downloader.git'
    ]
)
