#This mopdule contains my Tasks class for the final project > Cole Simner
import pickle
from datetime import datetime
import re
import task_module as t

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
            with open(".todo.pickle", "rb") as file: #loads a hidden file called 'todo' with the file type 'pickle'
                self.tasks = pickle.load(file)
        except FileNotFoundError: #accounts for a non existent task list at the begining
            self.tasks = []
        except Exception as e:
            print(f"Error while loading tasks: {e}")
        return self.tasks #return the list of tasks to the initalizer

    def pickle_tasks(self):
        """Write a list of task objects to a pickle file"""
        try:
            with open(".todo.pickle", "wb") as file: #this will overwrite the file every time it is called
                pickle.dump(self.tasks, file)
        except Exception as e:
            print(f"Error while saving tasks: {e}")
    
    def add_tasks(self, name, priority=1, due_date= None): #set default parameters for a task including priority and due date
        """This method is used to create a task, it inherets functionality from the Task class and returns the task object created, with applicable validation applied."""
        task = t.Task(name, priority, due_date)
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
            I made this decision since the task list should never be more than a dozen or so objects, no one would have a todo list in the millions. The method returns the tasks that match the query. """
        task_word_sets = [] #initialize an empty list for tasks and their sub words

        for task in self.tasks:  # Loop over all tasks (N tasks)
            if task.completed is None:
                task_name_cleaned = re.sub(r"[^\w\s]", "", task.name.lower())  # Removes punctuation and split by space, enables case insenstive substring matching
                task_words = set(task_name_cleaned.split())  # makes a unique set of words for fastser search
                task_word_sets.append((task, task_words)) #append the task and words to the list
    
        matching_tasks = [] #initailize an empty list for matching tasks
        query_terms = set(term.lower() for term in search)  # Preprocess query terms to reduce complexity (O(n))

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
        for task in self.tasks:
            if task.unique_id == task_id: #identify a matching task ID
                check_priority = task.validate_priority(new_priority) #check to see if the proposed ID is valid
                if check_priority == new_priority: #if the proposed ID equals a valid ID...this prevents bad requests from updating the priority to 1
                    task.priority = new_priority #update the priority of the task
                    self.pickle_tasks() #save the task to the todo pickle file
                    return True
        else:
            return False

