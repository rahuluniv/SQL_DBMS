# import the sqlite3 module so that we can use it in our python code
import sqlite3
# matplotlib.pyplot will allow us to create visualizations of our results
import matplotlib.pyplot as plt

# define global variables for our database connection and cursor
# these will be accessible by and consistent across all methods
connection = None
cursor = None

# define method for connecting to database
def connect(path):
    # using global variables already defined in main method, not new variables
    global connection, cursor
    # create a connection to the sqlite3 database
    connection = sqlite3.connect(path)
    # create a cursor object which will be used to execute sql statements
    cursor = connection.cursor()
    # execute a sql statement to enforce foreign key constraint
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    # commit the changes we have made so they are visible by any other connections
    connection.commit()
    return

# define function for the first query
def query1():
    # using globally define dconnection and cursor
    global connection, cursor
    
    # define the sql query string with variables
    query = '''SELECT S.Year, SUM(M.Revenue)
    FROM MovieData M, StreamedMovies S
    WHERE M.Title = S.Title AND
    M.Revenue IS NOT NULL AND
    S.Netflix = :Nflag AND S.Hulu = :Hflag AND
    S.PrimeVideo = :Pflag AND S.Disney = :Dflag
    GROUP BY S.Year;'''
    
    # need to get four inputs from user corresponding to the four platforms
    print('Please enter 1 for yes, 0 for no')
    # will cast the input as integers
    n_flag = int(input('Include movies on Netflix?: '))
    h_flag = int(input('Include movies on Hulu?: '))
    p_flag = int(input('Include movies on PrimeVideo?: '))
    d_flag = int(input('Include movies on DisneyPlus?: '))
    
    # execute query with provided flags
    cursor.execute(query, {'Nflag': n_flag, 'Hflag': h_flag,
                           'Pflag': p_flag, 'Dflag': d_flag})
    
    # get list of tuples
    rows = cursor.fetchall()
    # need list of years and revenues for plotting pie chart
    years = []
    revenues = []
    # iterate through results to build lists
    for row in rows:
        years.append(row[0])
        revenues.append(row[1])
        
    # pass lists to plotting functions to generate and save charts
    pie_chart(revenues, years, 'Query 1 Pie Chart')
    bar_chart(revenues, years, 'Query 1 Bar Chart', 'Years', 'Total Revenue')
    connection.commit()
    
    return

# define function for the second query
def query2():
    # using globally define dconnection and cursor
    global connection, cursor
    
    # define the sql query string with variables
    query = '''SELECT S.Year, AVG(M.Rating) as avgrating
    FROM MovieData M, StreamedMovies S
    WHERE M.Title = S.Title AND
    M.Revenue IS NOT NULL AND
    S.Year BETWEEN :Year1 AND :Year2
    AND S.Netflix = 1
    GROUP BY S.Year;'''
    
    # need to get two inputs from user for year range
    print('Please enter the years for the range (inclusive) to use in query')
    print('First year should be less than second year')
    # will cast the input as integers
    year1 = int(input('Start year: '))
    year2 = int(input('End year: '))
    
    # execute query with provided years
    cursor.execute(query, {'Year1': year1, 'Year2': year2})
    
    # get list of tuples
    rows = cursor.fetchall()
    # need list of years and revenues for plotting pie chart
    years = []
    ratings = []
    # iterate through results to build lists
    for row in rows:
        years.append(row[0])
        ratings.append(row[1])
        
    # pass lists to plotting functions to generate and save charts
    bar_chart(ratings, years, 'Query 2 Bar Chart', 'Years', 'Average Rating')
    connection.commit()
    
    return

# define pie chart plotting function
# takes list of values and labels and title string
# saves pie chart to file
def pie_chart(values, labels, title):
    # see matplotlib website for more details
    # https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
    
    # if lists empty, print warning
    if len(values) < 1:
        print('Warning: empty input so generated plot will be empty')
        
    # create a pie chart
    plt.pie(values, # these are the values that will make up the pie slices
            labels=labels, # these are names/labels for each slice
            autopct='%1.1f%%') # putting fomatted percent values on slices
    
    # give plot a title
    plt.title(title)
    
    # save plot to file
    # we'll use passed title to give file name
    path = './{}_piechart.png'.format(title)
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))
    
    # close figure so it doesn't display
    plt.close()
    return

# define bar chart plotting function
# takes list of values and labels and title string
# saves plot to file
def bar_chart(values, labels, title, x_label, y_label):
    # see matplotlib website for more details
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
    
    # if lists empty print warning
    if len(values) < 1:
        print('Warning: empty input so generated plot will be empty')
    
    # create bar chart
    plt.bar(range(len(values)), # x coordinates of bars will be 0, 1,... len(values)-1
            values, # height of bars will be values
            tick_label=labels) # label bars with years
    
    # label x and y axis
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    # give plot a title
    plt.title(title)
    
    # save plot to file
    # we'll use passed title to give file name
    path = './{}_barchart.png'.format(title)
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))
    
    # close figure so it doesn't display
    plt.close()
    return

def bar_chart2(male_values, female_values, years, title, x_label, y_label):
    # see matplotlib website for more details
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
    
    # if lists empty print warning
    if len(years) < 1:
        print('Warning: empty input so generated plot will be empty')
        
    xs = list(range(len(years)))
    width = 0.35
    x_male = [x - width/2 for x in xs]
    x_female = [x + width/2 for x in xs]
    
    
    fig, ax = plt.subplots()
    
    ax.bar(x_male, male_values, width, label='Male')
    ax.bar(x_female, female_values, width, label='Female')
    
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(xs)
    ax.set_xticklabels(years)
    ax.legend()
    
    # save plot to file
    # we'll use passed title to give file name
    path = './{}_barchart2.png'.format(title)
    plt.savefig(path)
    print('Chart saved to file {}'.format(path))
    
    # close figure so it doesn't display
    plt.close()
    return
    
# define the main method that will run when our python program runs
def main():
    global connection
    # we will hard code the database name, could also get from user
    db_path = './MovieDBSmall.db'
    # create connection using function defined above
    connect(db_path)
    # loop program until user chooses to exit
    while(True):
        # prompt user to selet query
        print('\nPlease select query to execute')
        print('1. Total revenue by year')
        print('2. Average Netflix rating by year')
        print('3. Exit program')
        query_selection = input('Selection: ')
        # input function will return string so compare to strings
        if query_selection == '1':
            query1()
        elif query_selection == '2':
            query2()
        # if user selects 3 break program while loop and exit program
        elif query_selection == '3':
            print('Goodbye :)')
            break
        # if user enters anything but 1, 2, or 3 prompt for valid input
        else:
            print("\nInvalid input!\nSelection must be 1, 2, or 3")
    
    # close connection before exiting
    connection.close()
  
# run main method when program starts
if __name__ == "__main__":
    main()