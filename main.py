#Title: Study Scheduler
#Authors: Alex Zhang and Kellen Sun

#imports from other files and flask.
from algorithm import algorithm, check_int
from flask import Flask, render_template, url_for, request, redirect

#global variables so that every function/html page can access them
full={}
alg_out=[]
dark_mode = False

#Create a flask instance
app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)


# Index page
#each routing function does about the same, we call the 3 global variables then return a rendered template while passing the variables to the appropriate html file
#for index the url ends with /, and we pass the index.html file.
@app.route('/')
def index():
  global full
  global alg_out
  global dark_mode
  return render_template('index.html', value = [full, alg_out, dark_mode])

# The page where the user can enter tasks and create new study sessions.
@app.route('/newstudysession')
def newstudysession():
    global dark_mode
    global full
    global alg_out
    return render_template('newstudysession.html', value=[full, alg_out, dark_mode])

@app.route('/plans', methods=["POST", "GET"])
def plans():
    global full
    global alg_out
    global dark_mode
    full=dict(request.form)
    #full is a dictionary of all the information from the textboxes, keys are the textbox names, values are the inputs as strings
    #full was to mean full amount of data
    #h takes a list of the keys except for the first 3
    #we take out the first 3 as they ruin a pattern that would make checking input boxes easier
    h=list(full.keys())[3:]
    #the if checks if all the ones that should be integers are actually integers before we do int() and break the website
    if check_int(h,full) and full["studytimeH"].isdigit() and full["studytimeM"].isdigit():
        t=int(full["studytimeH"])*60+int(full["studytimeM"])
        #t is the total amount of time to study for
        tasks={}
        #tasks is a dict of the tasks as the algorithm needs them, key is taskname, value is a 2 element list, time and importance
        #print(h)
        for i in range(1, 1+(len(h)//4)):
            j=str(i)
            #we take a str of our counter so that we can acess the task number by ID names
            tasks[full["task"+j]]=[int(full["DurationH"+j])*60+int(full["DurationM"+j]), int(full["Importance"+j])]
            #multilpy by 60 the hours then add t0 minutes
            #we need to int() everything for the algorithm to work
        # we pass tasks and t into the algorithm
        #when we render the html, we can pass 1 value. which is our algorithm output and 'full' which is all the data in case we need extra information

        alg_out=algorithm(tasks, t)
        #alg_out is what the algorithm outputs

        return render_template('plans.html',value=[alg_out, full, dark_mode])
    else:
        return redirect(url_for('newstudysession'))
    #return "<h1> "+str(algorithm(tasks,t))+" </h1>"

@app.route('/studying', methods=["POST", "GET"])
def studying():
    global full
    global alg_out
    global dark_mode
    #full is a global variable of all the information given in the form page
    print(full)
    print(alg_out)
    return render_template('studying.html',value=[alg_out, full,dark_mode])

#making the settings page
@app.route('/setting', methods=["POST", "GET"])
def settings():
    print(request.form)
    global dark_mode
    #if the settings page is reached from a button (namely the darkmode one)
    if request.method == 'POST':
        #then we flip the value of darkmode
        dark_mode= not dark_mode
    return render_template('setting.html',value=[alg_out, full, dark_mode])


if __name__ == '__main__':
  # Run the Flask app
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )