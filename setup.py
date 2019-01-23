from setuptools import setup, find_packages


setup(
    name='pyclics-louvain',
    version='0.1',
    description="",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Johann-Mattis List and Robert Forkel',
    author_email='clics@shh.mpg.de',
    url='https://github.com/clics/pyclics-louvain',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.5',
    install_requires=[
        'python-louvain',
        'pyclics',
    ],
    entry_points={
        'clics.plugin': ['pyclics=pyclics_louvain:includeme'],
    },
)
