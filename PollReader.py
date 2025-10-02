import os
import unittest


class PollReader():
    """
    A class for reading and analyzing polling data.
    """
    def __init__(self, filename):
        """
        The constructor. Opens up the specified file, reads in the data,
        closes the file handler, and sets up the data dictionary that will be
        populated with build_data_dict().

        We have implemented this for you. You should not need to modify it.
        """

        # this is used to get the base path that this Python file is in in an
        # OS agnostic way since Windows and Mac/Linux use different formats
        # for file paths, the os library allows us to write code that works
        # well on any operating system
        self.base_path = os.path.abspath(os.path.dirname(__file__))

        # join the base path with the passed filename
        self.full_path = os.path.join(self.base_path, filename)

        # open up the file handler
        self.file_obj = open(self.full_path, 'r')

        # read in each line of the file to a list
        self.raw_data = self.file_obj.readlines()

        # close the file handler
        self.file_obj.close()

        # set up the data dict that we will fill in later
        self.data_dict = {
            'month': [],
            'date': [],
            'sample': [],
            'sample type': [],
            'Harris result': [],
            'Trump result': []
        }

def build_data_dict(self):
    """
    Reads all of the raw data from the CSV and builds a dictionary where
    each key is the name of a column in the CSV, and each value is a list
    containing the data for each row under that column heading.
    """
    # skip header row
    for line in self.raw_data[1:]:
        line = line.strip()
        if not line:
            continue

        parts = [p.strip() for p in line.split(',')]  # split by comma
        # month, date, sample, Harris result, Trump result
        month = parts[0]
        date = int(parts[1])

        # sample like "1880 LV" or "2027 A"
        sample_field = parts[2]
        sample_bits = sample_field.split()
        sample_size = int(sample_bits[0])
        sample_type = sample_bits[-1]

        harris = float(parts[3])
        trump = float(parts[4])

        self.data_dict['month'].append(month)
        self.data_dict['date'].append(date)
        self.data_dict['sample'].append(sample_size)
        self.data_dict['sample type'].append(sample_type)
        self.data_dict['Harris result'].append(harris)
        self.data_dict['Trump result'].append(trump)


def highest_polling_candidate(self):
    """
    Return a string naming the candidate with the single highest polling %
    and that percentage (one decimal). If tied, return 'EVEN <pct>'.
    """
    h_max = max(self.data_dict['Harris result'])
    t_max = max(self.data_dict['Trump result'])

    if h_max > t_max:
        return f"Harris {h_max*100:.1f}%"
    elif t_max > h_max:
        return f"Trump {t_max*100:.1f}%"
    else:
        return f"EVEN {h_max*100:.1f}%"



def likely_voter_polling_average(self):
    """
    Average polling percentages among likely voters ('LV').
    Returns floats in 0..1 for (Harris, Trump).
    """
    lv_idx = [i for i, st in enumerate(self.data_dict['sample type']) if st == 'LV']
    h_vals = [self.data_dict['Harris result'][i] for i in lv_idx]
    t_vals = [self.data_dict['Trump result'][i] for i in lv_idx]
    h_avg = sum(h_vals) / len(h_vals) if h_vals else 0.0
    t_avg = sum(t_vals) / len(t_vals) if t_vals else 0.0
    return h_avg, t_avg


def polling_history_change(self):
    """
    Net change between averages of the latest 30 polls and the earliest 30 polls.
    File is in reverse-chronological order (latest first).
    """
    h = self.data_dict['Harris result']
    t = self.data_dict['Trump result']
    n = len(h)

    if n >= 60:
        latest_slice = slice(0, 30)      # first 30 rows (latest)
        earliest_slice = slice(n-30, n)  # last 30 rows (earliest)
    else:
        mid = n // 2                     # fallback if fewer than 60
        latest_slice = slice(0, mid)
        earliest_slice = slice(n-mid, n)

    h_latest = sum(h[latest_slice]) / len(h[latest_slice])
    t_latest = sum(t[latest_slice]) / len(t[latest_slice])
    h_earliest = sum(h[earliest_slice]) / len(h[earliest_slice])
    t_earliest = sum(t[earliest_slice]) / len(t[earliest_slice])

    return (h_latest - h_earliest, t_latest - t_earliest)



class TestPollReader(unittest.TestCase):
    """
    Test cases for the PollReader class.
    """
    def setUp(self):
        self.poll_reader = PollReader('polling_data.csv')
        self.poll_reader.build_data_dict()

    def test_build_data_dict(self):
        self.assertEqual(len(self.poll_reader.data_dict['date']), len(self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['date']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, str) for x in self.poll_reader.data_dict['sample type']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Harris result']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Trump result']))

    def test_highest_polling_candidate(self):
        result = self.poll_reader.highest_polling_candidate()
        self.assertTrue(isinstance(result, str))
        self.assertTrue("Harris" in result)
        self.assertTrue("57.0%" in result)

    def test_likely_voter_polling_average(self):
        harris_avg, trump_avg = self.poll_reader.likely_voter_polling_average()
        self.assertTrue(isinstance(harris_avg, float))
        self.assertTrue(isinstance(trump_avg, float))
        self.assertTrue(f"{harris_avg:.2%}" == "49.34%")
        self.assertTrue(f"{trump_avg:.2%}" == "46.04%")

    def test_polling_history_change(self):
        harris_change, trump_change = self.poll_reader.polling_history_change()
        self.assertTrue(isinstance(harris_change, float))
        self.assertTrue(isinstance(trump_change, float))
        self.assertTrue(f"{harris_change:+.2%}" == "+1.53%")
        self.assertTrue(f"{trump_change:+.2%}" == "+2.07%")


def main():
    poll_reader = PollReader('polling_data.csv')
    poll_reader.build_data_dict()

    highest_polling = poll_reader.highest_polling_candidate()
    print(f"Highest Polling Candidate: {highest_polling}")
    
    harris_avg, trump_avg = poll_reader.likely_voter_polling_average()
    print(f"Likely Voter Polling Average:")
    print(f"  Harris: {harris_avg:.2%}")
    print(f"  Trump: {trump_avg:.2%}")
    
    harris_change, trump_change = poll_reader.polling_history_change()
    print(f"Polling History Change:")
    print(f"  Harris: {harris_change:+.2%}")
    print(f"  Trump: {trump_change:+.2%}")



if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)