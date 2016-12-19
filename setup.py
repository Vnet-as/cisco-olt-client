import setuptools

setuptools.setup(
    name="cisco_olt_client",
    version="0.1.0",
    url="https://github.com/Vnet-as/cisco-olt-client",
    author="Michal Kuffa",
    author_email="michal.kuffa@gmail.com",
    description="Python wrapper for cisco's olt boxes commands executed via ssh",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
