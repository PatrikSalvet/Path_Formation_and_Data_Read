def file_path(path, filename, postfix, log):
    r"""
    The function returns a list of absolute file paths constructed based on the function inputs.
    The file paths can be used to load data using commands such as pandas.read_csv, etc.
    The currently supported file formats are: .xlsx, .txt, .csv.
    The list of supported file formats can be extended in the <supported_files> variable.
    
    The function requires the following four inputs:
        1. <path>      2. <filename>      3. <postfix>      4. <log>
     
    Where:
        1. The <path> is a tuple containing the full absolute folder path of the searched file.
            Examples of a correctly defined <path> variable:
                path = (r'C:\Users\patri\Desktop\PYTHON')     * for Windows
                    To define the <path> variable correctly, use the raw string (r'') or double \.
                path = (r'C:/Users/patri/Desktop/PYTHON')     * for Linux
        2. The <filename> is a list of file names to search for in the specified folder path.
            Examples of a correctly defined <filename> variable:
                filename = ['N02', 'N03', 'N04', 'N05']
                filename = ['load all']    * Loads all files in the folder with the specified <postfix>.
        3. The <postfix> is a one-element list containing a single postfix for all searched files.
            All loaded files must be of the same file format. Use 'for' loop to load files in multiple file formats.
            Example of a correctly defined <postfix> variable:
                postfix = ['xlsx']
        4. The <log> is a boolean variable controlling the logging display.
            Example of a correctly defined <log> variable:
                log = True

    Only the file paths of successfully detected files are returned. The file paths are stored in a <file> variable.
            Example of <file> variable output:
                file = [['C:\\Users\\patri\\Desktop\\PYTHON\\N02.xlsx'], ['C:\\Users\\patri\\Desktop\\PYTHON\\N03.xlsx']]
            The <file> output example has been returned based on the following inputs:
                Function inputs:
                    path = (r'C:\Users\patri\Desktop\PYTHON')
                    filename = ['N02', 'N03']
                    postfix = ['xlsx']
                    log = True
                Function call:
                    file = file_path(path, filename, postfix, log)
    
     To search for files in different file formats, use a 'for' loop.
     In such a case, the <postfix> variable must be defined as a list of file formats, e.g: ['xlsx', 'txt'].
            Example of a 'for' loop function call:
                Function inputs:  
                    path = (r'C:\Users\patri\Desktop\PYTHON')
                    filename = ['N02', 'N03', 'data']
                    postfix = ['xlsx', 'txt']
                    log = False
                Function call:
                    multi_file = [file_path(path, filename, postfix, log) for postfix in postfix]
                Optional clear output display window:
                    from IPython.display import clear_output 
                    clear_output()
                Function output:
                    multi_file[0]   stores files with the postfix[0] file format.
                    multi_file[1]   stores files with the postfix[1] file format.
                    
      The <file_path> function can also be executed using the <file_path_widgets> function.
      The <file_path_widgets> function contains a GUI (Graphical User Interface) for the <file_path> function.
          Example of a <file_path_widgets> function execution:
                    file_path_widgets()
      Call 'help(file_path_widgets)' for detailed information about the GUI function.
      
      The <file_path> function is case-insensitive by default.
      The case sensitivity can be changed by the <case_sensitivity> variable in the <file_path> function code.
      The <file_path> function contains features such as empty space and symbol filtration, list unpacking etc.
    """

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°    MODULE IMPORT AND CONFIGURATION SETTING    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

# <-1->    TIME MODULE IMPORT
    import time

# <-1->    TIMER START
    start_time = time.time()
    
# <-1->    OTHER MODULE IMPORT
    from itertools import compress
    import os, re, logging
    import time
    import numpy as np
    import pandas as pd
    import copy
    logging.basicConfig(format = "%(levelname)s - %(message)s", level = logging.DEBUG)
    
# <-1->    INPUT FORMAT CHECK FUNCTION
    def file_path_format_check(path, filename, postfix, log):

