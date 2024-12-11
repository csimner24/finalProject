#This is the main module of my program for the final project, it imports tasks_module.py which in turn imports task_module. > Cole Simner
import argparse
import tasks_module as s


def main():
    """ All the real work driving the program!"""
    parser = argparse.ArgumentParser(description= "update the task list.")
    parser.add_argument('--add', type= str, required= False, help= "add one task to your list by passing in an alphanumeric name.")
    parser.add_argument('--list', action='store_true', required= False, help="list all tasks that have not been completed, by due date then priority.")
    parser.add_argument('--report', action='store_true', required= False, help="list all tasks that have not been completed, by due date then priority.")
    parser.add_argument('--done', type= str, required= False, help= "the unique ID of the task you want to mark 'complete.'")
    parser.add_argument('--delete', type= str, required= False, help= "the unique ID of the task you want to remove from the list.")
    parser.add_argument('--query', type=str, required= False, nargs="+", help="input a series of string-search to find key terms in task names")
    parser.add_argument('--due', type=str, required= False, help="the due date in MM/DD/YYYY format.")
    parser.add_argument('--priority', type= int, required= False, help="the priority of a task; the default is 1")
    parser.add_argument('--id', type= str, required= False, help= "the unique ID of the task you want to update.")


    args = parser.parse_args()

    task_list = s.Tasks()
    
    #for task in task_list.tasks:
    #    print(task)

    if args.add:
        task_priority = args.priority if args.priority is not None else 1
        new_task = task_list.add_tasks(name=args.add, priority=task_priority, due_date=args.due)
        task_list.tasks.append(new_task)
        print(f"Created task {new_task.unique_id}")
        task_list.pickle_tasks()
        return
    
    elif args.list:
        sorted_incomplete_tasks = task_list.display_list()
        print(f"{'ID':<10} {'Age':<5} {'Due Date':<12} {'Priority':<10} {'Task':<25}")
        print(f"{'-' * 8}   {'-' * 3}   {'-' * 10}   {'-' * 8}   {'-' * 4}")
        
        for task in sorted_incomplete_tasks:
            age_str = f"{task.age}d" if task.age is not None else "0d"
            due_date_str = task.due_date if task.due_date else "-"
            print(f"{task.unique_id:<10} {age_str:<5} {due_date_str:<12}  {task.priority:<9} {task.name:<25}")
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
            print(f"Completed task ID {args.done}")
            return
        else:
            print(f"Could not identity task ID {args.done}")
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
    
    elif args.due:
        modify_due = task_list.update_due_date(task_id=args.id, due_date=args.due)
        if modify_due == True:
            print(f"Successfully updated task ID {args.id} to the due date {args.due}.")
            return
        else:
            print(f"Either the task ID {args.id} does not exist or {args.due} is invalid, so nothing was modified.")
            return
    
    elif args.priority:
        modify_priority = task_list.update_priority(task_id=args.id, new_priority=args.priority)
        if modify_priority == True:
            print(f"Successfully updated task ID {args.id} to the priority {args.priority}")
            return
        else:
            print(f"Either the task ID {args.id} does not exist or {args.priority} is invalid, so nothing was modified.")
            return

    else:
        print("You did not call a valid operation, try -h for a list of valid operations")

if __name__ == "__main__":
    main()