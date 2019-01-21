import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'stlfed_py',
    version = '0.1.0',
    author = ['Ryan Price'],
    author_email = ['ryapric@gmail.com'],
    description = 'Short description',
    long_description = long_description,
    url = 'https://url_to_repo',
    packages = setuptools.find_packages(),
    python_requires = '>=3.6.*',
    install_requires = [
        'pandas>=0.23.4',
        'statsmodels>=0.9.0'
    ],
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points = {
        'console_scripts': [
            'pkgname-main-script=pkgname.modulename.modulename_main:main'
        ]
    },
    include_package_data = True
)
