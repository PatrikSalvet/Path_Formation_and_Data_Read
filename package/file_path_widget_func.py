from .file_path_func import file_path

def file_path_widgets():
    r"""
    The <file_path_widgets> function is a GUI (Graphical User Interface) of the <file_path> function.
    The <file_path_widgets> function calls the <file_path> function using the inputs specified in the widget cells.
    Call 'help(file_path)' for detailed information about the <file_path> function.
    The widget function can be visualised using the 'file_path_widgets()' command.
    
    The <file_path> function requires the following four inputs:
        1. <path>      2. <filename>      3. <postfix>      4. <log>
        
    Where:
        1. The <path> variable is defined in the 'FOLDER PATH' section by the 'Path' widget cell.
            Example of a correct 'Path' cell input:    C:\Users\Folder1\Folder2      * For Windows
                                                       C:/Users/Folder1/Folder2      * For Linux
        2. The <filename> variable is defined in the 'FILE NAMES' section.
            The 'Filename Option' widget cell options are [1] 'load all' and [2] 'manual', where:
                [1] The 'load all' option searches for all files of the selected <postfix> file format located in the <path> directory.
                    Assigns 'load all' to the <filename> variable.
                [2] The 'manual' option allows to search for only specific files.
                    Activates the 'Number of Files' and 'Filename' widget cells.
                        The 'Number of Files' controls the number of displayed 'Filename' widget cells.
                        The 'Filename' cell inputs represent the searched files.
                        The 'Filename' cell inputs are stored to the <filename> variable.
                            Example of a correct 'Filename' cell inputs:   ExcelFile1   ExcelFile2    * For 'Number of Files' = 2
        3. The <postfix> variable is defined in the 'FILE FORMAT' section by the 'Postfix' widget cell.
            The currently supported file formats are 'xlsx', 'txt' and 'csv'.
        4. The <log> variable is defined in the 'LOGGING' section by the 'Log' widget cell.
      
    The 'Update Button' assigns values specified in the widget cells to the <path>, <filename>, <postfix> and <log> variables.
    The currently assigned <path>, <filename>, <postfix> and <log> variables are displayed in the 'ASSIGNED VALUES' section.

    The 'Result Storage Name' widget cell in the 'Function Run' section represents a variable name in which the results will be stored.
    The 'Function Run' button executes the <file_path> function.
    Prior to <file_path> function execution, all <path>, <filename>, <postfix>, <log>, 'Result Storage Name' variables must be defined.
    
    Creates new <path_global>, <filename_global>, <postfix_global> and <log_global> global variables.
    Due to the local function scope, the <path>, <filename>, etc. variables have been renamed to <path_global>, <filename_global>, etc.
    The widget cell inputs must be correctly formatted to work properly, use non-widget function call for more robust execution.
    """
    
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°    MODULE IMPORT AND CONFIGURATION SETTING    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
    
# <-1->    MODULE IMPORT
    import ipywidgets as widgets
    from IPython.display import display, clear_output
    import time
    import numpy as np
    import pandas as pd
    import re, logging, os, copy
    logging.basicConfig(format = "%(levelname)s - %(message)s", level = logging.DEBUG)
    
# <-1->    VARIABLE CREATION
    global path_global, filename_global, postfix_global, log_global
    path_global, filename_global, postfix_global, log_global = None, None, None, None
    gui_guide = file_path_widgets.__doc__

#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°    WIDGET DEFINITION    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
    
