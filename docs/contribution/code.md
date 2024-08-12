# Contribute to the code

## Getting Started
To build the package and install the requirements you can run in the root directory
```bash
pip install .
```

## Setup the testing environment 
To be sure the new code don't break something older please run the tests before comitting the code. If your code breaks the tests we have to reject the merge request. To run the tests the easy way is to use docker:

### Docker setup
For the docker setup you can follow these steps:

- Open your terminal where you have docker 
- Change to the folder `tests/integration/mysql` (for mysql tests)
- Run in the terminal 
    ```bash
    docker-compose up -d # This starts a mysql database for testing
    ```
### Run tests
Change back to the root folder and run 
```bash
pytest
```
this will collect all tests. If you want to have some information about code coverage run 
```bash
coverage run -m pytest
```
to show the results you can run either of these 
=== "Terminal"

    ```bash
    coverage report
    ```

=== "Detailed html"

    ```bash
    coverage html
    ```


