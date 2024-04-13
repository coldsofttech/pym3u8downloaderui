from setuptools import setup

from src import Constants

setup(
    name=Constants.APP_PACKAGE_NAME,
    version=Constants.APP_VERSION,
    package_dir={'': 'src'},
    url='https://github.com/coldsofttech/pym3u8downloaderui',
    license='MIT',
    author='coldsofttech',
    description=Constants.APP_PACKAGE_DESCRIPTION,
    entry_points={
        'console_scripts': [
            'pym3u8downloaderui = src.__init__:main'
        ]
    },
    install_requires=[
        'requests',
        'pym3u8downloader'
    ],
    requires_python=">=3.10",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=["m3u8-playlist", "m3u8", "m3u8-downloader", "m3u8-ui"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ]
)
