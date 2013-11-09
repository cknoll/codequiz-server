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


class DictContainer(object):
    """
    data structure to handle json data (dicts whose values are
    dicts, lists or "flat objects")
    """

    def __init__(self, thedict, dc_name='unnamed'):
        self.dc_name = dc_name
        self.ext_dict = dict(thedict) # store a flat copy of external dict
        self.ext_attributes = thedict.keys()
        # only new keys are allowed
        assert set(self.ext_attributes).intersection(self.__dict__.keys()) == \
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
                        name = "%s[%i]" % (aname, i)
                        attr[i] = DictContainer(element, name)

    def __repr__(self):
        return "<DC:%s>" % self.dc_name


#class TopLevelElement(object):
#    def __init__(self, element):
#        self.tag = element.tag
#        self.element = element
#        mapping = {'txt': self.process_txt,
#                   'src': self.process_src,
#                   'lelist': self.process_lelist,
#                   'cboxlist': self.process_cboxlist,
#                   'input_list': self.process_input_list,
#        }
#
#        # execute the appropriate method
#        mapping[self.tag]()
#
#        #print self.element.text
#        #print "multi:", self.context.get('multiline')
#
#    def process_txt(self):
#
#        self.template = 'tasks/txt.html'
#        self.context = {
#            'text': self.element.text,
#            'multiline': "\n" in self.element.text
#        }
#
#    def process_src(self):
#        self.template = 'tasks/src.html'
#        self.context = {
#            'text': self.element.text,
#            'multiline': "\n" in self.element.text
#        }
#
#    def process_lelist(self):
#        element_list, depths = zip(*[xml_to_py(xml_element) for xml_element in self.element])
#
#        self.template = 'tasks/le_list.html'
#        self.context = {
#            'le_list': element_list,
#        }
#
#    def process_input_list(self):
#        """
#        this list can contain checkboxes, line-edits and maybe more
#        """
#        input_list, depths = zip(*[xml_to_py(xml_element) for xml_element in self.element])
#
#        self.template = 'tasks/part_input_list.html'
#        self.context = dict(input_list=input_list)
#        #IPS()
#
#    def update_user_solution(self, sol_dict):
#        """
#        used to insert the user solution into the appropriate data structs
#        """
#        assert not self.tag == 'lelist', "Deprecated"
#
#        if self.tag in ['txt', 'src']:
#            return
#
#        assert self.tag == 'input_list', "unexpected Tag %s" % self.tag
#
#        if self.tag == 'input_list':
#            element_list = self.context['input_list']
#            assert len(sol_dict) == len(element_list)
#
#            # Challange: element_list is ordered
#            # sol_dict is not.
#            # -> we construct the keys live
#            for i, element in enumerate(element_list):
#                j = i + 1
#                key = element.get_type() + str(j)
#                #                IPS()
#                sol = sol_dict[key]
#                element.user_solution = sol
#                #print '>%s<:|%s|' % (repr(element.sol.text),  repr(sol))
#                element.user_correct = \
#                    (element.sol.text == aux_space_convert_for_lines(sol))
#
#                if element.user_correct:
#                    element.css_class = "sol_right"
#                    element.print_solution = "OK"
#                else:
#                    print element.sol.text.encode('utf8')
#                    element.css_class = "sol_wrong"
#                    if element.sol.text == "":
#                        # !! LANG
#                        element.print_solution = "[keine Änderung]"
#                    else:
#                        element.print_solution = element.sol.text


#class Element(object):
#    """
#    models an xml-Element which is not toplevel
#    """
#
#    def __init__(self, **kwargs):
#        self.__dict__.update(kwargs)
#
#        assert 'user_solution' not in self.__dict__
#        assert 'print_solution' not in self.__dict__
#        assert 'user_right' not in self.__dict__
#
#        # will be overwritten later
#        self.user_solution = ""
#        self.print_solution = ""  # will be overwritten later
#        self.css_class = "undefined_css_class"
#
#    def get_type(self):
#        """
#        determine which kind of element we have (le or cbox)
#        """
#
#        if hasattr(self, 'le'):
#            return 'le'
#        elif hasattr(self, 'cbox'):
#            return 'cbox'
#        else:
#        #            IPS()
#            raise ValueError("unknown xml-element-type")
#
#    def __repr__(self):
#        return 'xml:' + self.tag


def aux_preprocess_user_solution(us):
    us = us.replace('\r', '')
    return us


#def xml_to_py(xml_element):
#    """
#    converts an xml element into a py Element object
#    """
#    child_list = []
#    depths = [-1]  # if no
#    for child in xml_element:
#        element_object, depth = xml_to_py(child)
#        child_list.append((child.tag, element_object))
#        depths.append(depth)
#
#    maxdepth = max(depths) + 1
#    if xml_element.text is None:
#        xml_element.text = ''  # allows .strip()
#
#    if xml_element.tag == "sol":
#        tmp_element_string = aux_space_convert_for_lines(xml_element.text)
#    else:
#        tmp_element_string = xml_element.text
#
#    attribute_list = child_list + [( 'text', tmp_element_string.strip() )]
#    attribute_list += [('tag', xml_element.tag)]
#    attribute_list += xml_element.attrib.items()
#    kwargs = dict(attribute_list)
#    if not len(kwargs) == len(attribute_list):
#        raise ValueError("duplicate in attribute_list. This list should be unique: %s." % str(zip(*attribute_list)[0]))
#
#    this = Element(**kwargs)
#
#    return this, maxdepth

