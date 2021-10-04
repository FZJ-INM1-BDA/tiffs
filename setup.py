from setuptools import setup
from os.path import join, dirname, abspath


def read_utf8(*args):
    with open(join(*args), encoding="utf-8") as f:
        return f.read()


directory, m = dirname(abspath(__file__)), {}
exec(read_utf8(directory, 'tiffs', '__meta__.py'), m)
requirements = read_utf8(directory, 'requirements.txt').strip().split("\n")
long_description = read_utf8(directory, 'README.md')

setup(
    author=m['__author__'],
    author_email=m['__email__'],
    name=m['__title__'],
    version=m['__version__'],
    description=m['__summary__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=m['__url__'],
    packages=['tiffs'],
    package_data={'': ['LICENSE', 'requirements.txt', 'README.md']},
    include_package_data=True,
    install_requires=requirements,
    license=m['__license__'],
    keywords=['tiffs', 'tiff', 'stack', 'fzj', 'julich', 'juelich'],
    classifiers=[
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
)
