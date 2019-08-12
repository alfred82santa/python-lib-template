import ast
from pathlib import Path

from setuptools import find_packages, setup

PACKAGE_NAME = 'pylibrary_template'

path = Path(Path(__file__).parent, PACKAGE_NAME, '__init__.py')

with open(path, 'r') as file:
    t = compile(file.read(), str(path), 'exec', ast.PyCF_ONLY_AST)
    for node in (n for n in t.body if isinstance(n, ast.Assign)):
        if len(node.targets) != 1:
            continue

        name = node.targets[0]
        if not isinstance(name, ast.Name) or \
                name.id not in ('__version__', '__version_info__', 'VERSION'):
            continue

        v = node.value
        if isinstance(v, ast.Str):
            version = v.s
            break
        if isinstance(v, ast.Tuple):
            r = []
            for e in v.elts:
                if isinstance(e, ast.Str):
                    r.append(e.s)
                elif isinstance(e, ast.Num):
                    r.append(str(e.n))
            version = '.'.join(r)
            break

with Path(Path(__file__).parent, 'requirements.txt').open() as f:
    install_requires = [s.strip() for s in f.readlines() if not s.startswith('-')]

# Get the long description from the README file
with Path(Path(__file__).parent, 'README.rst').open(encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pylibrary-template',

    version=version,

    description='Python Library Template',
    long_description=long_description,

    url='https://github.com/alfred82santa/python-lib-template',

    author='Alfred Santacatalina',
    author_email='alfred82santa@gmail.com',
    include_package_data=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': []
    }
)
