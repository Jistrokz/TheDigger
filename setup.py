from setuptools import setup, find_packages


with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='raccoon-scanner',
    packages=find_packages(exclude="tests"),
    license="MIT",
    version='0.0.2',
    description='Red Team and Offensive Security Scanning and Reconnaisance Tool for Companies and Pentesters. ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Kartavya Trivedi',
    author_email='Kartavyatrivedi9@gmail.com',
    url='https://github.com/Jistrokz/TheDigger',
    install_requires=['beautifulsoup4',
                      'requests',
                      'dnspython',
                      "lxml",
                      "click",
                      "fake-useragent",
                      "requests[socks]",
                      "xmltodict"],
    package_data={
        "TheDigger_src": [
            "wordlists/*"
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'TheDigger=TheDigger_src.main:main'
        ]
    },
)
