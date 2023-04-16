from . import xml_lib
import unittest

def say_file():
    import inspect, os
    print("Setting up:", inspect.getfile(inspect.currentframe()))
    
say_file()


class Test_xml_lib(unittest.TestCase):

    def setUp(self):
        pass

    def test_pp_delimiters1(self):
        # make sure the shuffled sequence does not lose any elements
        xml1 = """
<bla><blub>123</blub>
<txt>567</txt>
<txt>hier ist <b>was</b> fett</txt>
<src>quelltext</src>
<src>mehr <i>quelltext</i> hier</src>
</bla>
"""
        res1_desired = """
<bla><blub>123</blub>
<txt>567</txt>
<txt>hier ist {+b+}was{+/b+} fett</txt>
<src>quelltext</src>
<src>mehr {+i+}quelltext{+/i+} hier</src>
</bla>
"""
        res1 = xml_lib.preprocess_delimiters(xml1)
        self.assertEqual(res1, res1_desired)

        xml2 = """
<txt>
hier ist <b>was</b> fett
</txt>
<src>
mehr <i>quelltext</i> hier
</src>
"""
        res2_desired = """
<txt>
hier ist {+b+}was{+/b+} fett
</txt>
<src>
mehr {+i+}quelltext{+/i+} hier
</src>
"""
        res2 = xml_lib.preprocess_delimiters(xml2)
        self.assertEqual(res2, res2_desired)

    def test_post_process(self):
        xml1 = """
<txt>
hier ist <b>was</b> fett
</txt>
"""
        res1 = xml_lib.preprocess_delimiters(xml1)
        element = xml_lib.ET.fromstring(res1)
        xml_lib.post_process_delimiters(element)


        self.assertNotEqual(xml1, res1)

        self.assertTrue(element.text in xml1) # <txt> etc is stripped of
        # but the core matters

    def test_xml_to_py(self):
        xml1 = """
<element>
    <src>func()</src><le len="10"/><sol>5 7</sol>
</element>
"""
        element = xml_lib.ET.fromstring(xml1)
        pyelement, depth = xml_lib.xml_to_py(element)

        self.assertEqual(depth, 1)
        self.assertEqual(pyelement.src.text, "func()")
        self.assertEqual(pyelement.le.text, "")
        self.assertEqual(pyelement.le.len, "10")
        self.assertEqual(pyelement.sol.text, "5 7")

    def test_fail(self):
#        self.assertTrue(False)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()