import setuptools

with open('ReadMe.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="ElexonDataPortal", 
    version="1.0.0",
    author="Ayrton Bourn",
    author_email="AyrtonBourn@Outlook.com",
    description="Package for accessing the Elexon data portal API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AyrtonB/ElexonDataPortal",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'seaborn',
        'matplotlib',
        'requests',
        'xmltodict',
        'ipypb',
    ],
    package_data={'ElexonDataPortal':['*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)