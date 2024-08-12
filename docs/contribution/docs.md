# __Contributing to fits2db Documentation__


## Getting Started
Before you begin, make sure you have the necessary tools installed with :
```bash
pip install -r mkdocs-requirements.txt
pip install fits2db
```

## Contributing to the User guides
If you're only changing the user guide, tutorial, or any other non-code-related documentation:

1. Navigate to the docs directory where the Markdown files for the user guide and other documentation are located.
2. Make your changes or additions directly to the relevant Markdown (.md) files.
3. Test your changes locally to ensure everything looks correct:
```bash
mkdocs serve
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser to view the documentation site with your changes.

4. Commit the code and create an merge request

## __Contributing to the Code Documentation__
If you're contributing to the code documentation:

1. Follow the same steps to fork, clone, and set up the repository.
2. You will need to install fits2db from source to see your changes made to the cli docs
3. The code documentation is generated using mkdocstrings. To modify the documentation, Update the docstrings in your Python code following the project's conventions. Ensure that your docstrings are clear, concise, and make proper use of type annotations.
4. Reinstall the package and run the `mkdocs serve` command to check if changes look good before you create a merge request.


