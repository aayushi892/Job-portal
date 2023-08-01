import sqlite3
import getpass

# Connect to the database
conn = sqlite3.connect('job_matching.db')
c = conn.cursor()

# Create a table for users if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              email TEXT NOT NULL UNIQUE,
              password TEXT NOT NULL)''')
conn.commit()

# Create a table for jobs if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS jobs
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              company TEXT NOT NULL,
              
              salary TEXT NOT NULL)''')
conn.commit()

# Define a function to sign up a new user
def sign_up():
    name = input('Enter your full name: ')
    email = input('Enter your email address: ')
    password = getpass.getpass('Enter a password: ')
    # Check if the email is already registered
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    if c.fetchone() is not None:
        print('This email is already registered.')
    else:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        print('Account created successfully!')

# Define a function to log in an existing user
def log_in():
    email = input('Enter your email address: ')
    password = getpass.getpass('Enter your password: ')
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    if user is None:
        print('Incorrect email or password.')
    else:
        print('Welcome back, {}!'.format(user[1]))

# Define a function to search for jobs by title or keyword
def search_jobs():
    keyword = input('Enter a job title or keyword: ')
    c.execute("SELECT * FROM jobs WHERE title LIKE ? OR company LIKE ?", ('%{}%'.format(keyword), '%{}%'.format(keyword), '%{}%'.format(keyword)))
    results = c.fetchall()
    if len(results) == 0:
        print('No results found.')
    else:
        print('Results:')
        for i, job in enumerate(results):
            print('{}. {} - {} - {} - {}'.format(i+1, job[1], job[2], job[3], job[4]))
        choice = input('Please select a job (1-{}): '.format(len(results)))
        try:
            choice = int(choice)
            if choice < 1 or choice > len(results):
                raise ValueError
            else:
                job = results[choice-1]
                print('Job details:')
                print('Title: {}'.format(job[1]))
                print('Company: {}'.format(job[2]))
            
                print('Salary: {}'.format(job[4]))
                apply_choice = input('Apply for this job? (Y/N): ')
                if apply_choice.upper() == 'Y':
                    print('Application submitted successfully!')
                else:
                    print('Application canceled.')
        except ValueError:
            print('Invalid input.')
        
            

# Define a function to view recommended jobs
def view_recommended_jobs():
    print("Recommended jobs for you: ")
    c.execute("SELECT *FROM jobs ORDER BY RANDOM() LIMIT 3")
    results = c.fetchall()
    if len(results) == 0:
        print("No recommended jobs found.")
    else:
        for i, job in enumerate(results):
            print('{} . {} - {} - {}'. format(i+1, job[1], job[3], job[4]))
            choice = input('Apply for a job? (Y/N):')
        if choice.upper() == 'Y':
            print('Application submitted successfully!')
        else:
            print('No applications submitted.')



def post_job():
    title = input('Enter the job title:')
    company = input('Enter the company name:')
    location = input('Enter th e job location :')
    salary = input('Enter the job salary:')
    c.execute("INSERT INTO JOBS(title, company, location, salary)VALUES (?,?,?,?)",(title, company, location, salary))
    conn.commit()
    print('Job posted successfully!')


def log_out():
    print('Logged out successfully!')
    global current_user
    current_user = None


def delete_job():
    job_id = input('Enter the ID of the jobs to delete : ')
    c.execute("DELETE FROM jobs WHERE id=?", (job_id))
    conn.commit()
    print('Job deleted successfully!')


def display_menu():
    print('''Welcome to Job matching!
          1.Sign up
          2.Log-in
          3.Seach for jobs
          4.View recommended jobs
          5.Post a job
          6.Log-out
          7.Delete a job posting
          8.Exit''')

    

current_user = None
while True:
    display_menu()
    choice = input('Enter your choice: ')
    if choice == '1':
        sign_up()
    elif choice == '2':
        log_in()
    elif choice == '3':
        search_jobs()
    elif choice == '4':
        view_recommended_jobs()
    elif choice == '5':
        post_job()
    elif choice == '6':
        log_out()
    elif choice == '7':
        delete_job()
    elif choice == '8':
        print('Goodbye!')


    break
else:
    print('Invalid input. Please try again.')
conn.close()

def main():
    while True:
        print('----------------------------------')
        print('Welcome to the Job Matching Platform')
        print('----------------------------------')
        print('1. Sign up')
        print('2. Log in')
        print('3. Search for jobs')
        print('4. View recommended jobs')
        print('5. Exit')
        choice = input('Please select an option (1-5): ')
        if choice == '1':
            sign_up()
        elif choice == '2':
            log_in()
        elif choice == '3':
            search_jobs()
        elif choice == '4':
            view_recommended_jobs()
        elif choice == '5':
            print('Thank you for using the Job Matching Platform. Goodbye!')
            break
        else:
            print('Invalid input. Please try again.')

conn.close()