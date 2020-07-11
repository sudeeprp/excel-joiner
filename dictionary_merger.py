import re

COLTOMERGE = 'coltomerge'
RECORDS = 'records'


def low_split_no_company(value):
    return re.split(r'\W+', value.lower().split('@')[0])


def match_score(value1, value2):
    if value1 == value2:
        return 100
    set1 = set(low_split_no_company(value1))
    set2 = set(low_split_no_company(value2))
    max_score = len(set1.union(set2))
    matched = len(set1.intersection(set2))
    return matched * 99 // max_score


def match_record(value_to_match, records_for_match, values_match):
    key_to_match = records_for_match[COLTOMERGE]
    match_scores = []
    for index, candidate_record in enumerate(records_for_match[RECORDS]):
        match_scores.append(
            values_match(value_to_match, candidate_record[key_to_match]))
    max_matched_score = max(match_scores)
    if max_matched_score > 0:
        assert match_scores.count(max_matched_score) == 1,\
            f'More than one match found for {value_to_match}'
        max_matched_index = match_scores.index(max_matched_score)
        return records_for_match[RECORDS][max_matched_index], max_matched_index
    else:
        return {}, -1


def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}


def remove_matched(records, matched_indexes):
    residual_records = []
    for i, r in enumerate(records):
        if i not in matched_indexes:
            residual_records.append(r)
    return residual_records


def segregate_by_key(records_to_merge):
    key_name = records_to_merge[COLTOMERGE]
    keyed_records = []
    keyless_records = []
    for r in records_to_merge[RECORDS]:
        if key_name in r:
            keyed_records.append(r)
        else:
            keyless_records.append(r)
    return keyed_records, keyless_records


def merge_records(records_to_merge1, records_to_merge2):
    merged = []
    match_key1 = records_to_merge1[COLTOMERGE]
    matched_indexes2 = set()
    keyed_records_to_merge, keyless_records_to_merge = segregate_by_key(records_to_merge1)
    for record in keyed_records_to_merge:
        matched, index = match_record(record[match_key1], records_to_merge2,
                                      match_score)
        matched_indexes2.add(index)
        merged.append(merge_dicts(record, matched))
    residual_records2 = remove_matched(records_to_merge2[RECORDS], matched_indexes2)
    merged.extend(residual_records2)
    merged.extend(keyless_records_to_merge)
    return merged