# <-1->    WIDGET CREATION
    path_widget = widgets.Text(description='Path', style={'description_width': '150px', 'width': '350px'}, 
                    layout={'width': '400px', 'margin': '10px 0px 10px 0px'}, disabled = False)
    filename_option_widget = widgets.Dropdown(options=['load all', 'manual'], value='load all', description='Filename Option',
                                style={'description_width': '150px'}, layout={'width': '300px', 'margin': '10px 0px 10px 0px'}, disabled = False)
    filename_amount_widget = widgets.BoundedIntText(value=1, min=1, max=98, step=1, description='Number of Files', style={'description_width': '150px'}, 
                                layout={'width': '300px', 'margin': '0px 0px 0px 0px'}, disabled = True)
    postfix_widget = widgets.Dropdown(options=['xlsx', 'txt', 'csv'], value='xlsx', description='Postfix',
                        style={'description_width': '150px'}, layout={'width': '300px', 'margin': '10px 0px 10px 0px'}, disabled = False)
    log_widget = widgets.Dropdown(options=['on', 'off'], value='on', description='Log',
                    style={'description_width': '150px'}, layout={'width': '300px', 'margin': '10px 0px 10px 0px'}, disabled = False)
    filename_widget = widgets.GridBox([], layout=widgets.Layout(grid_template_columns="repeat(7, 140px)", margin='0px 0px 10px 0px'))
    update_button = widgets.Button(description="Update Values", style={'description_width': '150px', 'font_weight':'bold'},
                        layout=widgets.Layout(width='400px', height='35px', margin = '0px 0px 10px 0px', border='5px solid gray'))
    path_global_widget = widgets.Text(value = path_global, description='', style={'description_width': '100x', 'width': '250px'}, 
                            layout={'width': '400px','margin': '0px 0px 6px 0px'}, disabled = True)
    filename_global_widget = widgets.Text(value = filename_global, description='', style={'description_width': '100px', 'width': '250px'}, 
                                layout={'width': '400px','margin': '6px 0px 6px 0px'}, disabled = True)
    postfix_global_widget = widgets.Text(value = postfix_global, description='', style={'description_width': '100px', 'width': '250px'}, 
                                layout={'width': '400px','margin': '6px 0px 6px 0px'}, disabled = True)
    log_global_widget = widgets.Text(value = log_global, description='', style={'description_width': '100px', 'width': '250px'}, 
                            layout={'width': '400px','margin': '6px 0px 0px 0px'}, disabled = True)
    file_widget = widgets.Text(description='Result Storage Name', style={'description_width': '150px', 'width': '350px'}, 
                        layout={'width': '400px', 'margin': '10px 0px 10px 0px'}, disabled = False)
    function_button = widgets.Button(description="Function Run", style={'description_width': '150px', 'font_weight':'bold'},
                            layout=widgets.Layout(width='400px', height='35px', margin = '0px 0px 10px 0px', border='5px solid gray'))
    guide_widget = widgets.Textarea(description='', value=gui_guide, style={'description_width': '250px', 'font_weight': 'bold'}, 
                            layout=widgets.Layout(width='800px', height='1130px', margin='0px 0px 0px 0px', border='None'), disabled = True)
    out = widgets.Output(layout={'border': '5px solid gray', 'width': '1185px', 'margin':'0px 0px 10px 0px'})
      
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°    WIDGET SETTING    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

# <-1->    <Filename> NO INPUT RESET AFTER NEW CELL INSERTION
    def update_filename_boxes(boxes_amount):
        boxes_amount = max(1, boxes_amount['new'])
        current_amount = len(filename_widget.children)
        if boxes_amount > current_amount:
            for i in range(current_amount, boxes_amount):
                filename_widget.children += (widgets.Text(description=f'', style={'description_width': '150px', 'width': '350px'},
                                                          layout={'width': '130px'}),)
        elif boxes_amount < current_amount:
            filename_widget.children = filename_widget.children[:boxes_amount]
    filename_amount_widget.observe(update_filename_boxes, 'value')
    update_filename_boxes({'new': filename_amount_widget.value})
    
# <-1->    <Filename>, <Number of Files> ENABLE WIDGET CONTENT FOR 'manual' <Filename Option>
    def update_filename_widget(filename_option_widget):
        if filename_option_widget['new'] == 'manual':
            filename_amount_widget.disabled = False
            for child in filename_widget.children:
                child.disabled = False
        elif filename_option_widget['new'] == 'load all':
            filename_amount_widget.disabled = True
            for child in filename_widget.children:
                child.disabled = True        
    filename_option_widget.observe(update_filename_widget, names='value')
    filename_widget.observe(update_filename_widget, names='value')
    update_filename_widget({'new': filename_amount_widget.value})
    
