from setuptools import setup

setup(
    name='pym3u8downloaderui',
    version='0.1.0',
    packages=[''],
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
        'pym3u8downloader@ git+https://github.com/coldsofttech/pym3u8downloader.git'
    ]
)
