import datetime
import re
everys = 0
temp_def ='''
class Temperature:
    def __init__(self, number, tempType):
        if tempType == 'K':
            self.KTemp = number
            self.CTemp = number + 273.15
            self.FTemp = 5.0/9.0*(number - 32.0) + 273.15
        elif tempType == 'C':
            self.KTemp = number + 273.15
            self.CTemp = number
            self.FTemp = 9.0/5.0*number + 32.0      
        elif tempType == 'F':
            self.KTemp = 5.0/9.0*(number - 32.0) + 273.15
            self.CTemp = 5.0/9.0*(number -32.0)
            self.FTemp = number
    def getCelsius(self):
        return self.CTemp
    def getFarenheit(self):
        return self.FTemp
    def getKelvin(self):
        return self.KTemp

'''

class semanticAnalyzer(object):
    def __init__(self, tree):
        # Keep track of scopes
        self.varScopes = [[]]
        self.scopeDepth = 0
        # Symbols table
        self.symbolsTable = {}
        # Variable to store the code
        self.ret = "import datetime\n" + "every_list = []\n" + temp_def + self.dispatch(tree)
        # 
        # Keeps track of the number of every's

    #force exits the program after printing 
    def exit(self, exit_msg):
        print exit_msg
        #sys.exit()

    
    def dispatch(self, tree, flag=None):
        '''Dispatches based on type of node'''
        if isinstance(tree, list):
            temp = ""
            for t in tree:
                temp += self.dispatch(t)
            return temp

        method = getattr(self, "_"+tree.type)
        code = method(tree, flag)
        return code

    def _program(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _external_declaration(self, tree, flag=None):
        return self.dispatch(tree.children)

    # very basic function definition
    def _function_definition(self, tree, flag=None):
        s = "def " + tree.children[0] + "(" + self.dispatch(tree.children[1])+") :\n"
        lines = self.dispatch(tree.children[2]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        return s

    def _function_param_list(self, tree, flag=None):
        if len(tree.children)==0:
            return ''
        else:
            return self.dispatch(tree.children[0])

    def _function_param(self, tree, flag=None):
        if tree.leaf==None:
           return  self.dispatch(tree.children[0]) + "," + self.dispatch(tree.children[1])
        else:
           return tree.leaf

    def _function_param_end(self, tree, flag=None):
        return tree.leaf


    def _statement_list(self, tree, flag=None):
        return self.dispatch(tree.children)

    def _statement(self, tree, flag=None):
        return self.dispatch(tree.children) + "\n"

    def _assignment_statement(self, tree, flag=None):
        return tree.leaf + " = " + self.dispatch(tree.children[0])

    def _or_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _and_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _equality_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _relational_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _additive_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0])
        else:
            return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])  

    def _multiplicative_expression(self, tree, flag=None):
        
        if len(tree.children) == 1:
            return self.dispatch(tree.children[0]) 
        else:
            return self.dispatch(tree.children[0]) + " " + tree.children[2] + " " + self.dispatch(tree.children[1])

    #this needs to be fixed        
    def _primary_expression(self, tree, flag=None):
        if tree.leaf == None:
            return "( " + self.dispatch(tree.children[0]) + " )"
        else:
            return tree.leaf
                
    def _every_statement(self, tree, flag=None):
        global everys
        global every_list        
        everys = everys + 1
        
        s = "\ndef every" + str(everys) + "() :\n"
        s += "    print 'executing every" + str(everys) + "'\n"

        lines = self.dispatch(tree.children[1]).splitlines()
        for line in lines:
            s+= "    " + line +"\n"

        s += "def condition" + str(everys) + "():\n"
        s += "    print 'checking" + str(everys) + "'\n"
        s += "    if " + self.dispatch(tree.children[0]) + ": return True\n"
        s += "every_list.append({'func' : 'every" + str(everys)
        s += "', 'condition' : 'condition" + str(everys) + "'})"
        return s

    def _iteration_statement(self, tree, flag=None):
        s = "while(" + self.dispatch(tree.children[0]) + "):\n"
        lines = self.dispatch(tree.children[1]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        return s

    def _selection_statement(self, tree, flag=None):
        if len(tree.children) == 2:
            s = "if(" + self.dispatch(tree.children[0]) + "):\n"
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            return s
        else:
            s = "if(" + self.dispatch(tree.children[0]) + "):\n"
            lines = self.dispatch(tree.children[1]).splitlines()
            for line in lines:
                s+= "    " + line +"\n"
            s += "else:\n"
            lines = self.dispatch(tree.children[2]).splitlines()

            for line in lines:
                s+= "    " + line +"\n"
            return s

    def _print_statement(self, tree, flag=None):
        s = "print " + self.dispatch(tree.children[0])
        return s

    def _for_statement(self, tree, flag=None):
        #for iterator in a range
        s = "for " + self.dispatch(tree.children[0]) + " in range( " + self.dispatch(tree.children[1]) + " , " + self.dispatch(tree.children[2]) + " + 1 ) : \n"
        lines = self.dispatch(tree.children[3]).splitlines()

        for line in lines:
            s+= "    " + line +"\n"
        return s
    
    def _day_expression(self, tree, flag=None):
        s = "datetime.datetime.now().weekday() == "
        if tree.leaf == "Monday":
            s += "0"
        elif tree.leaf == "Tuesday":
            s += "1"
        elif tree.leaf == "Wednesday":
            s += "2"
        elif tree.leaf == "Thursday":
            s += "3"
        elif tree.leaf == "Friday":
            s += "4"
        elif tree.leaf == "Saturday":
            s += "5"
        elif tree.leaf == "Sunday":
            s += "6"

        return s
    
    def _month_expression(self, tree, flag=None):
        s = "datetime.datetime.now().month() == "
        if tree.leaf == "January":
            s+= "0"
        elif tree.leaf == 'February':
            s+= "1"
        elif tree.leaf == 'March':
            s+= "2"
        elif tree.leaf == 'April':
            s+= "3"
        elif tree.leaf == 'May':
            s+= "4"
        elif tree.leaf == 'June':
            s+= "5"
        elif tree.leaf == 'July':
            s+= "6"
        elif tree.leaf == 'August':
            s+= "7"
        elif tree.leaf == 'September':
            s+= "8"
        elif tree.leaf == 'October':
            s+= "9"
        elif tree.leaf == 'November':
            s+= "10"
        elif tree.leaf == 'December':
            s+= "11"
        else:
            s+= "12"
        return s

    def _date_time_expression(self, tree, flag=None):
        p = re.compile(r'([0-3]?[0-9])/([01]?[0-9])/([0-9][0-9][0-9][0-9])[ ]([01]?[0-9]):([0-5][0-9][ ])((AM)|(PM))')
        match = p.search(tree.leaf)
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        
        #check for valid time entries
        if day > 31 or day < 1:
            exit("Error: day value must be between 1 and 31")
        if month > 12 or month < 1:
            exit("Error: month value must be between 1 and 12")
        if year < 0:
            exit("Error: Invalid year. Year must be a positive value")
        if hour > 24 or hour < 0:
            exit("Error: Invalid hour. Only 24 hours in a day")
        if minute > 59 or minute < 0:
            exit("Error: Invalid minute. Minute must be between 0 and 59")
        
        return "datetime.datetime(" + `year` + ", " + `month` + ", " + `day` + ", " + `hour` + ", " + `minute` + ")"

    def _time_expression(self, tree, flag=None):
        p = re.compile(r'([01]?[0-9]):([0-5][0-9])[ ]((AM)|(PM))')
        match = p.search(tree.leaf)
        hour = int(match.group(1))
        minute = str(int(match.group(2)))
        time_of_day = match.group(3)
        print "Hour: " + str(hour)
        print "Minute: " + minute
        print "Time of Day: '" + time_of_day + "'"
        if time_of_day == "PM":
            hour += 12
        print "Hour: " + str(hour)
        print "Minute: " + minute
        print "Time of Day: '" + time_of_day + "'"
        return "datetime.time(" + str(hour) + ", " + minute +")" 

    def _date_expression(self, tree, flag=None):
       
        p = re.compile(r'([0-3]?[0-9])/([01]?[0-9])/([0-9][0-9][0-9][0-9])')
        match = p.search(tree.leaf)
        day = int(match.group(1))
        month = int(match.group(2))
        year = int(match.group(3))
    
        #check for errors
        if day > 31 or day < 1:
            exit("Error: day value must be between 1 and 31")

        if month > 12 or month < 1:
            exit("Error: month value must be between 1 and 12")

        if year < 1:
            exit("Error: invalid year")
            
        return "datetime.date(" + `year` + ", " + `month` + ", " + `day` + ")"


    def _temperature_expression(self, tree, flag=None):
        p = re.compile(r'([0-9]+)[ ]*([CFK])')
        match = p.search(tree.leaf)
        number = str(int(match.group(1)))
        temp_type = match.group(2)
        return "Temperature(" + number + ", '" + temp_type + "')"
    