# <-2->    <path> VARIABLE FORMAT CHECK
        if not isinstance(path, str):
#          path = ['C:\\Users\\PYTHON01', 'C:\\Users\\PYTHON02']  =>  raise Exception
            if type(path) in [tuple, list] and len(path) > 1:
                raise Exception(f"\nIncorrectly defined <path> variable.\nCheck the <path> variable format.")
#          path = ((([[([(([[((r'C:\Users\patri\Desktop\PYTHON'))]]))])]])))  =>  path = 'C:\Users\patri\Desktop\PYTHON'
            while type(path) == tuple or type(path) == list:
                path = path[0]
#          path = {r'C:\Users\patri\Desktop\PYTHON'}  =>  raise Exception 
            if type(path) != str:
                raise Exception(f"\nIncorrectly defined <path> variable.\nCheck the <path> variable format.")
#          path = 'C:\Users\patri\Desktop\PYTHON'  =>  path = ['C:\Users\patri\Desktop\PYTHON']
            path = [path]
            
# <-2->    ITEM UNPACKING FUNCTION
        def flatten_items(inputs):
#          inputs = True  =>  inputs = 'True'
            if isinstance(inputs, bool):
                inputs = str(inputs)
#          inputs = 'True'  =>  inputs = ['True']
            if isinstance(inputs, str):
                return [inputs]
#          inputs = ([[(['N02']), [[('N03')]]], ['N04']])  =>  result = ['N02', 'N03', 'N04']
            if isinstance(inputs, (list, tuple)):
                result = []
                for item in inputs:
                    result.extend(flatten_items(item))
                return result
        
# <-2->    <filename> VARIABLE UNPACKING
#          filename = ([[(['N02']), [[('N03')]]], ['N04']])  =>  filename = ['N02', 'N03', 'N04']
        filename = flatten_items(filename)
#          filename = {'N02', 'N03'}  =>  raise Exception 
        if not isinstance(filename, (list)):
            raise Exception(f"\nIncorrectly defined <filename> variable.\nCheck the <filename> variable format.") 
        
# <-2->    <postfix> VARIABLE UNPACKING
#          postfix = [[(((([[(('xlsx'))]]))))]], 'txt', ['.csv']  =>  postfix = ['xlsx', 'txt', '.csv']
        postfix = flatten_items(postfix)
#          postfix = {'xlsx', 'txt'}  =>  raise Exception 
        if not isinstance(postfix, (list)):
            raise Exception(f"\nIncorrectly defined <postfix> variable.\nCheck the <postfix> variable format.")
        
# <-2->    <log> VARIABLE UNPACKING
#          log = ([((([(True)])))])  =>  log = ['True']
        log = flatten_items(log)
#          log = {'True'}  =>  raise Exception 
        if not isinstance(log, (list)):
            raise Exception(f"\nIncorrectly defined <log> variable.\nCheck the <log> variable format.")

# <-2->    <file_path_format_check> FUNCTION OUTPUT VARIABLE DEFINITION
        return path, filename, postfix, log

# <-1->    <file_path_format_check> FUNCTION CALL
    format_check = True
    if format_check:
        path, filename, postfix, log = file_path_format_check(path,filename,postfix,log)
    
# <-1->    LOGGING CONFIGURATION
    logging.basicConfig(format = "%(levelname)s - %(message)s", level = logging.DEBUG)

# <-1->    <log> VARIABLE UNPACKING.
#          log = [True]  =>  log = True      log = ['True']  =>  log = 'True'      log = 'True'  <=>  log = 'True'
    if type(log) == list and len(log) > 0:
        log = log[0]

# <-1->    <log> VARIABLE INPUT RECOGNITION AND BOOLEAN ASSIGNMENT
    if type(log) != bool:
        try:
#          log = 'abcTrue23False'  =>  len(logging_yes) != 0        log = 'abc023'  =>  len(logging_yes) == 0
            logging_yes = re.compile(r'(1|one|true|yes|enable|on)').findall(log.lower())
