# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as ET

import json

from IPython import embed as IPS

"""
Currently, the body of a task is stored in a custom xml format.
-> better: json

this module should be the json backend of the code-quiz server
"""


class TopLevelElement(object):
    def __init__(self, element):
        self.tag = element.tag
        self.element = element
        mapping = {'txt': self.process_txt,
                   'src': self.process_src,
                   'lelist': self.process_lelist,
                   'cboxlist': self.process_cboxlist,
                   'input_list': self.process_input_list,
        }

        # execute the appropriate method
        mapping[self.tag]()

        #print self.element.text
        #print "multi:", self.context.get('multiline')

    def process_txt(self):

        self.template = 'tasks/txt.html'
        self.context = {
            'text': self.element.text,
            'multiline': "\n" in self.element.text
        }

    def process_src(self):
        self.template = 'tasks/src.html'
        self.context = {
            'text': self.element.text,
            'multiline': "\n" in self.element.text
        }

    def process_lelist(self):
        element_list, depths = zip(*[xml_to_py(xml_element) for xml_element in self.element])

        self.template = 'tasks/le_list.html'
        self.context = {
            'le_list': element_list,
        }

    def process_input_list(self):
        """
        this list can contain checkboxes, line-edits and maybe more
        """
        input_list, depths = zip(*[xml_to_py(xml_element) for xml_element in self.element])

        self.template = 'tasks/part_input_list.html'
        self.context = dict(input_list=input_list)
        #IPS()

    def update_user_solution(self, sol_dict):
        """
        used to insert the user solution into the appropriate data structs
        """
        assert not self.tag == 'lelist', "Deprecated"

        if self.tag in ['txt', 'src']:
            return

        assert self.tag == 'input_list', "unexpected Tag %s" % self.tag

        if self.tag == 'input_list':
            element_list = self.context['input_list']
            assert len(sol_dict) == len(element_list)

            # Challange: element_list is ordered
            # sol_dict is not.
            # -> we construct the keys live
            for i, element in enumerate(element_list):
                j = i + 1
                key = element.get_type() + str(j)
                #                IPS()
                sol = sol_dict[key]
                element.user_solution = sol
                #print '>%s<:|%s|' % (repr(element.sol.text),  repr(sol))
                element.user_correct = \
                    (element.sol.text == aux_space_convert_for_lines(sol))

                if element.user_correct:
                    element.css_class = "sol_right"
                    element.print_solution = "OK"
                else:
                    print element.sol.text.encode('utf8')
                    element.css_class = "sol_wrong"
                    if element.sol.text == "":
                        # !! LANG
                        element.print_solution = "[keine Änderung]"
                    else:
                        element.print_solution = element.sol.text