class Segment(object):
    """
    Models a JSON segment (of the segment list)
    """

    def __unicode__(self):
        return unicode("<%s %s>" % (type(self), id(self) ))

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
        pass


def aux_ensure_sequence(arg):
    """
    if arg is not a sequence, return (arg,)
    -> result is always iterable
    """
    if hasattr(arg, '__len__'):
        return arg
    else:
        return (arg,)


def aux_unified_solution_structure(solution):
    """
    some solutions are dictcontainers
    some are lists of dictcontainers, some are (lists of) flat objects

    always return a sequence of dictcontainers
    """

    solutions = aux_ensure_sequence(solution)
    res = []

    for s in solutions:
        if isinstance(s, DictContainer):
            assert hasattr(s, 'content')
            res.append(s)
        else:
            dc = DictContainer({'content': s}, 'flat_solution')
            res.append(dc)

    return res

# mutable global variable
question_counter = [0]


class QuestionSegment(Segment):
    """
    models anything with a solution
    """

    def __init__(self, dc):
        # probably obsolete

        if 0:
            items = dc.ext_dict.items()

            # mark the name of the keys which will go to self.context later
            # solution should not be part of self.context
            new_items = [('c_%s' % k, v) for k, v in items
                         if not k.startswith('sol')]
            self.__dict__.update(new_items)

        question_counter[0] += 1
        self.c_question_counter = question_counter[0]
        self.solution = aux_unified_solution_structure(dc.solution)
        self.make_context()

    def test_user_was_correct(self, user_solution):

        res = []
        for s in self.solution:
            content = getattr(s, 'content', s)
            #            IPS()
            res.append(user_solution == unicode(content))
        return any(res)

    def update_user_solution(self, sol_dict):
        """
        This function decides whether the users answer was correct and
        sets the respective attributes (css_class, printed_solution)
        """

        # get the matching solution for this segment
        user_solution = sol_dict[self.idx]

        # !! encoding?
        # user_solution is just a string (not unicode)
        # TODO: test solutions with special characters


        # TODO : handle leading spaces properly (already in self.solution)
        user_solution = aux_preprocess_user_solution(user_solution)

        # TODO: more sophisticated test here (multiple solutions)
        self.user_was_correct = self.test_user_was_correct(user_solution)
        self.context['prefilled_text'] = user_solution

        if self.user_was_correct:
            self.context['css_class'] = "sol_right"
            self.context['printed_solution'] = "OK"
        else:
            self.context['css_class'] = "sol_wrong"
            # TODO: handle multiple solutions
            if self.solution[0].content == "":
                # !! LANG
                self.context['printed_solution'] = "<empty string>"
            else:
                print_sol = self.solution[0].content
                self.context['printed_solution'] = print_sol


class Text(Segment):
    """
    Models Text (and Source) Segments
    """

    template = 'tasks/txt.html'

    def __init__(self, dc):
        assert isinstance(dc.content, unicode)
        self.c_text = dc.content
        # List of unicode is not handled anymore

        self.c_multiline = "\n" in self.c_text
        self.c_comment = getattr(dc, 'comment', False)

        self.make_context()


class Src(Text):
    template = 'tasks/src.html'
    pass


class InputField(QuestionSegment):
    template = 'tasks/cq2_input_field.html'

    def __init__(self, dc):
        assert isinstance(dc.content, list)

        self.make_description_cells(dc.content)

        self.c_lines = len(dc.answer.content.splitlines())
        self.c_prefilled_text = dc.answer.content

        QuestionSegment.__init__(self, dc)

    def make_description_cells(self, content):
        self.c_text_slots = content

        # currently this multiline attribute is not needed
        for cell in self.c_text_slots:
            if '\n' in cell.content:
                cell.multiline = True


class CBox(QuestionSegment):
    template = 'tasks/cq2_cbox.html'

    def __init__(self, dc):
        self.c_text_slots = dc.content
        self.c_cbox_id = "123"

        QuestionSegment.__init__(self, dc)

# not yet implemented
class RadioList(QuestionSegment):
    pass


typestr_to_class_map = {'text': Text, 'source': Src,
                        'input': InputField, 'check': CBox}


# our json format "specification" by example
# https://gist.github.com/leberwurstsaft/7158911

def make_segment(thedict, idx):
    """
    :thedict:   dictionary from json parser
    :idx:       number (index) in the segment-list
    """

    assert isinstance(thedict, dict)

    thetype = thedict.get('type', None)
    if thetype == None:
        raise ValueError("segment_dict should have key 'type'")

    theclass = typestr_to_class_map.get(thetype, None)
    if thetype == None:
        raise ValueError("unknown type string: %s" % thetype)

    dc = DictContainer(thedict, thetype)
    s = theclass(dc)

    s.set_idx(idx)
    return s


def preprocess_task_from_db(task):
    """
    this function takes a task object, coming from the database

    * it parses the json and stores the result in .segment_list
    * it sets the .solution_flag to False

    """

    rd = json.loads(task.body_xml)  # TODO: rename this field (see models.py)

    dict_list = rd['segments']

    question_counter[0] = 0
    task.segment_list = [make_segment(d, idx)
                         for idx, d in enumerate(dict_list)]

    task.solution_flag = False

    # task is changed, no need to return anything
    return None


def debug_task():
    path = "aux/task1.json"
    with open(path, 'r') as myfile:
        content = myfile.read()

    rd = json.loads(content)

    dict_list = rd['segments']

    question_counter[0] = 0
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

