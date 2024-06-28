# BlackJack Game

- BlackJack game under development. Originated as a side project to learn more about game development and PySide.

- To run the files, ensure that you have **poetry** installed to download all the right dependencies under the **pyproject.toml** file.

- Run ```pip install poetry``` to install poetry in your machine, and then **inside of the blackjack proeject package**, run ```poetry install``` to install the right dependencies and right Python Version.

- The **pyproject.toml** file will create a **virtual env**, that you need to select in your IDE to be able to run the code and game. Usually , it will create the virtual env on the following Windows path:
```C:\Users\your_user\AppData\Local\pypoetry\Cache\virtualenvs``` and on MacOS: ```/Users/your_user/Library/Caches/pypoetry/virtualenvs```, then select the wright environment created in the step before. (Change **your_user** for your user name).

- If you want to use this repository to learn, or help in the development, use the ```pip install pre-commit``` for crosschecking files before pushing to the repository. After doing the **pip install**, do ```pre-commit install```, and to run the pre-commit checks, do ```pre-commit run --argument```.

- Before commiting, the pre-commit will check the files in order to format, you will need to install flake8 by doing ```pip install flake8```.

- You can check more about the pre-commit hooks on: [https://github.com/pre-commit/pre-commit-hooks].

- To run the game, you can do the command ```python src/main.py``` or ```python ./src/main.py``` or simple run the ```main.py``` file on your IDE.
