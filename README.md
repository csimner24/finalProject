# finalProject

1. To use the executable version of this code, I created a file caled "todo_extra_credit_version.py" that has all the code in one file

2. I then installed pyinstaller >> pip install pyinstaller

3. I then navigated to my code directory

4. I added this code and changed the read and write functions to work with the pickle file:
>import os
>home_dir = os.path.expanduser("~")
> pickle_file_path = os.path.join(home_dir, ".todo.pickle")

5. I then ran "pyinstaller --onefile todo_extra_credit_version.py"
6. I pulled the Application file 'todo_extra_credit_version' from the dist folder

7. when I run my file from the command terminal, I can pass arguments to it and the functionality works