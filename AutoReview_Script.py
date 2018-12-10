import os
from AutoReivew_Common import Export_Report
from Report_Definition import *


#################################################


def main_Script(input_dir, report_name):
    global report_content
    report_content = []

    script_dir = input_dir + TEST_SCRIPT_DIR
    list_dir_script = findScriptdir(script_dir)

    for dir_script in list_dir_script:
        ScanTestScript(dir_script)

    Export_Report(report_name, report_content)


#################################################


def findScriptdir(script_dir):
    Cfile_lst = []
    for path, subdirs, files in os.walk(script_dir):
        for filename in files:
            if filename.endswith(".c"):
                filepath = os.path.join(path, filename)
                Cfile_lst.append(filepath)

    if not (Cfile_lst):
        report_content.append(NO_SCRIPT_FOUND)

    return Cfile_lst


#################################################


def ScanTestScript(dir_script):
    report_content.append(START_C_FILE + dir_script + PROCESSING)
    try:
        C_file = open(dir_script, "r")
    except Exception as e:
        report_content.append(UNABLE_OPEN_SCRIPT)
        report_content.append(END_C_FILE)
        return

    all_codes = C_file.readlines()
    state = 0
    for LineCounter, LineofCode in enumerate(all_codes, start = 1):
        pre_state = state
        state = state_machine_Init(LineofCode, pre_state)
        if (state == 1): pass
        elif (state == 2): 
            begincheckTCline = LineCounter
            break

    ReviewTestScript(all_codes, begincheckTCline)

    C_file.close()
    del C_file


#################################################


def ReviewTestScript(all_codes, begin_counter):
    state = UNDEFINED_STATE
    (TesterDef_lst, ExptCalls_lst, Checked_lst, CalledSeq_lst, VerfCrit_lst) = ([], [], [], [], [])

    for LineCounter, LineofCode in enumerate(all_codes[begin_counter:], start = begin_counter+1):
        pre_state = state
        state = state_machine(LineofCode, Checked_lst, pre_state)

        if ((state == BEGIN_TEST_CASE) and (pre_state != state)):
            BeginTestCase(LineofCode, LineCounter)
        elif (state == TESTERDEFINE_STR):
            TesterDef_lst.append(LineofCode)
        elif (state == EXPTCALL):
            ExptCalls_lst.append(LineofCode)
        elif (state == VC):
            VerfCrit_lst.append(LineofCode)
        elif ((state == END_TEST_CASE) and (pre_state != state)):
            checkTesterDef(TesterDef_lst)
            getCalledSeq(ExptCalls_lst, CalledSeq_lst)
            check_TO_CHECK_LST(Checked_lst)
            checkVCmapped(Checked_lst, VerfCrit_lst)
            (TesterDef_lst, ExptCalls_lst, Checked_lst, VerfCrit_lst) = ([], [], [], [])
        elif (state == END_ALL_TEST_CASES):
            Review_Call_Interface(all_codes, CalledSeq_lst , LineCounter)
            break


#################################################


def state_machine_Init(LineofCode, pre_state):
    retval = pre_state
    if (isBeginDeclareTestCases(LineofCode)):
        retval = 1
    
    elif (isEndDeclareTestCases(LineofCode)):
        retval = 2
    
    return retval


#################################################


def state_machine(LineofCode, Checked_lst, pre_state):
    retval = pre_state

    if (isBeginTestCase(LineofCode)):
        retval = BEGIN_TEST_CASE
    elif (isEndTestCase(LineofCode)):
        retval = END_TEST_CASE
    elif (isEndAllTestCases(LineofCode)):
        retval = END_ALL_TEST_CASES
    else:
        for element_to_check in TO_CHECK_LST:
            if (element_to_check.lower() in LineofCode.lower()):
                Checked_lst.append(element_to_check)
                retval = element_to_check
                break

    return retval


################################################# 


def BeginTestCase(lineofcode, linecounter):
    TestCase_name = (lineofcode.strip())[5:-11]
    report_content.append(START_TESTCASE + TestCase_name + AT_LINE + str(linecounter) + PROCESSING)

    
