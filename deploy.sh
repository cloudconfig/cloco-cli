# Clears the dist folder
echo "Clearing the dist folder"
rm -rf dist/*

# Build the wheel
echo "Building the wheel package"
python setup.py bdist_wheel --universal

# Register
WHEEL="dist/$(ls dist)"
echo "Registering package $WHEEL"
twine register $WHEEL

# Upload
echo "Uploading package $WHEEL"
twine upload dist/*
