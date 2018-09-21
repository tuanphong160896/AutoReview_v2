import os
import re
from datetime import datetime
from git import Repo

#################################################


def main_Script(dir):
    global report_Script
    report_name = getReportName(dir)
    report_Script = open(report_name, "w")

    directory_Script = dir + "/02_TestScript/"
    list_dir_TestScript_files = findAllTestScripts(directory_Script)

    for dir_TestScript_file in list_dir_TestScript_files:
        #get .c filename
        try:
            inverse_dir = dir_TestScript_file[::-1]
            first_slash_index = inverse_dir.index("/")
            inverse_Cfile_name = inverse_dir[:first_slash_index]
            Cfile_name = inverse_Cfile_name[::-1]
        except Exception as e:
            print_writetoReport("Cannot get Test Script name in " + dir_TestScript_file + "\n" + str(e))
            continue

        print_writetoReport("Checking file " + Cfile_name + "...")
        ScanTestScript(dir_TestScript_file)
        print_writetoReport("\n\n*********************************************************\n\n")
    
    report_Script.close()

#################################################

def getReportName(dir):
    #get current active branch
    try:
        repo = Repo(dir, search_parent_directories=True)
        active_branch = str(repo.active_branch)
    except Exception as e:
        print("Cannot find current active branch in git")
        active_branch = 'defaultbranch'
    
    #get datetime
    time = str(datetime.now().strftime("%H%M%S"))

    #Report name
    report_name = "Review_TestScript_" + active_branch + "_" + time + ".txt"
    return report_name

#################################################


def findAllTestScripts(directory_Script):
    list_dir_Cfiles = []
    for root, dirs, Files in os.walk(directory_Script):

        check_tests = re.search('tests', root)
        if (check_tests):
            for filename in Files:
                inverse_name = filename[::-1]
                if (inverse_name[0:2] == 'c.'):
                    dir_Cfile = root + "/" + filename
                    list_dir_Cfiles.append(dir_Cfile)

    if (len(list_dir_Cfiles) == 0):
        print_writetoReport("\n- WARNING: Cannot find any Test Script file.\nThe tool stopped here.")

    return list_dir_Cfiles


#################################################


def ScanTestScript(dir_TestScript_file):
    try:
        C_file = open(dir_TestScript_file, "r")
        all_codes = C_file.readlines()
    except Exception as e:
        print_writetoReport("Cannot open Test Script file. The tool stopped here.")
        return

    declare_TC_flag = 0
    list_TestCases = []
    line_counter = 0
    for LineofCode in all_codes:
        line_counter += 1
        if ((LineofCode.find('void run_tests()') != -1) and (LineofCode.find(';') == -1)):
            declare_TC_flag = 1

        if (declare_TC_flag == 1):
            if (LineofCode.find('(1)') != -1):
                TestCase_name = (LineofCode.strip())[0:-4]
                list_TestCases.append(TestCase_name)

            if (LineofCode.find('rule_set') != -1):
                declare_TC_flag = 0
                break

    Stub_Functions_list, begin_stub_functions_line = checkTestCase_format(all_codes, list_TestCases, line_counter)
    check_Stub_Functions(all_codes, Stub_Functions_list , begin_stub_functions_line)

    C_file.close()
    del C_file


#################################################


def checkTestCase_format(all_codes, list_TestCases, begin_counter):
    line_counter = begin_counter

    list_Tester_Define_Declaration = []
    list_Tester_Define_Init = []
    Expected_Calls_flag = 0
    Stub_Functions_list = []
    list_to_check = ["Test Method", "Tester define", "Test case data declarations", "Set global data",
                    "initialise_global_data()", "Set expected values for global data checks", "initialise_expected_global_data()",
                    "Expected Call Sequence", "EXPECTED_CALLS", "Call SUT", "Test case checks", "Expected Result",
                    "Checks on global data", "check_global_data()", "GUID"]
    list_checked = []

    state = "Unidentified"
    for LineofCode in (all_codes[begin_counter:]):
        line_counter += 1
        pre_state = state
        state = state_machine(LineofCode, list_to_check, list_checked, pre_state, str(line_counter))

        if (state == "Tester define"):
            get_content_Tester_define(LineofCode, list_Tester_Define_Declaration, list_Tester_Define_Init)

        if (state == "EXPECTED_CALLS"):
            get_stub_functions(LineofCode, Stub_Functions_list)

        if ((state == "End Test Case") and (pre_state != state)):
            check_content_Tester_define(list_Tester_Define_Declaration, list_Tester_Define_Init)
            check_list_to_check(list_to_check, list_checked)
            list_Tester_Define_Declaration = []
            list_Tester_Define_Init = []

        if (state == "End of Checking Test Cases"):
            return Stub_Functions_list, line_counter+1


#################################################


def state_machine(LineofCode, list_to_check, list_checked, pre_state, line_counter):
    returnvalue = pre_state
    if ((LineofCode.find('void') != -1) and (LineofCode.find('(int doIt)') != -1)):
        
        TestCase_name = (LineofCode.strip())[5:-11]
        print_writetoReport("\n\nChecking format of TC: " + TestCase_name + " at line " + line_counter)
        
        returnvalue = "Begin Test Case"
        return returnvalue

    for element_to_check in list_to_check:
        if (re.search(element_to_check.lower(), LineofCode.lower())):
            list_checked.append(element_to_check)
            returnvalue = element_to_check
            return returnvalue

    if (LineofCode.find('END_TEST();') != -1):
        returnvalue = "End Test Case"
        return returnvalue

    if (LineofCode.find('Call Interface Control') != -1):
        returnvalue = "End of Checking Test Cases"
        return returnvalue
        
    return returnvalue


