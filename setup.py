from setuptools import setup, find_packages

setup(
    name='SentimentFlow',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'spacy',
        'tqdm',
        'numpy',
        'pandas',
        'scipy',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for processing and analyzing sentiment flow in texts using principles from fluid dynamics.",
    url="https://github.com/dpicca/sentimentflow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
