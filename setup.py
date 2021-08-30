# by G.Landais (CDS) (08/2021)

import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

from cdsclient.__init__ import __version__
version = __version__

setuptools.setup(
    name="cdsclient", # Replace with your own username
    version=version,
    author="Gilles Landais (CDS)",
    url='https://github.com/cds-astro/cds.cdsclient',
    description="CDS VizieR client (query large table)",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    keywords='astronomy',
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: BSD License 2.0",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
#    package_data={'cdspyreadme': ['*.template']},
#    include_package_data=True,
    python_requires='>=3.6',
    install_requires=['astropy>=3.2',
                      'numpy>=1.17.2'
                     ],
)

