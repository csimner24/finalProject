#This mopdule contains my Tasks class for the final project > Cole Simner
import pickle
from datetime import datetime
import re
import task_module as t

class Tasks:
    """A list of 'Task' objects."""
    def __init__(self):
        """Read pickled tasks file into a list."""
        self.tasks = []
        self.tasks = self.pickle_read()
    
    def pickle_read(self):
        """Read existing tasks from a pickle file if applicable."""
        try:
            with open(".todo.pickle", "rb") as file:
                self.tasks = pickle.load(file)
        except FileNotFoundError:
            self.tasks = []
        except Exception as e:
            print(f"Error while loading tasks: {e}")
        return self.tasks

    def pickle_tasks(self):
        """Write the list objects to a pickle file"""
        try:
            with open(".todo.pickle", "wb") as file:
                pickle.dump(self.tasks, file)
        except Exception as e:
            print(f"Error while saving tasks: {e}")
    
    def add_tasks(self, name, priority=1, due_date= None):
        """This method is used to create a task, it inherets functionality from the Task class and returns the  """
        task = t.Task(name, priority, due_date)
        return task
    
    def display_list(self):
        """This method is used for the list operation. """
        incomplete_tasks = []
        for task in self.tasks:
            if task.completed is None:
                current_date = datetime.now()
                created_date = datetime.strptime(task.created, "%m/%d/%Y")
                age = (current_date - created_date).days
                task.age = age
                incomplete_tasks.append(task)
        
        sorted_incomplete_tasks = sorted(incomplete_tasks, 
                                         key=lambda task: (datetime.strptime(task.due_date, "%m/%d/%Y") if task.due_date 
                                                           else datetime.max, task.priority))
        return sorted_incomplete_tasks
    
    def list_query(self, search):
        """This is a docstring for the query method"""
        task_word_sets = []

        for task in self.tasks:  # Loop over all tasks (N tasks)
            if task.completed is None:
            # Remove punctuation from task name and split by space
                task_name_cleaned = re.sub(r"[^\w\s]", "", task.name.lower())  # Removes punctuation
                task_words = set(task_name_cleaned.split())  # Split into words and make a set
                task_word_sets.append((task, task_words))
    
        matching_tasks = []
        query_terms = set(term.lower() for term in search)  # Preprocess query terms (O(M))

        # Check for matches (substring match)
        for task, task_words in task_word_sets:  # Loop over all tasks (N tasks)
            if any(any(term in word for term in query_terms) for word in task_words):  # Check for substring match
               matching_tasks.append(task)
        
        final_tasks = []
        for task in matching_tasks:
            current_date = datetime.now()
            created_date = datetime.strptime(task.created, "%m/%d/%Y")
            age = (current_date - created_date).days
            task.age = age
            final_tasks.append(task)
        
        return final_tasks
    
    def list_done(self, task_id):
        """This is a docstring for the done functionality that updates the 'completed' field of a task."""
        for task in self.tasks:
            if task.unique_id == task_id:
                current_date = datetime.now()
                formatted_date = current_date.strftime("%m/%d/%Y")
                raw_time = current_date.strftime('%a %b %d %H:%M:%S CST %Y')
                task.completed = formatted_date
                task.raw_completed = raw_time
                self.pickle_tasks()
                return True
        else:
            return False
        
                
    
    def list_delete(self, task_id):
        """This is a docstring for the delete functionality that deletes task."""
        for task in self.tasks:
            if task.unique_id == task_id:
                self.tasks.remove(task)
                self.pickle_tasks()
                return True
        else:
            return False
        
    
    def list_report(self):
        """This is a docstring for the Task report command"""
        all_tasks = []
        for task in self.tasks:
                current_date = datetime.now()
                created_date = datetime.strptime(task.created, "%m/%d/%Y")
                age = (current_date - created_date).days
                task.age = age
                all_tasks.append(task)
        
        sorted_tasks = sorted(all_tasks, key=lambda task: task.priority)
        
        return sorted_tasks
    
    def update_due_date(self, task_id, due_date):
        """This is a docstring"""
        for task in self.tasks:
            if task.unique_id == task_id:
                valid_date = task.validate_due_date(due_date)
                if valid_date is not None:
                    task.due_date = due_date
                    self.pickle_tasks()
                    return True
        else:
            return False
        
    def update_priority(self, task_id, new_priority):
        """This is a docstring"""
        for task in self.tasks:
            if task.unique_id == task_id:
                check_priority = task.validate_priority(new_priority)
                if check_priority == new_priority:
                    task.priority = new_priority
                    self.pickle_tasks()
                    return True
        else:
            return False