#          log = 'abcTrue23False'  =>  len(logging_no) != 0        log = 'abc123'  =>  len(logging_no) == 0
            logging_no = re.compile(r'(0|zero|false|no|disable|off)').findall(log.lower())
            if (len(logging_yes) != 0 ) and (len(logging_no) == 0):
                log = True
            elif (len(logging_yes) == 0 ) and (len(logging_no) != 0):
                log = False
            elif (len(logging_yes) != 0 ) and (len(logging_no) != 0):
                logging.warning(f"Incorrectly defined <log> variable. The logging has been enabled by default.")
                log = True
            elif (len(logging_yes) == 0 ) and (len(logging_no) == 0):
                logging.warning(f"Incorrectly defined <log> variable. The logging has been enabled by default.")
                log = True
        except:
            logging.warning(f"Incorrectly defined <log> variable. The logging has been enabled by default.")
            log = True
            
# <-1->    LOGGING ACTIVATION
    if log:
        logging.disable(logging.NOTSET)
        logging.info(f"Logging has been enabled for the <file_path> function.")

# <-1->    LOGGING DEACTIVATION
    else:
        logging.disable(logging.CRITICAL)

# <-1->    INPUT VARIABLE UNPACKING MESSAGE
    if format_check:
        logging.info(f"Input variable unpacking has been performed.")

# <-1->    FUNCTION INPUT DISPLAY
    logging.info(f"""file_path(path, filename, postfix, log) function has been called.
       The function inputs are:
            path = {path}
            filename = {filename}
            postfix = {postfix}
            log = {log}""")

# <-1->    <log_global> VARIABLE CREATION
    global log_global; log_global = log

# <-1->    UPPER/LOWER CASE SENSITIVITY SETTING
    if os.sep == '/':
        case_sensitivity = 'on'
        logging.info(f"The upper/lower case sensitivity status has been set to: {case_sensitivity}")
    else:
        case_sensitivity = 'off'
        logging.info(f"The upper/lower case sensitivity status has been set to: {case_sensitivity}")

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°    FILE FORMAT VERIFICATION    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

# <-1->    <supported_files> VARIABLE CREATION
    supported_files = ['xlsx', 'txt', 'csv']
    logging.info(f"The supported file formats are: {supported_files}") 

# <-1->    <postfix> VARIABLE LIST CONVERSION
#          postfix = ('xlsx')  =>  postfix = ['xlsx']        postfix = 'xlsx'  =>  postfix = ['xlsx']
    if type(postfix) == str:
        postfix = [postfix]
#          postfix = ('xlsx', 'txt')  =>  postfix = ['xlsx', 'txt']      postfix = 'xlsx', 'txt'  =>  postfix = ['xlsx', 'txt']
    elif type(postfix) == tuple:
        postfix = [*postfix]
    logging.info(f"The entered file formats are: {postfix}")
    
# <-1->    <postfix> VARIABLE EMPTY SPACE AND SYMBOL FILTRATION
#          postfix = ['x*l?!s x+']  =>  postfix = ['xlsx']
    for index,postfix_i in enumerate(postfix):
        filtered_symbols = re.compile(r"[^\s\^\?\!\#\*\%\/\\\<\>\{\}\&\$\'\"\:\;\|\@\+\-\`\[\]\(\)\.\_]*").findall(postfix_i)
        postfix[index] = (''.join([i for i in filtered_symbols])).lower()
        
# <-1->    <postfix> VARIABLE DUPLICATE FILTRATION
#     postfix = ['xlsx', 'xlsx', 'txt']  =>  postfix = ['xlsx', 'txt']
    unique_postfix = []
    [unique_postfix.append(i) for i in postfix if i not in unique_postfix]
    
# <-1->    <postfix> VARIABLE UNSUPPORTED FILE FORMAT FILTRATION
#          supported_files = ['xlsx', 'txt', 'csv']   and   postfix = ['xlsx', 'txt', 'ABC123']  =>  postfix = ['xlsx', 'txt']
    postfix = []
    [postfix.append(postfix_i) for postfix_i in unique_postfix if postfix_i in supported_files]
    logging.info(f"File format filtering has been performed, the following postfixes have been recognized: {postfix}")

