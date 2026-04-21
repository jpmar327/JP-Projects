# PACKAGING GUIDE

This guide outlines the setup and distribution instructions for packaging a Python project using PyOxidizer.

## Prerequisites
- Ensure you have Python 3.7 or higher installed.
- Install PyOxidizer using `pip`:
  ```bash
  pip install pyoxidizer
  ```

## Creating a PyOxidizer Configuration
1. **Create a new directory** for your project if you haven't already:
   ```bash
   mkdir my_python_project
   cd my_python_project
   ```

2. **Generate a PyOxidizer configuration** file:
   ```bash
   pyoxidizer init
   ```
   This creates a `pyoxidizer.bzl` file which is the build configuration for your project.

## Building Your Executable
To create a standalone executable, use the following command:
```bash
pyoxidizer build
```
This command will generate a binary inside the `build` directory.

## Running the Executable
You can run the generated executable directly:
```bash
./build/my_python_project
```

## Customizing Your Build
You can customize your build by editing the `pyoxidizer.bzl` file. Refer to the [PyOxidizer documentation](https://pyoxidizer.readthedocs.io) for more detailed configuration options.

## Distribution
To distribute your application, simply share the contents of the `build` directory. You can also create an installer using tools like `pkg` or `Inno Setup` for Windows distributions.

## Additional Resources
- [PyOxidizer Documentation](https://pyoxidizer.readthedocs.io)
- [Python Packaging](https://packaging.python.org)

## Conclusion
Following these instructions, you will be able to package and distribute your Python project successfully using PyOxidizer.