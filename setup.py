from setuptools import setup, find_packages

setup(
    name="modbuster",
    version="0.2.0",
    description="Busting ICS/SCADA over modbus",
    author="tacticalgator",
    url="https://github.com/tacticalgator/modbuster",
    packages=find_packages(),
    install_requires=[
        "pymodbus==3.6.9"
    ],
    entry_points={
        "console_scripts": [
            'modbuster=modbuster.modbuster:main',
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    license="GNU General Public License v3 (GPLv3)",
    keywords="modbus, ICS, SCADA, security, penetration-testing, pymodbus, red-team",
)
