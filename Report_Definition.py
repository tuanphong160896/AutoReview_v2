
TEST_SCRIPT_DIR = "/02_TestScript"



############################################################################

START_C_FILE = "Checking file: "
END_C_FILE = "\n\n*********************************************************\n\n"
NO_SCRIPT_FOUND = "\nCannot find any Test Script file.\nThe tool stopped here.\n"
UNABLE_OPEN_SCRIPT = "\nCannot open Test Script file. The tool stopped here.\n"
START_TESTCASE = "\n\nChecking format of Test Case: "
START_STUBFNC = "\n\nChecking Call Interface Control "
PARAMETER_CHECK = "parameters check in INSTANCE "
OF_FUNCTION = " of Function "
AT_LINE = " at line "
WARNING = "\n- WARNING: "
UNITIALIZED = " was not INITIALISED"
LACKOF = "Lack of "
NOVCMAPPED = "No VC was mapped"
PROCESSING = "..."

############################################################################

TESTMETHOD_STR = "Test Method"
TESTERDEFINE_STR = "Tester Define"
TESTCASEDECLARE_STR = "Test case data declarations"
SETGLOBALDATA_STR = "Set global data"
INITGLOBAL = "initialise_global_data()"
SETEXPTGLOBAL_STR = "Set expected values for global data checks"
INITEXPTGLOBAL = "initialise_expected_global_data()"
EXPTCALL_STR = "Expected call sequence"
EXPTCALL = "EXPECTED_CALLS"
CALLSUT_STR = "Call SUT"
TESTCASECHECK = "Test case checks"
EXPTRESULT = "Expected Result"
CHECKGLOBAL_STR = "Checks on global data"
CHECKGLOBAL = "check_global_data"
VC = "GUID"
TO_CHECK_LST = [ TESTMETHOD_STR, TESTERDEFINE_STR, TESTCASEDECLARE_STR, SETGLOBALDATA_STR,
                INITGLOBAL, SETEXPTGLOBAL_STR, INITEXPTGLOBAL,
                EXPTCALL_STR, EXPTCALL, CALLSUT_STR, TESTCASECHECK, EXPTRESULT,
                CHECKGLOBAL_STR, CHECKGLOBAL, VC]

BEGIN_TEST_CASE = "Begin Test Case"
END_TEST_CASE = "End Test Case"
END_ALL_TEST_CASES = "End of Checking Test Cases"
UNDEFINED_STATE = "Undefined"

############################################################################

BEGINFUNC = "Begin Stub Function"
DECLAREFNC = "Stub Function Declaration"
REGISTERCALL = "REGISTER CALL"
BEGININTSTANCE = "Begin INSTANCE"
CHECK_PARAM = "CHECK_"
ENDINSTANCE = "End INSTANCE"
ENDFILE = "End Test Script file"
ENDFUNC = "End Stub Function"

############################################################################

