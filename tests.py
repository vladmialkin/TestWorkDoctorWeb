import unittest
from main import Transaction


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction()

    def test_set_and_get_value(self):
        self.transaction.set_value("A", 10)
        self.assertEqual(self.transaction.get_value("A"), 10)

    def test_get_non_existent_value(self):
        self.assertEqual(self.transaction.get_value("B"), "NULL")

    def test_unset_value(self):
        self.transaction.set_value("C", 20)
        self.transaction.unset_value("C")
        self.assertEqual(self.transaction.get_value("C"), "NULL")

    def test_counts_value(self):
        self.transaction.set_value("A", 10)
        self.transaction.set_value("B", 10)
        self.transaction.set_value("C", 20)
        self.assertEqual(self.transaction.counts_value(10), 2)
        self.assertEqual(self.transaction.counts_value(20), 1)
        self.assertEqual(self.transaction.counts_value(30), 0)

    def test_find_keys(self):
        self.transaction.set_value("A", 10)
        self.transaction.set_value("B", 10)
        self.assertIn("A", self.transaction.find_keys(10))
        self.assertIn("B", self.transaction.find_keys(10))
        self.assertNotIn("C", self.transaction.find_keys(10))

    def test_transaction(self):
        self.transaction.begin()
        self.transaction.begin()
        self.transaction.set_value("A", 10)
        self.assertEqual(self.transaction.get_value("A"), 10)

        self.transaction.begin()
        self.transaction.set_value("A", 20)
        self.assertEqual(self.transaction.get_value("A"), 20)

        self.transaction.rollback()
        self.assertEqual(self.transaction.get_value("A"), 10)

        self.transaction.commit()
        self.assertEqual(self.transaction.get_value("A"), 10)

        self.transaction.begin()
        self.transaction.set_value("B", 30)
        self.assertEqual(self.transaction.get_value("B"), 30)

        self.transaction.begin()
        self.transaction.set_value("A", 40)
        self.assertEqual(self.transaction.get_value("A"), 40)

        self.transaction.rollback()
        self.assertEqual(self.transaction.get_value("A"), 10)

        self.transaction.commit()
        self.assertEqual(self.transaction.get_value("B"), 30)

        self.transaction.commit()


if __name__ == '__main__':
    unittest.main()
