TEST_SPEC_DIR = "/01_TestSpecification"


############################################################################


NO_SPEC_FOUND = "\nCannot find any Test Spec file.\nThe tool stopped here."
UNABLE_OPEN_SPEC = "\nCannot open this workbook."

START_SPEC_FILE = "Checking file: "
PROCESSING = "..."
END_SPEC_FILE = "\n\n*********************************************************\n\n"

WARNING = "\n- WARNING: "

CHECKING = "\n\nChecking "
TEST_RESULT_SUMMARY_SHEET = "TestResultSummary"
TCUNIT_SHEET = "TC_Unit_"
UNABLE_OPEN_SHEET = "Cannot open sheet: "
UNABLE_FIND_CELL = "Cannot find cell: "
TCUNIT_NOT_FOUND = "Cannot find any TC_Unit sheet. \nThe tool stopped here."

CUBAS = "CUBAS"
UNABLE_READ_STREAM = "Unable to read stream name"
UNABLE_TO_READ = "Unable to read "
CONTENT_EMPTY = " was not filled"
REMAINING = " remaining"
IN = " in"
SPACE = " "

############################################################################

STREAM_POSITION = [3,2] #C4 cell

EXPECTED_RESULT = "Test Case Expected Results"
EXPECTED_RESULT_POS = [11, 1] #B12 cell
TEST_DESRIPTION = "Test Case Description"
TEST_DESRIPTION_POS = [12, 1] #B13 cell
TEST_METHOD = "Test Method"
TEST_METHOD_POS = [13,1]
COVERDESIGN_ID = "Covered Design_Id"
COVERDESIGN_ID_POS = [20,1] #B21 cell
SET_GLOBAL_VARIABLES = "Global Variables"
SET_GLOBAL_VARIABLES_POS = [27,1]
SET_PARAMETERS = "Parameters"
SET_PARAMETERS_POS = [28,1]
SET_STUB_FUNCTIONS = "Stub Functions"
SET_STUB_FUNCTIONS_POS = [29,1]

LIST_TO_CHECK = [EXPECTED_RESULT, TEST_DESRIPTION, TEST_METHOD, COVERDESIGN_ID,
                SET_GLOBAL_VARIABLES, SET_PARAMETERS, SET_STUB_FUNCTIONS]

LIST_TO_CHECK_POS = [EXPECTED_RESULT_POS, TEST_DESRIPTION_POS, TEST_METHOD_POS, COVERDESIGN_ID_POS,
                    SET_GLOBAL_VARIABLES_POS, SET_PARAMETERS_POS, SET_STUB_FUNCTIONS_POS]

REMAINING_PTR_PREFIX = "ptr_"
REMAINING_PTR_SUFFIX = "_ptr"
REMAINING_FNC = "_fnc"
REMAINING_ASTERISK = "*"
REMAINING_ENTITY = "_entity"

LIST_REMAINING_TO_CHECK = [REMAINING_PTR_PREFIX, REMAINING_PTR_SUFFIX, REMAINING_FNC, REMAINING_ASTERISK, REMAINING_ENTITY]
