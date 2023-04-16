# -*- coding: utf-8 -*-

import re

from IPython import embed as IPS


xml="""
<bla><blub>123</blub>
<txt>567</txt>
<txt>hier ist <b>was</b> fett</txt>
<src>quelltext</src>
<src>mehr <i>quelltext</i> hier</src>
</bla>
"""


def pp_html(xml_string):
    pp_matches = ['<txt>.*</txt>', "<src>.*</src>"]
    delim_replacements = [('<', '{+'), ('>', '+}')]
  

    pp_matches = [m.replace('.*', '(?P<my_match>.*)') for m in pp_matches]
        
    #matcher = "(%s)" % ")|(".join(pp_matches)
    #print matcher
    
    result_string = xml_string
    
    res = []
    for m in pp_matches:
        res += re.findall(m, xml_string)
    
    #print res
    #return 
    for old_str in res:
#        tmp_tup = filter(lambda e: len(e)>0, r)
#        assert len(tmp_tup) == 1
#        old_str = tmp_tup[0]
        new_str = old_str
             
        # replace the delimiters within the match
        for o, n in delim_replacements:
            new_str = new_str.replace(o, n)
             
        # replace the whole match
        result_string = result_string.replace(old_str, new_str)

    return result_string
         

if 0:         
    m = "<txt>(?P<my_match>.*)</txt>"
    pp_matches = ['<txt>(?P<my_match1>.*)</txt>', "<src>(?P<my_match2>.*)</src>"]
    delim_replacements = [('<', '{+'), ('>', '+}')]
    matcher = "(%s)" % ")|(".join(pp_matches)
    
    print re.findall(matcher, xml)


print pp_html(xml)



def test_pp_html():
    res="""
<bla><blub>123</blub>
<txt>567</txt>
<txt>hier ist {+b+}was{+/b+} fett</txt>
<src>quelltext</src>
<src>mehr {+i+}quelltext{+/i+} hier</src>
</bla>
"""
    
IPS()