# <-1->    <Filename> WIDGET DISABLE CELL BY DEFAULT
    for child in filename_widget.children:
            child.disabled = True
            
# <-1->    <Path>, <Filename>, <Postfix>, <Log> VALUE ASSIGN ON <Update Button> EXECUTION
    def update_values(button):
        global path_global, filename_global, postfix_global, log_global
        path_global = str(path_widget.value)
        postfix_global = str(postfix_widget.value)
        log_global = str(log_widget.value)
        filename_option_value = filename_option_widget.value
        if filename_option_value == 'load all':
            filename_global = str(filename_option_value)
            filename_global_widget.value = f"filename = {filename_global}"
        else:
            filename_global = [child.value for child in filename_widget.children]
            filename_global_widget.value = f"filename = {', '.join(filename_global)}"
        path_global_widget.value = f"path = {path_global}"
        postfix_global_widget.value = f"postfix = {postfix_global}"
        log_global_widget.value = f"log = {log_global}"
    update_button.on_click(update_values)
    
# <-1->    <Result Storage Name> CREATION ON <Function RUN> EXECUTION AND OUTPUT LOG DISPLAY
    def file_path_call(button):
        with out:
            clear_output(wait=True)
            file_placeholder = file_widget.value
            if filename_global in [None,''] or path_global in [None,''] or file_widget.value == '':
                print("\n--------------  ERROR  ---------------\n|  All input cells must be defined.  |\n-------------------------------------- \
                \n\nMake sure to click the 'Update Values' button to assign the values to the variables and also make sure that the result storage "
                "name has been defined.\n")
            else:
                globals()[file_placeholder] = file_path(path_global, filename_global, postfix_global, log_global)
    function_button.on_click(file_path_call)

# <-1->    <ASSIGNED VALUES>, <GUI GUIDE> GRIDBOX CREATION
    left_box_layout = widgets.Layout(width='40%', height='160px')
    right_box_layout = widgets.Layout(width='60%', height='160px')
    left_box = widgets.VBox(children=[path_global_widget, filename_global_widget, postfix_global_widget, log_global_widget],
                            layout=left_box_layout)
    right_box = widgets.HBox(children=[guide_widget], layout=right_box_layout)
    grid_layout = widgets.HBox([left_box, right_box])
    
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°    WIDGET VISUALIZATION    °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°

# <-1->    WIDGET DISPLAY FUNCTION CREATION
    def widget_display():
        print(f"{'-' * 78}<   FILE PATH FUNCTION WIDGETS   >{'-' * 78}\n\n")
        print(f"-------------------------  FOLDER PATH  -------------------------\t\t\t\t\t\tPath input example:\t\tC:\\Users\\Folder1\\Folder2")
        display(path_widget)
        print(f"-------------------------  FILE NAMES  --------------------------\t\t\t\t\t\tFilename input example:\t\tExcelFile1   ExcelFile2")
        display(filename_option_widget)
        display(filename_amount_widget)
        display(widgets.VBox([widgets.Label(value="Filename"), filename_widget]))
        print(r'-------------------------  FILE FORMAT  -------------------------')
        display(postfix_widget)
        print(r'-------------------------  LOGGING  -----------------------------')
        display(log_widget)
        display(update_button)
        print(f"-------------------------  ASSIGNED VALUES  ---------------------\t\t\t{' ' * 6}\
        -------------------------  GUI GUIDE  ---------------------")
        display(grid_layout)
        print(r'-------------------------  FUNCTION RUN  ------------------------')
        display(file_widget)
        display(function_button)
        print(f"{'-' * 89}   OUTPUT   {'-' * 89}\n")
        display(out)
    widget_display()