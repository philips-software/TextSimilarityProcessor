import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="similarity_processor",
    version="0.0.1",
    author="Brijesh",
    author_email="brijesh.krishnank@philips.com",
    description="Text Similarity Index Processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bkk003/text_de_duplication_monitoring",
    # packages=setuptools.find_packages(exclude=['test', '*.test', '*.test.*']),
    packages=setuptools.find_packages(include=['similarity_processor'], exclude=['test', '*.test', '*.test.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.6',
)