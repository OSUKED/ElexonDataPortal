## !!! You should make no changes in this file !!!
## !!! All changes should be made in settings.ini !!!

import setuptools
from configparser import ConfigParser

with open("README.md", "r") as fh:
    long_description = fh.read()
    
config = ConfigParser(delimiters=['='])
config.read('settings.ini')
setup_kwargs = dict(config['DEFAULT'])

setuptools.setup(
    name=setup_kwargs['lib_name'],
    version=setup_kwargs['version'],
    author=setup_kwargs['author'],
    author_email=setup_kwargs['author_email'],
    description=setup_kwargs['description'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=setup_kwargs['git_url'],
    packages=setuptools.find_packages(),
    install_requires=setup_kwargs['requirements'].split(' '),
    extras_require={'dev': setup_kwargs['dev_requirements'].split(' ')},
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=f">={setup_kwargs['min_python']}",
)