try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description' : 'Optical Measurement Code',
    'author' : 'Mark S. Brown',
    'url' : 'www.github.com/marksbrown',
    'download_url' : 'www.github.com/marksbrown',
    'author_email' : 'contact@markbrown.io',
    'install_requires' : [''],
    'packages' : [''],
    'scripts' : [],
    'name': ''
}

setup(**config)
