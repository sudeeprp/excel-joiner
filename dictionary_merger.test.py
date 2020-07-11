import unittest
import dictionary_merger as merger


class DictionaryMergeCases(unittest.TestCase):
    def test_match_record_finds_record_with_key_value(self):
        value_to_find = 'aval1'
        records_for_match = {
            merger.RECORDS: [
                {'acol': 'aval1', 'bcol': 'bval1'},
                {'acol': 'aval2', 'bcol': 'bval2'}],
            merger.COLTOMERGE: 'acol'
        }
        matched, index = merger.match_record(
            value_to_find, records_for_match, merger.match_score)
        self.assertEqual(index, 0)
        self.assertEqual(matched['bcol'], 'bval1')

    def test_match_record_gives_empty_when_not_matched(self):
        value_to_find = 'notexists'
        records_for_match = {
            merger.RECORDS: [{'keytofind': 'existval'}],
            merger.COLTOMERGE: 'keytofind'
        }
        matched, index = merger.match_record(
            value_to_find, records_for_match, merger.match_score)
        self.assertEqual(index, -1)
        self.assertEqual(matched, {})

    def test_match_record_gives_best_matched_item(self):
        value_to_find = 'w1 w2'
        records_for_match = {
            merger.RECORDS: [
                {'acol': 'w0', 'bcol': 'bval1'},
                {'acol': 'w1 ab', 'bcol': 'bval2'}],
            merger.COLTOMERGE: 'acol'
        }
        matched, index = merger.match_record(
            value_to_find, records_for_match, merger.match_score)
        self.assertEqual(index, 1)
        self.assertEqual(matched['bcol'], 'bval2')

    def test_match_matches_email_to_name(self):
        value_to_find = 'w2, w1'
        records_for_match = {
            merger.RECORDS: [
                {'acol': 'w0@b.com', 'bcol': 'bval1'},
                {'acol': 'w1.w2@b.com', 'bcol': 'bval2'}],
            merger.COLTOMERGE: 'acol'
        }
        matched, index = merger.match_record(
            value_to_find, records_for_match, merger.match_score)
        self.assertEqual(index, 1)
        self.assertEqual(matched['bcol'], 'bval2')

    def test_dictionaries_with_equal_rows_are_merged(self):
        records1 = [{'acol': 'aval1', 'bcol': 'bval1'},
                    {'acol': 'aval2', 'bcol': 'bval2'}]
        records2 = [{'acol': 'aval1', 'ccol': 'cval1'},
                    {'acol': 'aval2', 'ccol': 'cval2'}]
        merged = merger.merge_records(
            {merger.RECORDS: records1, merger.COLTOMERGE: 'acol'},
            {merger.RECORDS: records2, merger.COLTOMERGE: 'acol'})
        self.assertEqual(len(merged), len(records1))
        self.assertTrue('acol' in merged[0])
        self.assertTrue('bcol' in merged[0])
        self.assertTrue('ccol' in merged[0])
        self.assertEqual('cval2', merged[1]['ccol'])

    def test_dictionaries_with_more_rows_in_first_are_merged(self):
        records1 = [{'acol': 'aval1', 'bcol': 'bval1'},
                    {'acol': 'aval2', 'bcol': 'bval2'}]
        records2 = [{'acol': 'aval1', 'ccol': 'cval1'}]
        merged = merger.merge_records(
            {merger.RECORDS: records1, merger.COLTOMERGE: 'acol'},
            {merger.RECORDS: records2, merger.COLTOMERGE: 'acol'})
        self.assertEqual(len(merged), len(records1))
        self.assertTrue('acol' in merged[0])
        self.assertTrue('bcol' in merged[0])
        self.assertTrue('ccol' in merged[0])
        self.assertFalse('ccol' in merged[1])

    def test_dictionaries_with_more_rows_in_second_are_merged(self):
        records1 = [{'acol': 'aval1', 'bcol': 'bval1'}]
        records2 = [{'acol': 'aval1', 'ccol': 'cval1'},
                    {'acol': 'aval2', 'ccol': 'cval2'}]
        merged = merger.merge_records(
            {merger.RECORDS: records1, merger.COLTOMERGE: 'acol'},
            {merger.RECORDS: records2, merger.COLTOMERGE: 'acol'})
        self.assertEqual(len(merged), len(records2))
        self.assertTrue('acol' in merged[0])
        self.assertTrue('bcol' in merged[0])
        self.assertTrue('ccol' in merged[0])
        self.assertFalse('bcol' in merged[1])


if __name__ == '__main__':
    unittest.main()
