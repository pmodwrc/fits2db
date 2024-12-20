# Testing the code
We doint aim for 100% code coverage to have 100%. But it is good to have the basics covered. Thus we use tests to check if the interfaces between the modules work as expected.


If you contribute new code it will run with unit-testing and if they are failing the code is not merged so please give it a run before opening a merge request :heart:

## Setup the testing environment 
To be sure the new code don't break something older please run the tests before comitting the code. If your code breaks the tests we have to reject the merge request. To run the tests the easy way is to use docker:

### pytest setup 
Change back to the root folder and run 
```bash
pip install -r test-requirements.txt
```

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

The tests of the base.py script are excluded in the github actions, but will run when pytest is called locally.

