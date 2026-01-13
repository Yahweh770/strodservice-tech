#!/bin/bash
# Script to install dependencies from vendor directory

echo "Installing Node.js dependencies from vendor..."
if [ -d "./vendor/node_modules" ]; then
  # Create symbolic links to vendor node_modules
  rm -rf node_modules
  ln -sf ../vendor/node_modules ./
  echo "Created symlink to vendor node_modules"
else
  echo "Vendor node_modules directory not found"
fi

for dir in electron-app desktop-app src/frontend; do
  if [ -d "$dir" ]; then
    cd $dir
    if [ -d "../vendor/node_modules" ]; then
      rm -rf node_modules
      ln -sf ../../vendor/node_modules ./
      echo "Created symlink to vendor node_modules in $dir"
    fi
    cd ../
  fi
done

echo "Installing Python dependencies from vendor..."
pip install --find-links ./vendor/python_packages -r requirements.txt --no-index

echo "Installation from vendor completed!"