class Element(object):
    """
    models an xml-Element which is not toplevel
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        assert 'user_solution' not in self.__dict__
        assert 'print_solution' not in self.__dict__
        assert 'user_right' not in self.__dict__

        # will be overwritten later
        self.user_solution = ""
        self.print_solution = ""  # will be overwritten later
        self.css_class = "undefined_css_class"

    def get_type(self):
        """
        determine which kind of element we have (le or cbox)
        """

        if hasattr(self, 'le'):
            return 'le'
        elif hasattr(self, 'cbox'):
            return 'cbox'
        else:
        #            IPS()
            raise ValueError("unknown xml-element-type")

    def __repr__(self):
        return 'xml:' + self.tag


def aux_space_convert(string):
    u"""
    converts leading spaces into ␣
    strips trailing spaces
    """

    assert "\n" not in string, "No multiline support here"

    s2 = string.strip()
    if s2 == '':
        return s2
    idx = string.index(s2[0])

    leading_spaces = string[:idx]
    # assumes utf8 file encoding:
    brace = u"␣"  # .encode('utf8')
    res = brace * len(leading_spaces) + s2
    return res


def aux_space_convert_for_lines(string):
    u"""
    multiline support of converting the leading spaces into ␣
    """
    lines = string.split("\n")
    return "\n".join([aux_space_convert(line) for line in lines])


def xml_to_py(xml_element):
    """
    converts an xml element into a py Element object
    """
    child_list = []
    depths = [-1]  # if no
    for child in xml_element:
        element_object, depth = xml_to_py(child)
        child_list.append((child.tag, element_object))
        depths.append(depth)

    maxdepth = max(depths) + 1
    if xml_element.text is None:
        xml_element.text = ''  # allows .strip()

    # TODO: This should live in the xml_element
    if xml_element.tag == "sol":
        tmp_element_string = aux_space_convert_for_lines(xml_element.text)
    else:
        tmp_element_string = xml_element.text

    attribute_list = child_list + [( 'text', tmp_element_string.strip() )]
    attribute_list += [('tag', xml_element.tag)]
    attribute_list += xml_element.attrib.items()
    kwargs = dict(attribute_list)
    if not len(kwargs) == len(attribute_list):
        raise ValueError, "duplicate in attribute_list. " \
                          "This list should be unique: %s." % str(zip(*attribute_list)[0])

    this = Element(**kwargs)

    return this, maxdepth


class DictContainer(object):

    def __init__(self, thedict, dc_name = 'unnamed'):
        self.dc_name = dc_name
        self.ext_attributes = thedict.keys()
        # only new keys are allowed
        assert set(self.ext_attributes).intersection(self.__dict__.keys()) ==\
                                                                        set()
        self.__dict__.update(thedict)

        self.deep_recursion()

    def deep_recursion(self):
        """
        goes through external attributes and converts all dicts
        (lurking in lists etc) to DictContainers
        """

        for aname in self.ext_attributes:
            attr = getattr(self, aname)

            if isinstance(attr, dict):
                setattr(self, aname, DictContainer(attr, aname))
            elif isinstance(attr, list):
                for i, element in enumerate(attr):
                    if isinstance(element, dict):
                        name = "%s[%i]" %(aname, i)
                        attr[i] = DictContainer(element, name)

    def __repr__(self):
        return "<DC:%s>" % self.dc_name

class Segment(object):
    """
    This class models a json segment (of the segmentlist)
    """
    def __init__(self, adict):
        # TODO: This constructor should live in QuestionSegment
        # -> dismiss the multi inheritance
        items = adict.items()

        # mark the name of the keys which will go to self.context later
        # soulution should not be part of self.context
        new_items = [('c_%s'%k, v) for k,v in items if not k.startswith('sol')]
        self.__dict__.update(new_items)

        assert 'solution' in adict
        self.solution  = unicode(adict['solution'])

        self.make_context()

    def __unicode__(self):
        return unicode( "<%s %s>" % (type(self), id(self) ) )

    def make_context(self):
        """
        every segment needs a context attribute where the rendering data
        is  contained

        this method creates it
        """

        keys = [k for k in dir(self) if k.startswith('c_')]


        items = [(k.replace('c_', ''), getattr(self, k)) for k in keys]
        self.context = dict(items)

    def set_idx(self, idx):
        assert self.context.get('idx') == None
        self.context['idx'] = idx # for the template
        self.idx = idx # for update_user_solution

    def update_user_solution(self, *args, **kwargs):
        """
        this abstract method does nothing
        Segments which actually have a solution override this method
        """

        # hack to use multiple inheritance here (see QuestionSegment)
        method_name = "_update_user_solution"
        if hasattr(self, method_name):
            the_method = getattr(self, method_name)
#            IPS()
            the_method(*args, **kwargs)
        else:
            # no solution to update
            pass


class QuestionSegment():
    """
    models anything with a solution
    """

    def _update_user_solution(self, sol_dict, **kwargs):

        # get the matching solution for this segment
        my_solution = sol_dict[self.idx]

        IPS()
        pass

class Text(Segment):
    """
    Models Text (and Source) Segments
    """

    template = 'tasks/txt.html'

    def __init__(self, arg):
        if isinstance(arg, unicode):
            self.c_text = arg
        elif isinstance(arg, list):
            ## !! speed improvement potential:
            assert all([isinstance(line, unicode) for line in arg])
            self.c_text = "\n".join(arg)
        else:
            raise TypeError, "arg has the wrong type: %s" % type(arg)

        self.c_multiline = "\n" in self.c_text

        self.make_context()



class Src(Text):

    template = 'tasks/src.html'
    pass

class LineInput(Segment, QuestionSegment):
    template = 'tasks/line_input.html'
    pass

class CBox(Segment, QuestionSegment):
    template = 'tasks/cbox.html'

    def __init__(self, arg):
        self.c_text_slot2 = "Label (Richtig)"
        self.c_cbox_id = "123"
        Segment.__init__(self, arg)





class RadioList(Segment, QuestionSegment):
    pass


def make_segment(thedict, idx):
    """
    :thedict:   dictionary from json parser
    :idx:       number (index) in the segment-list
    """

    assert isinstance(thedict, dict)

    assert len(thedict) == 1
    key, value = thedict.items()[0]

    if key == "text":
        s = Text(value)
    elif key == "source":
        s = Src(value)

    # !! second option is only for compatibility; should be removed soon
    elif key == "cbox" or key == "check":
        s = CBox(value)
    elif key == "line_input" or key == "line":
        s = LineInput(value)
    elif key == "radio":
        raise NotImplementedError, "radio buttons not yet implemented"
    else:
        raise ValueError, "unknown segment type from json: %s" % key

    s.set_idx(idx)
    return s


def debug_task():
    path = "aux/task1.json"
    with open(path, 'r') as myfile:
        content = myfile.read()

    rd = json.loads(content)

    dict_list = rd['segments']

    seg_list = [make_segment(d, idx) for idx, d in enumerate(dict_list)]

    return seg_list




if __name__ == "__main__":
    path = "task1.json"
    with open(path, 'r') as myfile:
        content = myfile.read()

    rd = json.loads(content)

    dict_list = rd['segments']

    seg_list = [make_segment(d) for d in dict_list]


    IPS()