################################################# 


def getCalledSeq(ExptCalls_lst, CalledSeq_lst):
    for lineofcode in ExptCalls_lst:
        if (isCalledSeq(lineofcode)):
            calledseq = getInsideQuote(lineofcode)
            CalledSeq_lst.append(calledseq)


##################################################
   

def checkTesterDef(TesterDef_lst):
    (list_Declare, list_Init) = ([], [])

    for lineofcode in TesterDef_lst:
        if (isTesterDefDeclare(lineofcode)):
            var_Declare = (lineofcode.split()[1]).replace(';', '')
            list_Declare.append(var_Declare)

        elif (isisTesterInit(lineofcode)):
            var_Init = getInsideBracket(lineofcode)
            list_Init.append(var_Init)

    for elem in list_Declare:
        if elem not in list_Init:
            report_content.append(WARNING + elem + UNITIALIZED)


##################################################  


def check_TO_CHECK_LST(Checked_lst):
    for tocheck in TO_CHECK_LST:
        if tocheck not in Checked_lst:
            report_content.append(WARNING + LACKOF + tocheck)
    

##################################################  


def checkVCmapped(Checked_lst, VerfCrit_lst):
    if ((VC in Checked_lst) and ( not (VerfCrit_lst))):
        VCmapped_check = 0
        for lineofcode in VerfCrit_lst:
            if isVC(lineofcode):
                VCmapped_check = 1
                break 
        if not (VCmapped_check):
            report_content.append(WARNING + NOVCMAPPED)


################################################## 


def Review_Call_Interface(all_codes, CalledSeq_lst, begin_counter):
    report_content.append(START_STUBFNC + PROCESSING)
    state = UNDEFINED_STATE
    fnc_used = 0

    for LineCounter, LineofCode in enumerate(all_codes[begin_counter:], start = begin_counter+1 ):
        pre_state = state
        state = state_machine_stub_functions(LineofCode, pre_state, fnc_used)
        
        if ((state == BEGINFUNC) and (pre_state != state)):
            fncname = (LineofCode.split())[4]
            fnc_used = checkusedfnc(fncname, CalledSeq_lst)
            (FncDec_str, InstContent_lst) = ('', [])
        elif (state == ENDFUNC):
            (fnc_used, FncDec_str) = (0, '')
        elif (state == DECLAREFNC):
            FncDec_str += LineofCode
        elif ((state == REGISTERCALL) and (pre_state != state)):
            param_count = CountParam(FncDec_str)
        elif (state == BEGININTSTANCE):
            InstContent_lst.append(LineofCode)
        elif ((state == ENDINSTANCE) and (pre_state != state)):
            checkInstance(fncname, param_count, InstContent_lst, CalledSeq_lst)
            InstContent_lst = []
        elif (state == ENDFILE):
            report_content.append(END_C_FILE)
            break

        
#################################################


def state_machine_stub_functions(LineofCode, pre_state, fnc_used):
    retval = pre_state

    if (isBeginStubFunc(LineofCode)):
        retval = BEGINFUNC
    elif ((pre_state == BEGINFUNC) and (isNotComment(LineofCode)) and (fnc_used == 1)):
        retval = DECLAREFNC
    elif (isRegisterCall(LineofCode) and (fnc_used == 1)):
        retval = REGISTERCALL
    elif (isBeginInstance(LineofCode) and (fnc_used == 1)):
        retval = BEGININTSTANCE
    elif ((pre_state == BEGININTSTANCE)) and (isEndInstance(LineofCode)):
        retval = ENDINSTANCE
    elif (isEndStubFunction(LineofCode)):
        retval = ENDFUNC
    elif (isEndFile(LineofCode)):
        retval = ENDFILE
    
    return retval


#################################################


def checkusedfnc(fncname, CalledSeq_lst):
    for elem in CalledSeq_lst:
        if (fncname in elem):
            return 1
    return 0


#################################################