# <-1->    <warnings> and <default_postfix> VARIABLE CREATION
    warnings = False; default_postfix = ['xlsx']
    
# <-1->    <postfix> VARIABLE UNSUPPORTED FILE FORMATS FOUND MESSAGE PRINT
    if len(unique_postfix) > len(postfix):
#          postfix = ['xlsx', 'ABC123']   and   supported_files = ['xlsx']  =>  postfix_difference = ['ABC123']
        postfix_difference = list(set(unique_postfix).symmetric_difference(set(postfix)))
        warnings = True
        logging.warning(f"The following file formats are not supported: {postfix_difference}")
        logging.warning(f"The files in the unsupported file format will not be searched.")

# <-1->    <postfix> VARIABLE NO VALID FILE FORMAT RECOGNIZED MESSAGE PRINT AND DEFAULT VALUE ASSIGNMENT
    if len(postfix) == 0:
#          postfix = ['']   and   default_postfix = ['xlsx'] =>  postfix = ['xlsx']
        postfix = default_postfix
        warnings = True
        logging.warning(f"None of the file formats specified in the <postfix> variable were valid.")
        logging.warning(f"The file format in the <postfix> variable has been set to the following default value: {postfix}")
        
# <-1->    <postfix> VARIABLE MULTIPLE VALID FILE FORMATS RECOGNIZED MESSAGE PRINT AND GENERIC VALUE ASSIGNMENT
    elif len(postfix) > 1:  
        warnings = True
        logging.warning(f"Multiple valid file formats have been recognized; however, only one can be used at a time.")
        logging.warning(f"The file format in the <postfix> variable has been set to the following value: ['{postfix[0]}']")
#          postfix = ['txt','xlsx']  =>  postfix = ['txt']               postfix = ['xlsx','txt']  =>  postfix = ['xlsx']
        postfix = [postfix[0]]
    
# <-1->    FINAL <postfix> VARIABLE DISPLAY
    logging.info(f"Postfix operations finished. The <postfix> variable is set to: {postfix}")

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°    FILE PATH VERIFICATION    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

# <-1->    <path> VARIABLE LIST UNPACKING
    if type(path) == list or type(path) == tuple:
        path = path[0]
        
# <-1->    <path> VARIABLE ' ', '/', '\' SYMBOL STRIP
#          path = (r'  \ \//C:\Users\patri\Desktop\PYTHON\\\ \/ ')  =>  path = (r'C:\Users\patri\Desktop\PYTHON')
    path = path.strip(' /\\')
    logging.info(f"The entered file path is: {path}")

# <-1->    <path> UNSUPPORTED SYMBOL FILTRATION
    filtered_path = re.compile(r"[^\*\?\"\|\<\>]*").findall(path)
#          path = (r'?C:\U?ser!s\pat*ri\Desk*top\PY<THO>N??/*')  =>  path = (r'C:\Users\patri\Desktop\PYTHON')
    path = (''.join(filtered_path))

# <-1->    <path> VARIABLE FOLDER NAME SEPARATION
    if os.sep == '\\':
#          path = (r'c://users///patri////desktop////python')  =>  path = (r'c:\\users\\\patri\\\\desktop\\\\python')
        path = path.replace("/",os.sep)
#          path = (r'c:\\users\patri\\desktop\python')  =>  path_split = ('c:','','','users','','patri','','','desktop','','python')
        path_split = path.split(os.sep)
    elif os.sep == '/':
#          path = (r'c:\\Users\\\patri\\\\desktop\\\\python')  =>  path = (r'c://Users///patri////desktop////python')
        path = path.replace("\\",os.sep)
#          path = (r'c://users/patri//desktop/python')  =>  path_split = ('c:','','','users','','patri','','','desktop','','python')
        path_split = path.split(os.sep)
    
