import sqlite3
import pandas as pd
import re
from prettytable import PrettyTable
import plotly
import plotly.express as px

conn = sqlite3.connect('Final_proj.db')
cur = conn.cursor()

def process_command(command,res_type=None,location=None,sort_type=None,sort_order=None,number=None):
    '''This function processes user's input command and will return a list 
    of tuples according to the options provided in the command string.
    
    Parameters
    ----------
    command: str
        The command to process
    
    Returns
    -------
    list:
        Return a list of tuples, 
        each tuple represents a particular restaurant's basic information.
    '''

    if 'category=' in command:
        res_type = 'Category'
    elif 'name' in command:
        res_type = 'Name'
    else:
        res_type = None
    
    if 'state=' in command:
        location = 'State'
    elif 'city=' in command:
        location = 'City'
    else:
        location = None

    if 'price' in command:
        sort_type = 'Price'
    else:
        sort_type = 'Rating'
    
    if 'bottom' in command:
        sort_order = 'ASC'
    else:
        sort_order = 'DESC'
    if (command.split(' ')[-1]).isnumeric():
        number = int(command.split(' ')[-1])
    else:
        number = 10
    
    if res_type == 'Category':
        search = re.findall(r"category=(.+?)]",command)[0]
        search = '%'+search+'%'

    elif res_type == 'Name':
        search = re.findall(r"name=(.+?)]",command)[0]
        search = '%'+search+'%'    

    if location != None and res_type !=None:
        if location == 'State':
            spec_loc = re.findall(r"state=(.+?)]",command)[0]
            query = "Select Name,Category,City,Price,Rating,Phone,Address from Restaurants where %s like '%s' and State='%s' order by %s %s" % (res_type,search,spec_loc,sort_type,sort_order)
            cur.execute(query)
            temp_data = cur.fetchall()
            raw_result = temp_data[0:number]
            return raw_result
            # print(raw_result)
        elif location == 'City':
            spec_loc = re.findall(r"city=(.+?)]",command)[0]
            query = "Select Name,Category,City,Price,Rating,Phone,Address from Restaurants where %s like '%s' and City='%s' order by %s %s" % (res_type,search,spec_loc,sort_type,sort_order)
            cur.execute(query)
            temp_data = cur.fetchall()
            raw_result = temp_data[0:number]
            return raw_result

    if location == None and res_type != None:
        query = "Select Name,Category,City,Price,Rating,Phone,Address from Restaurants where %s like '%s' order by %s %s" % (res_type,search,sort_type,sort_order)
        cur.execute(query)
        temp_data = cur.fetchall()
        raw_result = temp_data[0:number]
        return raw_result
   
    if location != None and res_type == None:
        if location:
            if location == 'State':
                spec_loc = re.findall(r"state=(.+?)]",command)[0]
                query = "Select Name,Category,City,Price,Rating,Phone,Address from Restaurants where State='%s' order by %s %s" % (spec_loc,sort_type,sort_order)
                cur.execute(query)
                temp_data = cur.fetchall()
                raw_result = temp_data[0:number]
                return raw_result
               
            elif location == 'City':
                spec_loc = re.findall(r"city=(.+?)]",command)[0]
                query = "Select Name,Category,City,Price,Rating,Phone,Address from Restaurants where City='%s' order by %s %s" % (spec_loc,sort_type,sort_order)
                cur.execute(query)
                temp_data = cur.fetchall()
                raw_result = temp_data[0:number]
                return raw_result
        else:
            query = "Select Name,Category,City,Price,Rating,Phone,Address from Restaurants order by %s %s" % (sort_type,sort_order)
            cur.execute(query)
            temp_data = cur.fetchall()
            raw_result = temp_data[0:number]
            return raw_result    

def distribution_plot(command):
    '''This function processes the user's input command
    and will return a pie chart according to the options provided in the command string.
    
    Parameters
    ----------
    command: str
        The command to process
    
    Returns
    -------
    A pie chart:
        Return a pie chart according to the options provided in the command string.
    '''

    if 'category' in command:
        res_type = 'Category'
    elif 'name' in command:
        res_type = 'Name'
    else:
        res_type = None

    if 'state' in command:
        location = 'State'
    elif 'city' in command:
        location = 'City'
    else:
        location = None
    
    if 'price' in command:
        sort_order = 'Price'
    else:
        sort_order = 'Rating'

    
    if res_type == 'Category':
        search_1 = re.findall(r"category=(.+?)]", command)[0]
        search_1 = '%'+search_1+'%'
    elif res_type =='Name':
        search_1 = re.findall(r"name=(.+?)]", command)[0]
        search_1 = '%'+search_1+'%'
            
    
    if location == 'State':
        search_2 = re.findall(r"state=(.+?)]", command)[0]
    elif location == 'City':
        search_2 = re.findall(r"city=(.+?)]",command)[0]
    
    if res_type != None and location != None:
        query = "select Name,Category,%s from Restaurants where %s like '%s' and %s='%s' order by %s asc" %(sort_order,res_type,search_1,location,search_2,sort_order)

    if res_type == None and location != None:
        query = "select Name,Category,%s from Restaurants where %s='%s' order by %s asc"%(sort_order,location,search_2,sort_order)

    if res_type != None and location == None:
        query = "select Name,Category,%s from Restaurants where %s like '%s' order by %s asc" %(sort_order,res_type,search_1,sort_order)
    
    if res_type == None and location == None:
        query = "select Name,Category,%s from Restaurants order by %s asc"%(sort_order,sort_order)
        
    cur.execute(query)
    temp_data = cur.fetchall()
    temp_df = pd.DataFrame(temp_data)
    pie_labels = list(temp_df[2].unique())
    count = list(temp_df.groupby([2]).size())
    
    if sort_order == 'Price':
        count0 = len(temp_df)-sum(count)
        values = [count0]
        pie_values = values+count
    else:
        pie_values = count
    # print(pie_labels)
    # print(pie_values)
    
    fig = px.pie(names=pie_labels,values=pie_values,
    title='Distribution Plot',hole=0.3,
    color_discrete_sequence=px.colors.sequential.Sunsetdark)
    fig.show()

def command_to_table(command):
    '''This function takes a list of tuples returned by
    process_command() function and returns a pretty table.
    
    Parameters
    ----------
    command: str
        The command to process
    
    Returns
    -------
    Pretty Table:
        Return a pretty table, each row reprents a tuple containing basic information of
        a particular restaurant.
    '''

    raw_result = process_command(command)
    x = PrettyTable()
    temp_row = []
    x.field_names = ['Resturant Name','Category','City','Price','Rating','Phone','Address']
    for item in raw_result:
        temp_row = []
        for i in range(len(item)):
            temp = item[i]
            temp_row.append(temp)
        x.add_row(temp_row)
    print(x)

def load_help_text():
    '''Read and load the 'Final_projHelp.txt' file.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    Load the 'FinalprojHelp.txt' file.
    '''
    with open('FinalprojHelp.txt') as f:
        return f.read()

def interactive_prompt():
    '''This function allows a user to interactively input commands,
    and to nicely format the result for presentation and visualization.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    a nicely format table or a pie chart:
        If 'distribution' is not in the command, it will return a nicely format table.
        If 'distribution' is in the command, it will return a pie chart according the parameters
        provided in the command string.
    '''
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Please enter a command: ')
        if response == 'exit':
            exit()
        elif response == 'help':
            print(help_text)
            continue

        elif 'distribution' in response:
            distribution_plot(response)
        
        else:
            try:
                command_to_table(response)
            except:
                print('Command not recognized: {}'.format(response))


if __name__ == "__main__":
    interactive_prompt()
   

        
        