def checkInstance(fncname, param_count, InstContent_lst, CalledSeq_lst):
    check_count = 0
    for elem in InstContent_lst:
        if (isBeginInstance(elem)):
            inst_name = getInsideBracket(elem)
        check_count += elem.count(CHECK_PARAM)

    seq_name = fncname + '#' + inst_name

    if (seq_name not in CalledSeq_lst):
        return
    elif (check_count < param_count):
        report_content.append(WARNING + LACKOF + PARAMETER_CHECK + inst_name + OF_FUNCTION + fncname)


#################################################


def CountParam(func_declaration):
    func_declaration = func_declaration.replace(' ', '').replace('\n','')
    input_param = getInsideBracket(func_declaration)
    comma_count = input_param.count(',')
    if (comma_count > 0): 
        param_count = comma_count + 1
    else:
        if not (input_param): param_count = 0
        else: param_count = 1

    return param_count
    


#################################################


def getInsideQuote(LineofCode):
    if (LineofCode.count('"') == 2):
        inside_quote = LineofCode[LineofCode.find('"')+1:LineofCode.rfind('"')]
        inside_quote = inside_quote.replace(';','')
        return inside_quote
    return None


#################################################


def getInsideBracket(LineofCode):
    if (('(' in LineofCode) and (')' in LineofCode)):
        inside_bracket = LineofCode[LineofCode.find('(')+1:LineofCode.rfind(')')]
        inside_bracket = inside_bracket.replace('"', '')
        return inside_bracket
    return None


#################################################


def isTesterDefDeclare(lineofcode):
    if (('INITIALISE' not in lineofcode) and ('_entity' in lineofcode) and ('=' not in lineofcode) and ('[' not in lineofcode)
        and (isNotComment(lineofcode))): return 1
    else: return 0

def isisTesterInit(lineofcode):
    if (('INITIALISE' in lineofcode) and (('_entity') in lineofcode) and (isNotComment(lineofcode))): return 1
    else: return 0

def isTestScriptWarning(lineofcode):
    if (('TEST_SCRIPT_WARNING' in lineofcode) and (isNotComment(lineofcode))): return 1
    else: return 0

def isBeginDeclareTestCases(lineofcode):
    if (('void run_tests()' in lineofcode) and (';' not in lineofcode)): return 1
    else: return 0

def isEndDeclareTestCases(lineofcode):
    if ('EXPORT_COVERAGE' in lineofcode): return 1
    else: return 0

def isUsedTestCase(lineofcode):
    if (('(1)' in lineofcode) and (isNotComment(lineofcode))): return 1
    else: return 0

def isBeginTestCase(lineofcode):
    if (('void' in lineofcode) and ('int doIt' in lineofcode)): return 1
    else: return 0

def isCalledSeq(lineofcode):
    if ((lineofcode.count('"') == 2) and ('#' in lineofcode)): return 1
    else: return 0

def isVC(lineofcode):
    if ((('{' in lineofcode) and ('}' in lineofcode)) or ('Not Applicable' in lineofcode)): return 1
    else: return 0

def isEndTestCase(lineofcode):
    if ('END_TEST();') in lineofcode: return 1
    else: return 0

def isEndAllTestCases(lineofcode):
    if ('Call Interface Control') in lineofcode: return 1
    else: return 0

def isBeginStubFunc(lineofcode):
    if (('Stub for function' in lineofcode) or ('Isolate for function' in lineofcode)): return 1
    else: return 0

def isRegisterCall(lineofcode):
    if ('REGISTER_CALL' in lineofcode): return 1
    else:  return 0

def isBeginInstance(lineofcode):
    if ('IF_INSTANCE' in lineofcode): return 1
    else: return 0

def isEndInstance(lineofcode):
    if ('return' in lineofcode): return 1
    else: return 0

def isEndStubFunction(lineofcode):
    if ('LOG_SCRIPT_ERROR' in lineofcode): return 1
    else: return 0

def isEndFile(lineofcode):
    if ('End of test script' in lineofcode): return 1
    else: return 0

def isNotComment(lineofcode):
    if (('//' not in lineofcode) and ('/*' not in lineofcode) and ('*/' not in lineofcode)): return 1
    else: return 0

        
#################################################