# <-1->    <path> VARIABLE FOLDER NAME LIST 'None' SYMBOL FILTRATION
    path_items = [] 
#          path_split = ('c:','','','users','','patri','','','desktop','','python')  =>  path_items = ('c:','users','patri','desktop','python')
    [path_items.append(item) for item in path_split if item != '']
    
# <-1->    <path> VARIABLE DRIVE SEPARATION
    disc_item = None
    for item in path_items:
        if ':' in item:
#          disc_item = ('c:')   disc_item = ('d:')
            disc_item = item
#          path_items = ('c:','users','patri','desktop','python')  =>  path_items = ('users','patri','desktop','python')
            path_items.remove(item)
            logging.info(f"The storage drive name is: {disc_item + os.sep}")
    logging.info(f"The path folders are: {path_items}")
    
# <-1->    <disc_item> VARIABLE NOT FOUND MESSAGE
    if disc_item == None:
        raise Exception(f"\nThe storage drive was not found.\nCheck the <path> variable definition.")
    
# <-1->    <path> VARIABLE FOLDER PATH CONCATENATION
#          path = ('')  =>  path = ('c:\users\patri\desktop\python') for Windows    path = ('c:/users/patri/desktop/python') for Linux
    path = os.path.join(disc_item, os.sep, *path_items)
    logging.info(f"The searched folder path is: {path}")

# <-1->    <path> VARIABLE FOLDER PATH VERIFICATION
#          disc_item = ('c:')  =>  os.getcwd() == ('c:\')
    os.chdir(disc_item + os.sep)
    for folder in path_items:
        if case_sensitivity == 'off':
            listdir = os.listdir()
#          os.listdir() =  ['Data.txt','Datas.txt']  =>  lower_listdir = ['data.txt','datas.txt']
            lower_listdir = [item.lower() for item in listdir]
            if folder.lower() in lower_listdir:
#          os.chdir('c:\')  =>  os.chdir('c:\users')  =>  os.chdir('c:\users\patri')  =>  ... (for Windows - not upper/lower case sensitive)
                os.chdir(str(folder))
            else:
                raise Exception(f"\nThe '{folder}' folder was not found in {os.getcwd() + os.sep}\nCheck the <path> variable definition.")
        elif case_sensitivity == 'on':
            if folder in os.listdir():
#          os.chdir('C:\')  =>  os.chdir('C:\Users')  =>  os.chdir('C:\Users\patri')  =>  ... (for Linux - upper/lower case sensitive)
                os.chdir(str(folder))
            else:
                raise Exception(f"\nThe '{folder}' folder was not found in {os.getcwd() + os.sep}\nCheck the <path> variable definition.")

# <-1->    FINAL <path> VARIABLE DISPLAY
    if case_sensitivity == 'off':
        if os.getcwd().lower() == path.lower():
            logging.info(f'The folder path has been successfully found.')
        else:
            raise Exception(f"\nThe folder path was not found.\nCheck the <path> variable definition.")
    if case_sensitivity == 'on':
        if os.getcwd() == path:
            logging.info(f'The folder path has been successfully found.')
        else:
            raise Exception(f"\nThe folder path was not found.\nCheck the <path> variable definition.")
    logging.info(f"Path operations finished. The <path> variable is set to: {path}")

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°    FILE NAME VERIFICATION    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
 
# <-1->    SEARCHED <postfix> VARIABLE DISPLAY
    logging.info(f"Only the files in the following file format will be searched: {postfix}")

# <-1->    <filename> VARIABLE LIST CONVERSION
#          filename = ('data')  =>  filename = ['data']        filename = 'data'  =>  filename = ['data']
    if type(filename) == str:
        filename = [filename]
#          filename = ('data1','data2')  =>  filename = ['data1', 'data2']     filename = 'data1', 'data2' =>  filename = ['data1','data2']
    elif type(filename) == tuple:
        filename = [*filename]

