CONTRIBUTING GUIDELINE
========================


## Code Quality
Comply at much as possible with PEP8
IDE such as Pycharm provide a code inspection to perform a [5S](https://www.agilitest.com/cards/5s-on-code)

# Todos
The code embeds "_todo_" tags to improve features.
Tickets in Github are also an option - this is still in building mode

You are encouraged to contribute...

# Building a package
    
    .\venv\Scripts\python.exe setup.py bdist_wheel

Then apply https://www.freecodecamp.org/news/how-to-create-and-upload-your-first-python-package-to-pypi/

To deploy the package on Pypi.org

    .\venv\Scripts\python.exe -m twine upload .\dist\\mkTk_Widgets<version>.whl