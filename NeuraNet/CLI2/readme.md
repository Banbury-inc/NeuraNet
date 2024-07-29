This is a CLI tool for Banbury Cloud. 


In order to update the CLI tool:

python setup.py sdist bdist_wheel
pip install .

In order to uninstall the CLI tool:

pip uninstall bcloud



In order to create a debain package:

mkdir DEBIAN
nvim DEBIAN/control

control file:

Package: your-cli-tool
Version: 1.0
Architecture: all  # Use "all" for architecture-independent packages
Maintainer: Your Name <your@email.com>
Description: Your CLI Tool Description
Section: utils  # Choose an appropriate section
Priority: optional


This will create a deb file

fpm -s python -t deb .








# Instructions for macos installation
In the dist directory with executable:

sudo mv dist/bcloud /usr/local/binbcloud 

sudo chmod +x /usr/local/bin/bcloud


bcloud


the command "cli" works... close enough for now... 