# <-1->    <filename> VARIABLE 'load all' OPTION FILE SEARCH
    if 'load' in filename[0].lower() and 'all' in filename[0].lower() and len(filename) == 1:
        logging.info(f"All files in the '{'.' + postfix[0]}' file format located in the {path} directory will be loaded.")
        filename, filename_full = [], []
        for item in os.listdir():
#          os.listdir() = data1.txt, data2.txt, data3.xlsx, ...   postfix = ['txt']  =>  filename_full = ('data1.txt', 'data2.txt')
            if (item).endswith('.' + postfix[0]):
                filename_full.append(item)
#          filename_full('data1.txt','data2.txt')  =>  filename = ('data1', 'data2')
        filename = [file.split('.' + postfix[0])[0] for file in filename_full]
        if len(filename) == 0:
            logging.warning(f"No files in the '{'.' + postfix[0]}' file format found in the following folder: {path}")
        else:
            logging.info(f"The following files in the '{'.' + postfix[0]}' file format found in the {path} folder: {filename_full}")

# <-1->    <filename> VARIABLE FILE SEARCH
    else:
# <-2->    <filename> VARIABLE EMPTY ITEMS REMOVAL
#          filename = ['N03', "", '', '', (), [],'N03']  =>  filename = ['N03','N03']
        try:
            if isinstance(filename, (list, tuple)):
                filename_pop_index = [i for i, file in enumerate(filename) if file == '' or file == () or file == []]
                filename = [file for i, file in enumerate(filename) if i not in filename_pop_index]
        except: pass
        logging.info(f"The entered file names are: {filename}")
        postfix_entered = False

# <-2->    <filename> VARIABLE INPUT POSTFIX REMOVAL
        for i in range(len(filename)):
            for extension in postfix:
                if filename[i].endswith(extension):
#          filename[i] = 'data.txt'  =>  filename[i] = ['data', '.txt']  =>  filename[i] = 'data'
                    filename[i] = os.path.splitext(filename[i])[0]
                    postfix_entered = True
        if postfix_entered == True:
            logging.info(f'File postfixes have been removed from the <filename> variable. They will be taken from the <postfix> variable.')
            logging.info(f'The file names after postfix removal are: {filename}')
        filename_original = copy.deepcopy(filename)

# <-2->    <filename> VARIABLE UNSUPPORTED SYMBOL FILTRATION
        for index,filename_i in enumerate(filename):
#          filename_i = '  data1  '  =>  filename_i = 'data1'
            filename_i = filename_i.strip(' ')
#          filename_i = 'dat?a<1'  =>  filename_i = ['d', '', 'at', '', 'a', '', '']
            filtered_symbols = re.compile(r"[^\\\/\:\*\?\"\|\<\>]*").findall(filename_i)
#          filename_i = ['d', '', 'at', '', 'a', '', '']  =>  filename = ['data1']
            filename[index] = (''.join([file for file in filtered_symbols]))
        logging.info(f'Filename punctuation symbol filtration has been performed.')

# <-2->    <filename> VARIABLE DUPLICATE FILTRATION
        if case_sensitivity == 'off':
            unique_filename = []
            lowercase_filenames = set()
#          filename = ['dATa1', 'datA2', 'data2']  =>  unique_filename = ['dATa1', 'datA2']
            for file in filename:
                lowercase_file = file.lower()
                if lowercase_file not in lowercase_filenames:
                    lowercase_filenames.add(lowercase_file)
                    unique_filename.append(file)
        else:
            unique_filename = []
#          filename = ['dAta1', 'datA2', 'data2', 'data2']  =>  unique_filename = ['dAta1', 'datA2','data2']
            [unique_filename.append(file) for file in filename if file not in unique_filename and file != '']

# <-2->    <filename> VARIABLE FILE SEARCH
        filename = []
        if case_sensitivity == 'off':
            listdir = os.listdir()
#          os.listdir() =  ['Data.txt','Datas.txt']  =>  lower_listdir = ['data.txt','datas.txt']
            lower_listdir = [item.lower() for item in listdir]
#          unique_filename = ['dATa1', 'data2']    postfix = ['txt']   os.listdir() = 'DAtA1.txt'   =>  filename = ['dATa1']
            [filename.append(file) for file in unique_filename if (file.lower() + '.' + postfix[0]) in lower_listdir]
        else:
#          unique_filename = ['data1', 'data2']    postfix = ['txt']   os.listdir() = 'data1.txt'   =>  filename = ['data1']
            [filename.append(file) for file in unique_filename if (file + '.' + postfix[0]) in os.listdir()]

# <-2->    <filename> VARIABLE FILE NAME WITH POSTFIX CONSTRUCTION
#          filename = ['data1','data2']    postfix = ['txt']   =>  filename_full = ['data1.txt','data2.txt']
        filename_full = [(file + '.' + postfix[0]) for file in filename]
        logging.info(f"The following files have been found: {filename_full}")

# <-2->    <filename> VARIABLE SOME FILES NOT FOUND MESSAGE
        if len(unique_filename) > len(filename):
#          unique_filename = ['data1','data2']   os.listdir() = 'data1.txt'   =>  filename_difference = ['data2']
            filename_difference = list(set(unique_filename).symmetric_difference(set(filename)))
            warning_message = '2'
#          filename_difference = ['data3'] AND filename_original = ['data1','data2','data3*']   =>  warning_message = '1'
            for file in filename_difference:
                if file not in filename_original:
                    warning_message = '1'
            if warning_message == '2':
                logging.warning(f"The following files could not be found: {filename_difference}")
                warnings = True
            else:
                logging.warning(f"Some of the entered files could not be found.")
                warnings = True

# <-2->    <filename> VARIABLE NO FILE FOUND MESSAGE
        if len(filename) == 0:
            logging.warning(f"No file listed in the <filename> variable could be found in the specified folder.")
            warnings = True

# <-2->    <filename> VARIABLE SUCCESSFUL SEARCH MESSAGE
        if (len(filename) != 0) and (len(unique_filename) == len(filename)):
            logging.info(f"All files specified in the <filename> variable have been found.")

# <-1->    FINAL <filename> VARIABLE DISPLAY
    logging.info(f"File name operations finished. The <filename> variable is set to: {filename}")
       
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°    FILE PATH CONSTRUCTION    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
 
# <-1->    <file> VARIABLE CREATION
    file= []
#          filename = ['data1','data2']  postfix = ['txt']  path = (r'C:\Users\')   =>  file = ['C:\Users\data1.txt','C:\Users\data2.txt']
    [file.append([path + os.sep + filename + '.' + postfix[0]]) for filename in filename]

# <-1->    <file> VARIABLE DISPLAY
    for i in range(len(filename)):
        logging.info(f"The full '{i}' absolute file path is: file{[i]} = {file[i]}")

# <-1->    WARNING MESSAGE DISPLAY
    if warnings == True:
        logging.warning(f"Warnings occurred during the execution of the file search function.")
        print(f"Warnings occurred during the execution of the file search function. Check log for details.")
    else:
        logging.info(f"No warnings occurred during the execution of the file search function.")
    warnings = False

# <-1->   ERROR MESSAGE DISPLAY
    if len(file) == 0:
        print(f"\n\t\t\t\t----- ERROR -----\nFile search function finished, no files found. Check log and correct the function inputs.\
        \nType help(file_path) for function help.\n")
        error = True
    else:
        logging.info('File search function finished. The <file> variable is returned.')
        error = False

# <-1->   FUNCTION RUNTIME DISPLAY
    end_time = time.time() - start_time
    logging.info('The runtime was: %1.6fs.' %(end_time))

# <-1->   <file> VARIABLE DISPLAY
    if error == False:
        print(f"Final file paths:")
        for file_i in file:
            print(f"\t{file_i}")

# <-1->   <file_path> FUNCTION INPUT RESET
    for variable_delete in ['path', 'filename', 'postfix', 'log']:
        if variable_delete in globals():
            del globals()[variable_delete]

# <-1->   <file> VARIABLE RETURN
    return file