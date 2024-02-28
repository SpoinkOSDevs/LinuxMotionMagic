#!/bin/bash

APP_NAME="LinuxMotionMagic"
PYTHON_FILE="Core.py"
VERSION="8.26"  # Set your application version
MAINTAINER="Carl <spoinkosgithub@gmail.com>"  # Set your information

all() {
    setup
    build
    package
    clean
}

setup() {
    echo "Setting up the virtual environment and installing dependencies..."
    python3 -m venv venv
    . venv/bin/activate && pip install pyinstaller
    echo "Setup completed successfully!"
}

build() {
    echo "🛠️  Building the Python app..."
    # No need to use PyInstaller, we'll handle the file movement manually
}

package() {
    echo "📦  Creating distribution directory structure..."

    # Create directories
    mkdir -p dist/$APP_NAME
    mkdir -p dist/$APP_NAME/bin

    # Copy Python file
    cp $PYTHON_FILE dist/$APP_NAME/bin/

    # Optionally, copy additional resources
    # cp -r resources dist/$APP_NAME/

    echo "🎉  Distribution directory structure created successfully!"

    echo "📦  Creating the Debian package..."

    # Create the DEBIAN control file
    mkdir -p dist/DEBIAN
    cat <<EOF > dist/DEBIAN/control
Package: $APP_NAME
Version: $VERSION
Section: base
Priority: optional
Architecture: all
Maintainer: $MAINTAINER
Description: An Animation Application for Linux
EOF

    # Build the Debian package
    dpkg-deb --build dist

    echo "🎉  Debian package created successfully!"
}

clean() {
    echo "🧹  Cleaning up..."
    rm -rf build/ venv
}

# Execute the 'all' target
all
