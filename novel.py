'''
Novel Python Application

This program allows users to order novel, register as a new member in order
to order books, view the list of novels, view the list of authors, and view
the purchase report of customers by getting data from the database.

Miki Ando
'''
import sqlite3 as sq
from datetime import datetime, date

# identify location of database
con = sq.connect("/Users/MikiAndo/Documents/GitHub/novel-console-application-mando210/novel.db")
c = con.cursor()

# getting data from the Author table
def get_author():
    res = c.execute("SELECT * from Author")
    # Gets the data from the table
    data = c.fetchall() 
    return data

# getting data from the Novel table
def get_novel():
    res = c.execute("SELECT NovelID, Genre, Title from Novel")
    # Gets the data from the table
    data = c.fetchall() 
    return data

# getting purchase data by combining multiple tables and only showing necessary information
def get_purchase():
    res = c.execute("SELECT LastName, FirstName, DatePurchased, Title from ConsumerPurchaseNovel, Author, Novel, Consumer where ConsumerPurchaseNovel.ConsumerID = Consumer.ConsumerID and ConsumerPurchaseNovel.NovelID = Novel.NovelID and Novel.AuthorID = Author.AuthorID")
    data = c.fetchall()
    return data

# adds the order from consumer through the console
def add_purchase(cid, nc, dt, q):

    # reference: https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
    ins_str = 'INSERT INTO ConsumerPurchaseNovel (ConsumerID, NovelID, DatePurchased, NumPurchased) Values (?,?,?,?)'
    res = c.execute(ins_str,(str(cid),str(nc),str(dt),str(q)))
    con.commit()

# registers a new consumer for their cosumer ID
def add_consumer(lname, fname, phone):
    ins_str= 'INSERT INTO Consumer (LastName, FirstName, PhoneNumber) VALUES (?,?,?)'
    res = c.execute(ins_str, (lname, fname, phone))
    con.commit()

# gets Last Names of all Consumers from Consumer Table
def get_lastName():
    res = c.execute("SELECT LastName from Consumer")
    data = c.fetchall()
    return (data)

# gets First Names of all Consumer from Consumer Table
def get_firstName():
    res = c.execute("SELECT FirstName from Consumer")
    data = c.fetchall()
    return (data)

# gets the consumer ID from the last name and firstname of the user's input
def get_consumerID(ln,fn):

    # returns the Consumer ID of the user
    # and checks if the consumer ID equals for both last name and firstname
    try:
        # reference: https://stackoverflow.com/questions/32166380/how-can-you-use-python-variables-in-an-sql-search
        res = c.execute('SELECT ConsumerID from Consumer WHERE Consumer.LastName = ? AND Consumer.FirstName = ?', (ln, fn,))

        cid = c.fetchall()
        cid = cid[0]
        cid = cid[0]
        return (cid)
    
    # returns false if the ID does not match with the first name and last name
    except:
        return False

# checks if the last name and first name is in the Consumer Table
def check_consumer_id(ln,fn):
    lcheck = False
    fcheck = False
    last = get_lastName()
    first = get_firstName()

    # checks last name
    for row in last:
        for field in row: 
            lname = str(field)
            if lname == ln:
                lcheck = True

    #checks first name
    for row in first:
        for field in row: 
            fname = str(field)
            if fname == fn:
                fcheck = True
                
    # gets ID if the last name and first name exists in the Consumer Table            
    if lcheck == True and fcheck == True:
        return (get_consumerID(ln,fn))
    else:
        return False


# The following VIEW functions are specific to a console based application
# main menu
def render_menu():
    print("1. Order Books")
    print("2. Register as member") 
    print("3. Purchases Report")
    print("4. View List of Novels")
    print("5. View List of Authors")
    print("6. Exit")
    choice = int(input("\nChoose an option:\t"))

    if choice == 1:
        render_order_request()
    elif choice == 2:
        render_consumer_register()
    elif choice == 3:
        render_purchase_report()
    elif choice == 4:
        render_novel_list()
    elif choice == 5:
        render_author_list()
    elif choice == 6:
        end_program()
        return False;

    return True;

#ending program
def end_program():
    print("\nENDED SYSTEM")
    con.close()

# purchase report
# new purchases can be seen after new orders but the purchase will be in the order of their ID
def render_purchase_report():
    purchase = get_purchase()

    tbl = "Last Name\t  First Name\t  Date Purchased\t  Novel Title\n"
    line = "-"*80 + "\n"
    tbl += line
    for row in purchase:
        for field in row:
            tbl += " " + str(field)
            if len(str(field)) < 9 or len(str(field)) == 10 :
                tbl += "\t\t "
            else:
                tbl += "\t "
        tbl += "\n"
    tbl += line

    print("\nReport results\n\n" + tbl)

# Shows the list of novels 
def render_novel_list():
    novel = get_novel()

    tbl = "NovelID\t  Genre\t\t  Title\n"
    line = "-"*len(tbl)*2 + "\n"
    tbl += line
    for row in novel:
        for field in row:
            tbl += " " + str(field)
            tbl += "\t "
        tbl += "\n"
    tbl += line
           
    print("\nReport results\n\n" + tbl)

# Shows the list of authors 
def render_author_list():
    author = get_author()

    tbl = "AuthorID\t  Name\t\t\t  Nationality\n"
    line = "-"*len(tbl)*2 + "\n"
    tbl += line
    for row in author:
        for field in row:
            tbl += " " + str(field)
            if len(str(field)) < 14:
                tbl += "\t\t "
            else:
                tbl += "\t "
        tbl += "\n"
    tbl += line

    print("\nReport results\n\n" + tbl)

# renders order request
# customer can order books choosing the pickup date, novel, and quantity
def render_order_request():

    # customers don't have to know their ID. The program will get their ID
    # from their last name and first name
    ln = str(input("\nEnter your Last Name:\t"))
    fn = str(input("Enter your First Name:\t"))

    # shows the list of novels they can order
    render_novel_list()
    
    # asks which novel they want and how many they want
    novelchoice = int(input("\nChoose a novel by ID NUMBER:\t"))
    quantity = int(input("\nEnter QUANTITY of novel you would like to order:\t"))

    # asks pick up Date
    day = int(input("\nEnter pick up DAY:\t"))
    month = int(input("Enter pick up MONTH:\t"))
    year = int(input("Enter pick up YEAR:\t"))

    check_and_enter_selection(day, month, year, novelchoice, ln, fn, quantity)

# checks if the consumer is registered and is valid, then adds the order in
def check_and_enter_selection(d, m, y, nc, ln, fn, q):

    # gets the consumer ID of the user
    cid = check_consumer_id(ln,fn)

    if cid == False:
        print("\nERROR", "You are not registered as a member yet or the given information is wrong")
        print("\nPlease register first or try again") 
    else: 
        dt = date(int(y), int(m) , int(d))
        add_purchase(cid, nc, dt, q)
        print("\nSUCCESS, Your order has been added")

# Adds new consumers and register members
def render_consumer_register():
    lname = str(input("\nEnter Last name:\t"))
    fname = str(input("Enter First name:\t"))
    phone = str(input("Enter Phone number (11 digits):\t"))

    # calls the function to register new customers
    add_consumer(lname, fname, phone)
    print("\nSUCCESS", "You are now registered")
    
# Start here: loop the main menu until the user choses the exit option
while(render_menu()):
    print("\n" + ("="*60))
    print("\n\nWelcome to our reservation system")
