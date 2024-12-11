#This mopdule contains my Task class for the final project > Cole Simner
from datetime import datetime #import necessary packages
import sys
import random
import string
import re

class Task: #This class a worst case runtime of O(n) for a strip() operation performed in __validate_name, otherwise runtime is constant
    """Representation of a task, the following attributes and private/public methods are used to create task objects for a todo list. 
  
    Attributes:
              - created - the date at which a task was created, displayed as MM/DD/YYYY and created automatically
              - raw_created - the datetime at which a task was created, used for date math and other displays, displayed as Day Month Date hour:minute:second timezone year(YYYY), created automatically
              - completed - the date that a task was completed, this is optional and defined as MM/DD/YYYY, defaults to None
              - name - the name or description of a task, held as a string
              - unique id - the unique ID of a task, this is created automatically
              - priority - the priority of a task between integer values of 1, 2, or 3; 1 is default value and does not need to be defined
              - due date - the due date for a task, this is optional and defined as MM/DD/YYYY, defaults to None
    """
    def __init__(self, name, priority= 1, due_date= None, completed= None): #set defaults for priority, due date, and completion date at initialization
        self.name = name
        self.name = self.__validate_name(name) #validate name with a private function
        if self.name is None:
            print("There was an error with creating your task. Name must be a non-blank, non-numeric value.")
            sys.exit() #exit the initialization since there is an error
        self.created = self.__create_date()
        self.raw_created = self.__raw_create_date() #this is a private method since the user should never access this function but the value is accessible
        self.completed = self.__validate_completed(completed) #performs error handling if there is input passed, accounts for the default valye
        self.unique_id = self.__create_unique_id()
        self.priority = self.validate_priority(priority) #this is a method that must be accessible when the priority of a task changes
        self.due_date = self.validate_due_date(due_date) #this is a method that must be accessible when the priority of a task changes

    def __str__(self): #allows the user to print a task object
        """Return a string representation of the Task object with all the fields above."""
        return f"Name: {self.name}, Created: '{self.created}', Completed: {self.completed}, Task ID: {self.unique_id}, Priority: {self.priority}, Due Date: {self.due_date}, Raw Creation Date: {self.raw_created}"
    
    def __create_date(self):
        """This is a private method used to create the date value for the 'created' attribute. It returns a string."""
        current = datetime.now() #get the current time

        formatted_date = current.strftime("%m/%d/%Y") #format the time according to MM/DD/YYYY

        return formatted_date
    
    def __raw_create_date(self):
        """This is a private method used to create the raw date value for a special attribute uses to sort dates. It returns a string."""
        current = datetime.now()

        formatted_time = current.strftime('%a %b %d %H:%M:%S CST %Y') #format the date according to the interface defined in the assignment

        return formatted_time
    
    def __create_unique_id(self):
        """This is a private method used to create the unique ID attribute for a Task. It generates 3 random numbers and 2 random letters and returns a concatenated string representing a unique ID."""
        #this generates 73 billion possible combinations with 4 digits 0-9, and 4 letters which can be a-zA-Z
        random_digits = ''.join(random.choices(string.digits, k=4)) #generate four random numbers
        random_letter = ''.join(random.choices(string.ascii_letters, k=4)) #generate four random letters either lowercase or uppercase
        unique_id = random_digits + random_letter #concatenate all random values
        return unique_id
    
    def __validate_date(self, date_value):
        """This is a private method to validate if a date string is in MM/DD/YYYY format. It returns true or false based on if the date is valid."""
        try:
            datetime.strptime(date_value, "%m/%d/%Y") #uses a python package to determine if a user defined value is valid, prevents 19/12/2024, 12/45/2024, and 12/31/24 from being valid vased on the pattern
            return True
        except:
            return False
        
    def __validate_name(self, name):
        """This is a private method used to validate the name attribute or set the default value to None. It returns either a string task name or None."""
        name_check = name.strip() #remove whitespace from around the name ----> this is the worst runtime of this class at O(n)
        if len(name_check) == 0: #ensure the name is not blank
            return None #returns none if there is an issue, this is used for further validation
        elif not re.search(r'[a-zA-Z]', name_check): #makes sure that the name has some alphabet characters, numbers are allowed
            return None
        elif len(name_check) > 25: 
            name_check = name_check[:25] #truncates any task length longer than 25, this is important for formatting in the display
            return name_check
        else:
            return name_check
        
    def __validate_completed(self, completed):
        """This is a private method used to validate the completed attribute or set the default value to None. It returns either a formatted date or None."""
        if completed is None: #accounts for the default value of None
            return None
        else:
            if self.__validate_date(completed): #validates that a user defined completion date as valid
                return completed
            else:
                print(f"You did not enter a correct completion date, you must use MM/DD/YYYY format, the default will be None.") #When an error occurs, defaut the value back to None and display a message
                return None #leave the default set to none
            
    def validate_due_date(self, due_date):
        """This is a private method used to validate the due date attribute or set the default value to None. It returns either a formatted date or None."""
        if due_date is None: #account for a default value of None and return None
            return None
        else:
            if self.__validate_date(due_date): #validates a user defined due date as valid
                return due_date
            else:
                print("You did not enter a correct due date, you must use MM/DD/YYYY format, the default will revert to None.")
                return None #When an error occurs, defaut the value back to None and display a message
    
    def validate_priority(self, priority):
        """This is a private method used to validate the user defined priority attribute or set the default value to 1. It returns the integers 1, 2, or 3."""
        if isinstance(priority, int): #ensure that the value being passed is an integer
            if priority == 1:
                return 1
            elif priority == 2:
                return 2
            elif priority == 3:
                return 3
            else:
                print("Please enter priority as an integer of either 1, 2, or 3. The default will be set to 1.")
                return 1
        else: #if the user attempts to define a priority that is not valid for any reason, set the default to 1
            print("Please enter priority as an integer of either 1, 2, or 3. The default will be set to 1.")
            return 1

if __name__ == "__main__": #below are a few objects of the Task class
    start = Task("hello")
    print(start)
    make_complete = Task("its done", completed= "12/31/2024")
    print(make_complete)
    due_today = Task("its due now", due_date= "12/11/2024", priority= 2) #exmple of a task with different defined attributes
    print(due_today)



