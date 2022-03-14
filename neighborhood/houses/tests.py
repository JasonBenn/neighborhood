from django.test import TestCase

from utils import format_address


class UtilsTestCase(TestCase):
    def test_format_addresses(self):
        tests = {
            "224 Page St San Francisco, CA 94102": "224 Page St, San Francisco, CA 94102",
            "226 Page St, San Francisco, CA 94102": "226 Page St, San Francisco, CA 94102",
            "290-292 Page St, San Francisco, CA 94102": "290-292 Page St, San Francisco, CA 94102",
            "290-292 PAGE St, San Francisco, CA 94102": "290-292 Page St, San Francisco, CA 94102",
            "231 SCOTT ST #1, San Francisco, CA 94117": "231 Scott St #1, San Francisco, CA 94117",
            "645 HAIGHT ST #1 A, San Francisco, CA 94117": "645 Haight St #1 A, San Francisco, CA 94117",
            "201 BUENA VISTA AVE EAST, San Francisco, CA 94117": "201 Buena Vista Ave East, San Francisco, CA 94117",
            "60 BUENA VISTA TER, San Francisco, CA 94117": "60 Buena Vista Ter, San Francisco, CA 94117",
            "56 CASTRO St, San Francisco, CA 94117": "56 Castro St, San Francisco, CA 94117"
        }
        for before, after in tests.items():
            print(format_address(before))
            assert format_address(before) == after
