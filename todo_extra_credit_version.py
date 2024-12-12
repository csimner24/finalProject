
#This is the extra credit for Cole Simner's final, it packages all the functionality in one file that can be executed

from datetime import datetime #import necessary packages
import sys
import random
import string
import re
import pickle
from datetime import datetime
import argparse
import os
home_dir = os.path.expanduser("~")
pickle_file_path = os.path.join(home_dir, ".todo.pickle")

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


class Tasks:
    """This class is used to create a list of task objects. It is initialized with an empty list and attempts to read existing task/todo objects from a pickle file. 
        This class has a series of methods used to interact with objects include handling a pickle file, adding tasks, listing existing-noncomplete tasks, querying the task list for names/descriptions that match a series of key words in a list,
        marking a task as done, removing a task from the list, creating a full report of the last list, and updating the priority and due date of a task."""
    def __init__(self):
        """Read pickled tasks file into a list."""
        self.tasks = [] #initialize with an empty list of tasks, this is used to create an instance of the Tasks class. 
        self.tasks = self.pickle_read() #read from the existing tasks file and update the task list
    
    def pickle_read(self):
        """Read existing tasks from a pickle file if the pickle file exists, or leave the task list empty if the file does not exist and this there are no tasks."""
        try:
            with open(pickle_file_path, "rb") as file: #loads a hidden file called 'todo' with the file type 'pickle'
                self.tasks = pickle.load(file)
        except FileNotFoundError: #accounts for a non existent task list at the begining
            self.tasks = []
        except Exception as e:
            print(f"Error while loading tasks: {e}")
        return self.tasks #return the list of tasks to the initalizer

    def pickle_tasks(self):
        """Write a list of task objects to a pickle file"""
        try:
            with open(pickle_file_path, "wb") as file: #this will overwrite the file every time it is called
                pickle.dump(self.tasks, file)
        except Exception as e:
            print(f"Error while saving tasks: {e}")
    
    def add_tasks(self, name, priority=1, due_date= None): #set default parameters for a task including priority and due date
        """This method is used to create a task, it inherets functionality from the Task class and returns the task object created, with applicable validation applied."""
        name = name.strip()
        task = Task(name, priority, due_date)
        return task
    
    def display_list(self):
        """This method is used for the list operation, it calculates the age of noncomplete tasks and sorts the noncomplete tasks by date and then priority. It returns a sorted list that only includes non-completed tasks."""
        incomplete_tasks = []
        for task in self.tasks:
            if task.completed is None:
                current_date = datetime.now()
                created_date = datetime.strptime(task.created, "%m/%d/%Y") #use the date when a task was created and apply formatting for date math
                age = (current_date - created_date).days #create the age of a task based on the days since creation
                task.age = age
                incomplete_tasks.append(task)
        
        sorted_incomplete_tasks = sorted(incomplete_tasks, #sorts the tasks bt date
                                         key=lambda task: (datetime.strptime(task.due_date, "%m/%d/%Y") if task.due_date #uses a lambda function to avoid a seperate function for sorting logic
                                                           else datetime.max, task.priority))
        return sorted_incomplete_tasks
    
    def list_query(self, search):#takes a list of strings as query terms 
        """This method is used to enable the search functionality of the Tasks class. It sacrifices poor runtime (O(N^3)) for highly effective substring search that handles case sensitivity.
            I made this decision since the task list should never be more than a dozen or so objects, no one would have a todo list with a million tasks. The method returns the tasks that match the query. """
        task_word_sets = [] #initialize an empty list for tasks and their sub words

        for task in self.tasks:  # Loop over all tasks (N tasks)
            if task.completed is None:
                task_name_cleaned = re.sub(r"[^\w\s]", "", task.name.lower())  # Removes punctuation and split by space, enables case insenstive substring matching
                task_words = set(task_name_cleaned.split())  # makes a unique set of words for fastser search
                task_word_sets.append((task, task_words)) #append the task and words to the list
    
        matching_tasks = [] #initailize an empty list for matching tasks
        query_terms = set(term.strip().lower() for term in search)  # Preprocess query terms to reduce complexity (O(n))

        for task, task_words in task_word_sets:  # Loop over all tasks (N tasks)
            if any(any(term in word for term in query_terms) for word in task_words):  # O(N^2) for the set size and number of workds per task > Check for substring match in the task words
               matching_tasks.append(task) #append a task with a matching word
        #The operation above ^ is O(N^3) runtime

        final_tasks = []
        for task in matching_tasks:
            current_date = datetime.now()
            created_date = datetime.strptime(task.created, "%m/%d/%Y")
            age = (current_date - created_date).days #create the age of all tasks that yielded a match with the query terms
            task.age = age
            final_tasks.append(task)
        
        return final_tasks #return the matching tasks for the query with the task age
    
    def list_done(self, task_id):
        """This is a docstring for the done functionality that updates the 'completed' field of a task. It takes a task's unqiue ID and verifies that the task item exists,
            then it generates a completed timestamp in a MM/DD/YYYY format as well as a longer format for the report display. It does not use the Task __validate_completed method since the 
            completion date is abstracted from the user. A child attribute called Raw Completed is also created which is used in the UI. 
            The method returns True or False based on if the unique ID match can be found. """
        task_id = task_id.replace(" ", "").strip()
        for task in self.tasks:
            if task.unique_id == task_id: #check for an ID match
                current_date = datetime.now()
                formatted_date = current_date.strftime("%m/%d/%Y") #use the current, running date to create a formatted completion date
                raw_time = current_date.strftime('%a %b %d %H:%M:%S CST %Y')
                task.completed = formatted_date #set the date completed
                task.raw_completed = raw_time
                self.pickle_tasks() #update the todo list by dumping our updated task to the pickle file. 
                return True
        else:
            return False #if the task ID could not be found, return false      
    
    def list_delete(self, task_id):
        """This method functions to remove a task from the task list, it matches the ID specified, removes the task from the list, and rewrites the todo list. It returns True or False depending on if the deletion suceeds."""
        task_id = task_id.replace(" ", "").strip() #prevent errors from spaces at the front, end, or in between
        for task in self.tasks:
            if task.unique_id == task_id: #check for an ID match
                self.tasks.remove(task) #access the tasks list and remove the task from the list
                self.pickle_tasks() #update the file
                return True #return true if the operation succeeded.
        else:
            return False
        
    
    def list_report(self):
        """This method is used to create a report of all complete and non complete tasks. It calculates the age of all tasks from the current date.
            It applies the same sorting logic as the display_list() function and returns a sorted list of all the tasks."""
        all_tasks = []
        for task in self.tasks:
                current_date = datetime.now()
                created_date = datetime.strptime(task.created, "%m/%d/%Y")
                age = (current_date - created_date).days
                task.age = age
                all_tasks.append(task)
        
        all_tasks_sorted = sorted(all_tasks, #sorts the tasks by the closest due date and then by priority
                                         key=lambda task: (datetime.strptime(task.due_date, "%m/%d/%Y") if task.due_date #uses a lambda function to avoid a seperate function for sorting logic
                                                           else datetime.max, task.priority))
        
        return all_tasks_sorted
    
    def update_due_date(self, task_id, due_date): #pass in a task unique ID and due date
        """This method is used to update the date of an existing task. It takes a task ID and a valid date in MM/DD/YYYY and updates the task date if the unique ID exists. 
            The function returns True or False depending on if the unique ID exists"""
        task_id = task_id.replace(" ", "").strip() #prevent errors from strings with white space at the front or end or in between
        due_date = due_date.replace(" ", "").strip()
        for task in self.tasks:
            if task.unique_id == task_id:
                valid_date = task.validate_due_date(due_date) #use the Task class method to validate the provided date or return None
                if valid_date is not None: #if the date is valid, update the task date and overwrite the file
                    task.due_date = due_date
                    self.pickle_tasks() 
                    return True #return true if the unique ID was found
        else:
            return False
        
    def update_priority(self, task_id, new_priority):
        """This method is used to update the priority of an existing task. It takes a task ID and the requested priority, validates the priority, and then overwrites the task object if the user's choice is valid.
            If the user attempts to pass in an invalid priority like 9 then the priority will not be updated. The function returns True or False depending on if the task ID exists. """
        task_id = task_id.replace(" ", "").strip()
        for task in self.tasks:
            if task.unique_id == task_id: #identify a matching task ID
                check_priority = task.validate_priority(new_priority) #check to see if the proposed ID is valid
                if check_priority == new_priority: #if the proposed ID equals a valid ID...this prevents bad requests from updating the priority to 1
                    task.priority = new_priority #update the priority of the task
                    self.pickle_tasks() #save the task to the todo pickle file
                    return True
        else:
            return False
        

