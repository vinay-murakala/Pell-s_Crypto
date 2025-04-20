from setuptools import setup, find_packages

setup(
    name="Pell's_Crypto",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pycryptodome==3.22.0',
        'pytest==8.3.2',
        'flake8==7.1.1',
    ],
    author="Vinay Kumar Murakala",
    author_email="vinaymurakala001@gmail.com",
    description="A hybrid encryption app using Pell's equation and AES",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vinay_murakala/Pell's_Crypto",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
