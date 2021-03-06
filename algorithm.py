def powerset(s):
    '''This function takes a set as input and then makes a powerset of it. The powerset of a set is a set whose elements are all the subsets of the given set s.'''
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

def algorithm(tasks, total_time):
    '''tasks is a dictionary with all the info about the given tasks including the task name as a key,the task importance and the duration. total_time is the total amount of time that one will study for. tasks input of the form of a dictionary
    {"task name":[duration, importance]}
    '''
    task_counter = 1  # count how many tasks there are

    task_s = set(tasks.keys())
    #task_perms is the name of the permutations of the tasks
    task_perms = list(powerset(task_s))

    #perms time is the total time for each possible permutation.
    #perms importance the total importance of each possible perms_importance
    perms_time = []
    perms_importance = []

    #Find the time and importance of each possible set of tasks
    for i in range(len(task_perms)):
        t = 0
        importance = 0
        for j in range(len(task_perms[i])):
            t += tasks[task_perms[i][j]][0]
            importance += tasks[task_perms[i][j]][1]
        perms_time.append(t)
        perms_importance.append(importance)

    #this just a very common maximizing algorithm
    #basically for loops search for largest importance which is also less than the time limit

    current_plan = ""
    current_max = 0

    for i in range(len(perms_time)):
        #check if less than time limit
        if perms_time[i] <= total_time:
            #check if current importance is more than the maximum we found.
            if perms_importance[i] > current_max:
                #If more important we update the max
                current_max = perms_importance[i]
                current_plan = task_perms[i]
    #return the best plan
    return [*current_plan]

def check_int(h, full):
    '''Check if the information provided in the textboxes are integers where it needs to be integers.'''
    is_int = True
    for i in range(len(h)//4):
        if not (full[h[4*i+1]].isdigit() and full[h[4*i+2]].isdigit() and full[h[4*i+3]].isdigit()):
            is_int=False
    return is_int
