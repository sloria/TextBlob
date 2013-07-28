'''Skipping this until NPExtractor becomes Py3 compatible.
For now, default to FastNPExtractor.
'''
# from __future__ import unicode_literals
# import unittest2 as unittest
# from nose.tools import *  # PEP8 asserts

# import nltk
# from text.np_extractor import NPExtractor, filter_insignificant

# @unittest.skip("Skipping these until the NPExtractor works with Python 3")
# class TestNPExtractor(unittest.TestCase):

#     '''An example unit test case.'''

#     def setUp(self):
#         self.extractor = NPExtractor()
#         self.text = '''
# Python is a widely used general-purpose,
# high-level programming language. Its design philosophy emphasizes code
# readability, and its syntax allows programmers to express concepts in fewer lines
# of code than would be possible in other languages. The language provides
# constructs intended to enable clear programs on both a small and large scale.
# '''
#         self.sentence = "Python is a widely used general-purpose, high-level programming language"

#     def test_extract(self):
#         noun_phrases = self.extractor.extract(self.text)
#         assert_true("Python" in noun_phrases)
#         assert_true("design philosophy" in noun_phrases)
#         assert_true("code readability" in noun_phrases)

#     def test_parse_sentence(self):
#         parsed = self.extractor.parse_sentence(self.sentence)
#         assert_true(isinstance(parsed, nltk.tree.Tree))

#     def test_filter_insignificant(self):
#         chunk = self.extractor.parse_sentence(self.sentence)
#         tags = [tag for word, tag in chunk.leaves()]
#         assert_true('DT' in tags)
#         filtered = filter_insignificant(chunk.leaves())
#         tags = [tag for word, tag in filtered]
#         assert_true("DT" not in tags)

# if __name__ == '__main__':
#     unittest.main()
