from Task import Task
 
class TimeTable:
    def __init__(self, start_time=None, finish_time=None, list_tasks=None):
        self.start_time = start_time
        self.finish_time = finish_time
        self.list_tasks = list_tasks

    def clean(self):
        self.list_tasks = []

    def delete_task(self, name_of_task):
        self.list_tasks.remove(name_of_task)

    def add_task(self, name_of_task, importance, urgency, duration):
        task = Task(name_of_task, importance, urgency, duration)
        self.list_tasks.append(task)
