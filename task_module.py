#This mopdule contains my Task class for the final project > Cole Simner
from datetime import datetime
import sys
import random
import string
import re

class Task:
    """Representation of a task
  
    Attributes:
              - created - date, displayed as MM/DD/YYYY
              - raw_created - datetime, the datetime stamp when a task was created
              - completed - date, this is optionally defined as MM/DD/YYYY
              - name - string
              - unique id - number, this is created automatically
              - priority - int value of 1, 2, or 3; 1 is default
              - due date - date, this is optional and defaults to None
    """
    def __init__(self, name, priority= 1, due_date= None, completed= None):
        self.name = name
        self.name = self.__validate_name(name)
        if self.name is None:
            print("There was an error with creating your task. Name must be a non-blank, non-numeric value.")
            sys.exit()
        self.created = self.__create_date()
        self.raw_created = self.__raw_create_date()
        self.completed = self.__validate_completed(completed) #This sets the default to None since the user won't set it right away, it performs error handling if there is a input passed
        self.unique_id = self.__create_unique_id()
        self.priority = self.validate_priority(priority)
        self.due_date = self.validate_due_date(due_date) #This sets the optional value of due date to None and performs error handling when a value is passed

    def __str__(self):
        """Return a string representation of the Task object."""
        return f"Name: {self.name}, Created: '{self.created}', Completed: {self.completed}, Task ID: {self.unique_id}, Priority: {self.priority}, Due Date: {self.due_date}"
    
    def __create_date(self):
        """This is a private method used to create the date value for the 'created' attribute. It returns a string."""
        current = datetime.now()

        formatted_date = current.strftime("%m/%d/%Y")

        return formatted_date
    
    def __raw_create_date(self):
        """This is a private method used to create the raw date value for a special attribute uses to sort dates. It returns a string."""
        current = datetime.now()

        formatted_time = current.strftime('%a %b %d %H:%M:%S CST %Y')

        return formatted_time
    
    def __create_unique_id(self):
        """This is a private method used to create the unique ID attribute for a Task. It generates 3 random numbers and 2 random letters and returns the concatenated string."""
        #this generates 73 billion possible combinations
        random_digits = ''.join(random.choices(string.digits, k=4)) #generate three random numbers
        random_letter = ''.join(random.choices(string.ascii_letters, k=4)) #generate 3 random letters
        unique_id = random_digits + random_letter
        return unique_id
    
    def __validate_date(self, date_value):
        """This is a private method to validate if a date string is in MM/DD/YYYY format."""
        try:
            datetime.strptime(date_value, "%m/%d/%Y")
            return True
        except:
            return False
        
    def __validate_name(self, name):
        """This is a private method used to validate the name attribute or set the default value to None. It returns either a string name or None."""
        name_check = name.strip()
        if len(name_check) == 0:
            return None
        elif not re.search(r'[a-zA-Z]', name_check):
            return None
        elif len(name_check) > 25:
            name_check = name_check[:25]
            return name_check
        else:
            return name.strip()
        
    def __validate_completed(self, completed):
        """This is a private method used to validate the completed attribute or set the default value to None. It returns either a formatted date or None."""
        if completed is None:
            return None
        else:
            if self.__validate_date(completed):
                return completed
            else:
                print(f"You did not enter a correct date in MM/DD/YYYY format.") #When an error occurs, defaut the value back to None and display a message
                return None 
            
    def validate_due_date(self, due_date):
        """This is a private method used to validate the completed attribute or set the default value to None. It returns either a formatted date or None."""
        if due_date is None:
            return None
        else:
            if self.__validate_date(due_date):
                return due_date
            else:
                print("You did not enter a correct date in MM/DD/YYYY format.")
                return None #When an error occurs, defaut the value back to None and display a message
    
    def validate_priority(self, priority):
        """This is a private method used to validate the priority attribute or set the default value to 1. It returns the integers 1, 2, or 3."""
        if priority == 1:
            return 1
        elif priority == 2:
            return 2
        elif priority == 3:
            return 3
        else:
            print("Please enter priority as an integer of either 1, 2, or 3. The default will be set to 1.")
            return 1

if __name__ == "__main__":
    start = Task("hello")
    print(start)
    make_complete = Task("its done", completed= "12/31/2024")
    print(make_complete)
    due_today = Task("its due now", due_date= "12/11/2024", priority= 2)
    print(due_today)