################################################# 
    

def get_content_Tester_define(lineofcode, list_Tester_Define_Declaration, list_Tester_Define_Init):
    if ((lineofcode.find('INITIALISE') == -1) and (lineofcode.find('_entity') != -1) 
        and (lineofcode.find('=') == -1)  and (lineofcode.find('[') == -1)):
        var_Declare = lineofcode.strip()
        try:
            space_index = var_Declare.index(' ')
            var_Declare = var_Declare[space_index+1:-1]
            list_Tester_Define_Declaration.append(var_Declare)
        except:
            pass

    if ((lineofcode.find('INITIALISE') != -1) and (lineofcode.find('_entity') != -1)):
        var_Init = lineofcode.strip()
        var_Init = var_Init[11:-2]
        list_Tester_Define_Init.append(var_Init)


##################################################


def get_stub_functions(LineofCode, Stub_Functions_list):
    try:
        first_index = LineofCode.index('"')
        second_index = LineofCode.index(';')
        function_name = LineofCode[first_index + 1:second_index]
        if function_name not in Stub_Functions_list:
            Stub_Functions_list.append(function_name)
    except:
        pass


##################################################
   

def check_content_Tester_define(list_Tester_Define_Declaration, list_Tester_Define_Init):
    for var_defined in list_Tester_Define_Declaration:
        if var_defined not in list_Tester_Define_Init:
            print_writetoReport("\n- WARNING: " + var_defined + " was not INITIALISED")


##################################################  
   

def check_list_to_check(list_to_check, list_checked):
    for tocheck in list_to_check:
        if tocheck not in list_checked:
            print_writetoReport("\n- WARNING: Lack of " + tocheck)

################################################## 


def check_Stub_Functions(all_codes, Stub_Functions_list, begin_stub_functions_line):
    print_writetoReport("\n\nChecking Stub & Isolate Functions...")
    state = "Unidentified"
    line_counter = begin_stub_functions_line

    check_count = 0
    param_count = 0
    stub_declare_str = ""

    for LineofCode in (all_codes[begin_stub_functions_line:]):
        line_counter += 1
        pre_state = state
        state = state_machine_stub_functions(LineofCode, pre_state)

        if (state == "End Test Script file"):
            break

        if (state == "Begin Stub Function"):
            stub_declare_str += getStubDeclaration(LineofCode)
            if (pre_state != state):
                Stub_Function_name = getStubFunctionName(LineofCode)

        if ((state == "REGISTER CALL") and (pre_state != state)):
            param_count = getInputParam(stub_declare_str)

        if (state == "Begin INSTANCE"):
            if (pre_state != state):
                instance_name = getInstanceName(LineofCode)
                stub_with_instance = Stub_Function_name + "#" + instance_name
            check_count += LineofCode.count('CHECK_')

        if ((state == "End INSTANCE") and (pre_state != state)):
            if ((stub_with_instance in Stub_Functions_list) and (check_count < param_count)):
                    print_writetoReport("\n- WARNING: Lack of checking parameters in INSTANCE: " + instance_name + " at Function " + Stub_Function_name)
            check_count = 0

        if (state == "End Stub Function"):
            stub_declare_str = ""
            param_count = 0

        
#################################################

def state_machine_stub_functions(LineofCode, pre_state):
    returnvalue = pre_state
    if ((LineofCode.find('Stub for function') != -1) or (LineofCode.find('Isolate for function') != -1)):
        returnvalue = "Begin Stub Function"
        return returnvalue
    
    if ((LineofCode.find('REGISTER_CALL') != -1)):
        returnvalue = "REGISTER CALL"
        return returnvalue
        
    if ((LineofCode.find('IF_INSTANCE') != -1)):
        returnvalue = "Begin INSTANCE"
        return returnvalue

    if (pre_state == "Begin INSTANCE"):
        if ((LineofCode.find('return') != -1)):
            returnvalue = "End INSTANCE"
            return returnvalue

    if ((LineofCode.find('LOG_SCRIPT_ERROR') != -1)):
        returnvalue = "End Stub Function"
        return returnvalue

    if ((LineofCode.find('End of test script') != -1)):
        returnvalue = "End Test Script file"
        return returnvalue
    
    return returnvalue

#################################################


def getStubDeclaration(LineofCode):
    if ((LineofCode.find("/*") == -1)):
        LineofCode = LineofCode.strip()
        return LineofCode
    else:
         return str("")


#################################################

def getInputParam(StubDeclaration):
    param_count = 0
    inside_paren = StubDeclaration[StubDeclaration.find("(")+1:StubDeclaration.rfind(")")]
    comma_count = inside_paren.count(",")
    if (comma_count == 0):
        if (len(inside_paren) == 0):
            param_count = 0
        else:
            param_count = 1
    else:
        param_count = comma_count + 1
    return param_count


#################################################


def getStubFunctionName(LineofCode):
    LineofCode = LineofCode[::-1]
    LineofCode = LineofCode[4::]
    first_index = LineofCode.index(' ')
    function_name = LineofCode[0:first_index]
    function_name = function_name[::-1].strip()

    return function_name

#################################################

def getInstanceName(LineofCode):
    first_index = LineofCode.index('(')
    second_index = LineofCode.index(')')
    LineofCode = LineofCode[first_index + 1:second_index]
    LineofCode = re.sub(r'\s+', '', LineofCode)
    instance_name = LineofCode[1:-1]

    return instance_name

#################################################

def print_writetoReport(content):
    print(content)
    report_Script.write(content)

#################################################  