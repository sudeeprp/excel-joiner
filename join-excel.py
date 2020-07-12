import sys
import pandas as pd
import excel2json
import dictionary_merger as merger

FILENAME = 'filename'
RECORDS = merger.RECORDS
COLTOMERGE = merger.COLTOMERGE


def write_to_excel(records, output_filename):
    df = pd.DataFrame.from_dict(records)
    df.to_excel(output_filename, index_label='index',
                columns=["participant name", "completion time", "participant email",
                         "gender", "id", "institute name", "joined as intern",
                         "philips email id", "profile", "hm in wd", "name", "bu", "stream",
                         "c# .net", "c++", "python", "java", "javascript", "nodejs",
                         "react", "spring, springboot",
                         "wcf (windows communication foundation)", "wpf (windows presentation foundation)",
                         ".net core", "angular", "raphsody",
                         "any other specifics (items not in the above list, specific versions of angular, specific python libs, etc)"
                         ])

def join_excels(file_to_merge1, file_to_merge2, output_filename):
    records1 = excel2json.rows_to_dict_list(file_to_merge1[FILENAME])
    records2 = excel2json.rows_to_dict_list(file_to_merge2[FILENAME])
    merged_records = merger.merge_records(
        {RECORDS: records1, COLTOMERGE: file_to_merge1[COLTOMERGE]},
        {RECORDS: records2, COLTOMERGE: file_to_merge2[COLTOMERGE]})
    write_to_excel(merged_records, output_filename)


def print_usage_and_quit():
    print(f'Usage: {sys.argv[0]} first-excel first-common-col second-excel second-common-col-name output-excel')


if len(sys.argv) != 6:
    print_usage_and_quit()
else:
    join_excels({FILENAME: sys.argv[1], COLTOMERGE: sys.argv[2].lower()},
                {FILENAME: sys.argv[3], COLTOMERGE: sys.argv[4].lower()},
                sys.argv[5])
