
# fits2db installation guide
It is recommended to use a virtual environment when running this tool. Utilizing [`venv`](https://docs.python.org/3/library/venv.html) or [`conda`](https://www.anaconda.com/) ensures a clean and isolated environment, which is a best practice.

## Install from [`PYPI`](https://pypi.org/project/fits2db/)
For Versions <= 0.0.3 fits2db can be installed from PYPI. Newer Versions must be installed from source

!!! tip "You can use pip to install this library "
    ```bash 
    pip install fits2db
    ```
    or for specific version use 
    ```bash 
    pip install fits2db==<your_version> 
    ```


## Install from source
Clone this repo to your local machine. Once cloned navigate to the `root` directory of this project and run in your python environment 
!!! tip "Build install with pip install"
    ```bash 
    pip install .
    ```
With this the `fits2db` lib should be installed. You can test if its properly installed by running the version command to check if you got the right version
```bash title="cmd"
>fits2db --version
>>> fits2db, version 0.0.1
```

Alternatively it can be installed from git with 
```bash
pip install git+https://github.com/pmodwrc/fits2db.git@main
```
For this method a local [`git`](https://git-scm.com/downloads/win) client installation is required.

**Happy coding :sparkles:**



