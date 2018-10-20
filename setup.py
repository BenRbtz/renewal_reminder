from setuptools import setup, find_packages

setup(
    name="renewal_reminder",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires=">=3.6",
    install_requires=['python-telegram-bot>=11.1.0'],
    tests_require=['pytest', 'pytest-mock', 'pytest-runner'],
)
