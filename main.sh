#!/bin/bash

set -e

display_help() {
    echo ""
    echo "Usage: $0 [--help] [--skip-install] <npm-command>"
    echo ""
    echo "Available commands:"
    echo " dev - Start development server (React and Electron)"
    echo " dev:electron - Start development server for Electron"
    echo " dev:react - Start development server for React"
    echo " build - Build production bundles (React and Electron)"
    echo " build:run - Build production bundles and run Electron app"
    echo " build:electron- Build production bundle for Electron"
    echo " build:react - Build production bundle for React"
    echo " package - Build production bundles and create distributable package"
    echo ""
    echo "Options:"
    echo " --help - Display this help message"
    echo " --skip-install - Skip installation of Python and npm dependencies"
    echo ""
}

if [ "$1" == "--help" ]; then
    display_help
    exit 0
fi

skip_install=false
if [ "$1" == "--skip-install" ]; then
    skip_install=true
    shift
fi

cd NeuraNet/frontend

# Checking if virtualenv is installed
# if not, it installs it
if ! command -v virtualenv &> /dev/null; then
    echo "virtualenv is not installed. Installing virtualenv..."
    python3 -m pip install --user virtualenv
fi

# Creating virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    virtualenv venv
fi

# Activating virtual environment only if it's not already activated
if [ -z "$VIRTUAL_ENV" ]; then
    source venv/bin/activate
fi

# Skipping installation of dependencies
# if the --skip-install flag is provided
if ! $skip_install; then
    pip install -r requirements.txt
    npm install --legacy-peer-deps
fi

if [ -z "$1" ]; then
    display_help
else
    npm run "$1"
fi