def main():
    """ All the real work driving the program!"""
    parser = argparse.ArgumentParser(description= "update the task list using a variety of commands such as --add, --done, --due, and --priority; where --due and --priority must include '--id'.")
    
    parser.add_argument('--add', type= str, required= False, help= "add one task to your list by passing in a name that contains alphabet characters; takes a string and optional arguments --priority and --due.")
    
    parser.add_argument('--list', action='store_true', required= False, help="list all tasks that have not been completed, by due date then priority.")
    
    parser.add_argument('--report', action='store_true', required= False, help="list all tasks regardless of completion, by due date then priority.")
    
    parser.add_argument('--done', type= str, required= False, help= "the unique ID of the task you want to mark 'complete.'; takes one argument which is the unique ID of the task")
    
    parser.add_argument('--delete', type= str, required= False, help= "remove a task from the list; takes one argument which is the unique ID.")

    parser.add_argument('--query', type=str, required= False, nargs="+", help="searches for matching terms in the task 'name(s)'; takes a variable number of arguments seperated by 'quotes'")
    
    parser.add_argument('--due', type=str, required= False, help="the due date of a task in MM/DD/YYYY format.")
    parser.add_argument('--priority', type= str, required= False, help="the priority of a task; the default is 1") #use string type to improve error handling

    parser.add_argument('--id', type= str, required= False, help= "the unique ID of the task you want to modify with either a new priority or new due date; takes one argument which is the task unique ID as a string.")


    args = parser.parse_args() #assign all the arguments to a variable called args

    task_list = Tasks() #create an instance of the Tasks class


    #I thought about creating a task age here however not all parser arguments use age, therefore it is more efficent to create Age on an as need basis
    #Moreover, Age is a calculated field that updates over time, it needs to be recomputed every time a display command is called

    if args.add:
        task_priority = args.priority if args.priority is not None else "1"
        try:
            task_priority = task_priority.strip() #handles edge cases when the user passes priority as a string
            task_priority = int(task_priority) #covert the string to an integer
        except:
            task_priority = 1 #set the task priority to the default if an error is present with the user choice
        
        new_task = task_list.add_tasks(name=args.add, priority=task_priority, due_date=args.due)
        task_list.tasks.append(new_task)
        print(f"Created task {new_task.unique_id}")
        task_list.pickle_tasks() #save the task to the file immediately
        return #prevent more operations
    
    elif args.list:
        sorted_incomplete_tasks = task_list.display_list()
        print(f"{'ID':<10} {'Age':<5} {'Due Date':<12} {'Priority':<10} {'Task':<25}") #create padding for the data
        print(f"{'-' * 8}   {'-' * 3}   {'-' * 10}   {'-' * 8}   {'-' * 4}") #format the UI
        
        for task in sorted_incomplete_tasks:
            age_str = f"{task.age}d" if task.age is not None else "0d" #format the age according to the instructions
            due_date_str = task.due_date if task.due_date else "-" #format due date according to the instructions
            print(f"{task.unique_id:<10} {age_str:<5} {due_date_str:<12}  {task.priority:<9} {task.name:<25}") #apply padding for the object attributes
        return
    
    elif args.report:
        all_tasks_debugging = task_list.list_report()
        
        print(f"{'ID':<10} {'Age':<5} {'Due Date':<12} {'Priority':<10} {'Task':<25}    {'Created':<30} {'Completed':<30}")
        print(f"{'-' * 8}   {'-' * 3}   {'-' * 10}   {'-' * 8}   {'-' * 4}                         {'-' * 27}    {'-' * 27}")
    
        for task in all_tasks_debugging:
            # Format age, due date, and completed date with fallback values
            age_str = f"{task.age}d" if task.age is not None else "0d"
            due_date_str = task.due_date if task.due_date else "-"
            completed_str = task.raw_completed if hasattr(task, 'raw_completed') else "-"
        
            # Print task details with aligned columns
            print(f"{task.unique_id:<10} {age_str:<5} {due_date_str:<12}  {task.priority:<9} {task.name:<25}    {task.raw_created:<30} {completed_str:<30}")
        return
    
    elif args.done:
        successfully_updated = task_list.list_done(args.done)
        if successfully_updated == True:
            print(f"Completed task ID {args.done}") #format a print statement when the completed field is updated successfully
            return
        else:
            print(f"Could not identity task ID {args.done}") #format a print statement when the completed field is not updated
            return
    
    elif args.delete:
        successfully_deleted = task_list.list_delete(args.delete)
        if successfully_deleted == True:
            print(f"Deleted task ID {args.delete}")  
            return
        else:
            print(f"Could not identify task ID {args.delete}")
            return
    
    elif args.query: #I made a runtime tradeoff here with the justification of better search performance for worse runtime O(N^3) vs O(N)
        final_tasks = task_list.list_query(args.query)
        
        print(f"{'ID':<10} {'Age':<5} {'Due Date':<8}  {'Priority':<10}  {'Task':<1}")
        print(f"{'-' * 8}   {'-' * 3}\t{'-' * 10} {'-' * 8}    {'-' * 5}")
        
        for task in final_tasks:
            age_str = f"{task.age}d" if task.age is not None else "0d"
            due_date_str = task.due_date if task.due_date else "-"
            #print(f"{task.unique_id}\t{age_str}\t{task.due_date}\t{task.priority}\t{task.name}")
            print(f"{task.unique_id:<10} {age_str:<5} {due_date_str:<12} {task.priority:<8} {task.name:<1}")
        return
    
    elif args.due: #the --due command takes only one other argument besides due_date which is the task ID
        modify_due = task_list.update_due_date(task_id=args.id, due_date=args.due)
        if modify_due == True:
            print(f"Successfully updated task ID {args.id} to the due date {args.due}.")
            return
        else:
            print(f"Either the task ID {args.id} does not exist or {args.due} is invalid, so nothing was modified.")
            return
    
    elif args.priority: #the --priority command takes only one other argument besides priority which is the task ID
        try: #check the formatting of the user specified priority
            task_priority = args.priority
            task_priority = task_priority.strip()
            task_priority = int(task_priority)
        except:
            print("The priority provided could not be converted to an integer, try again.") 
            return #here we don't want anything to happen when the user passes a bad value so we exit the function
        modify_priority = task_list.update_priority(task_id=args.id, new_priority=task_priority)
        if modify_priority == True:
            print(f"Successfully updated task ID {args.id} to the priority {args.priority}")
            return
        else:
            print(f"Either the task ID {args.id} does not exist or {args.priority} is invalid, so nothing was modified.")
            return
    
    elif args.id: # concurrently using --id with --due and --priority will trigger the first of either --due or --priority
        #provide the user some information on the --id argument
        print("The --id command must be used with either '--due' or '--priority' to update the due date or priority of a specific task ID; passing both will only trigger the first command included")

    else:
        print("You did not call a valid operation, try -h for a list of valid operations") #print a statement when the file is run without a command to steer users
        print("")
        print("The following commands can be performed: ") #provide the user with a basic tutorial if no arguments are passed
        print("    Add a task with '--add'; takes 1 mandatory string argument and 2 optional arguments >> --add 'example name' --priority 3 --due 12/24/2024")
        print("    List all of the non complete commands; takes zero arguments >> --list")
        print("    List all of the non complete commands; takes zero arguments >> --list")
        print("    Complete a task with '--done'; takes 1 mandatory argument unique_ID >> --done 1234aBcD")
        print("    Remove a task with '--delete'; takes 1 mandatory argument unique_ID >> --delete 1234aBcD")
        print("    Search for terms in the non-completed task names; takes a variable number of arguments to search >> --query eggs milk bread 'hello world'")
        print("    Modify an existing task's due date with '--due'; takes 2 required arguments: the date and '--id {Task ID}' in either order >> --due 12/31/2024 --id 1234aBcD")
        print("    Modify an existing task's priority with '--priority'; takes 2 required arguments: the priority and '--id {Task ID}' in either order >> --priority 2 --id 1234aBcD")
        print("")
if __name__ == "__main__":
    main()




