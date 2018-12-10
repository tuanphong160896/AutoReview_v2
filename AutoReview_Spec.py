import os
import xlrd
from AutoReivew_Common import Export_Report
from ReviewSpec_Def import *


#################################################

def main_Spec(input_dir, report_name):
    global report_content
    report_content = []

    spec_dir = input_dir + TEST_SPEC_DIR
    specfile_lst = findSpecdir(spec_dir)

    for specfile in specfile_lst:
        OpenWorkbook(specfile)
    
    Export_Report(report_name, report_content)


#################################################


def findSpecdir(spec_dir):
    specfile_lst = []
    for path, dirs, files in os.walk(spec_dir):
        for filename in files:
            if not (filename.startswith('~$')): #check for temporary if file is opening
                filepath = os.path.join(path, filename)
                specfile_lst.append(filepath)

    if not (specfile_lst):
        report_content.append(NO_SPEC_FOUND)

    return specfile_lst


#################################################


def OpenWorkbook(specfile):
    report_content.append(START_SPEC_FILE + specfile + PROCESSING)
    try:
        spec_workbook = xlrd.open_workbook(specfile)
        all_sheets = spec_workbook.sheet_names()
    except Exception as e:
        report_content.append(UNABLE_OPEN_SPEC)
        report_content.append(END_SPEC_FILE)
        return

    check_Stream(spec_workbook)
    tcunit_lst = get_TCSheet(all_sheets)
    check_TCSheet(tcunit_lst, spec_workbook)

    spec_workbook.release_resources()
    del spec_workbook
    report_content.append(END_SPEC_FILE)


#################################################


def check_Stream(spec_workbook):
    report_content.append(CHECKING + TEST_RESULT_SUMMARY_SHEET + PROCESSING)
    try:
        current_sheet = spec_workbook.sheet_by_name(TEST_RESULT_SUMMARY_SHEET)
    except Exception as e:
        report_content.append(WARNING + UNABLE_OPEN_SHEET + TEST_RESULT_SUMMARY_SHEET)
        return

    try:
        stream_content = current_sheet.cell(STREAM_POSITION[0], STREAM_POSITION[1]).value
    except:
        report_content.append(WARNING + UNABLE_READ_STREAM)
        return

    if (CUBAS not in stream_content):
        report_content.append(WARNING + CUBAS + CONTENT_EMPTY)


#################################################


def get_TCSheet(all_sheets):
    TCUnit_sheet_lst = []
    for sheet_name in all_sheets:
        if (TCUNIT_SHEET in sheet_name):
            TCUnit_sheet_lst.append(sheet_name)

    if not (TCUnit_sheet_lst):
        report_content.append(WARNING + TCUNIT_NOT_FOUND)
        return
    else:
        return TCUnit_sheet_lst

#################################################


def check_TCSheet(tcunit_lst, spec_workbook):
    for tc_unit_sheet in tcunit_lst:
        report_content.append(CHECKING + tc_unit_sheet + PROCESSING)
        current_sheet = spec_workbook.sheet_by_name(tc_unit_sheet)

        for index, pos_to_check in enumerate(LIST_TO_CHECK_POS):
            try:
                cell_content = current_sheet.cell(pos_to_check[0], pos_to_check[1]).value
            except: 
                report_content.append(WARNING + UNABLE_TO_READ + LIST_TO_CHECK[index])
                continue

            review_Content(cell_content.strip(), LIST_TO_CHECK[index])
            

#################################################


def review_Content(cell_content, content_refer):
    if not (cell_content):
        report_content.append(WARNING + content_refer + CONTENT_EMPTY)

    if (content_refer in (SET_GLOBAL_VARIABLES, SET_PARAMETERS, SET_STUB_FUNCTIONS)):
        for to_check in LIST_REMAINING_TO_CHECK:
            if (to_check in cell_content):
                count = cell_content.count(to_check)
                report_content.append(WARNING + str(count) + SPACE + to_check + REMAINING + IN + SPACE + content_refer)


#################################################
