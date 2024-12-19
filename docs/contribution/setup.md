# __Getting Started__

To contribute to fits2db, follow these steps:

1. Fork the repository by clicking "Fork" on the top right of this page.
2. Clone your fork to your local machine
3. Set up your local development environment. 

## Docs setup
```bash
pip install -r mkdocs-requirements.txt
pip install fits2db
```

## pytest setup 
In the root folder and run 
```bash
pip install -r test-requirements.txt
```

## Docker setup
For the docker setup you can follow these steps:

- Open your terminal where you have docker 
- Change to the folder `tests/integration/mysql` (for mysql tests)
- Run in the terminal 
    ```bash
    docker-compose up -d # This starts a mysql database for testing
    ```



