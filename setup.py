from setuptools import setup, find_packages


setup(
    name='pyclics-clustering',
    version='1.0.0',
    description="clustering algorithms for CLICS networks",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Johann-Mattis List and Robert Forkel',
    author_email='clics@shh.mpg.de',
    url='https://github.com/clics/pyclics-clustering',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.5',
    install_requires=[
        'attrs>=18.2',
        'python-louvain',
        'networkx',
        'pyclics>=2.0.0',
    ],
    extras_require={
        'dev': [
            'tox',
            'flake8',
            'wheel',
            'twine',
        ],
        'test': [
            'mock',
            'pytest>=3.6',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
        ],
    },
    entry_points={
        'clics.plugin': ['clustering=pyclics_clustering:includeme'],
    },
)
