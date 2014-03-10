# -*- coding: utf-8 -*-

import json
import shlex

from IPython import embed as IPS

"""
this module is the json backend of the code-quiz server
"""


class DictContainer(object):
    """
    data structure to handle json data (dicts whose values are
    dicts, lists or "flat objects")
    """

    def __init__(self, segment_dict, dc_name='unnamed'):
        self.dc_name = dc_name
        self.ext_dict = dict(segment_dict)  # store a flat copy of external dict
        self.ext_attributes = segment_dict.keys()
        # only new keys are allowed
        assert set(self.ext_attributes).intersection(self.__dict__.keys()) == \
               set()
        self.__dict__.update(segment_dict)

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


def aux_remove_carriage_returns(solution):
    solution = solution.replace('\r', '')
    return solution


# TODO: Unit-Tests
# This gets more involved if multiline strings are considered
def aux_remove_needless_spaces(string):
    """
    converts "x =  8 +3" into "x = 8 + 3"
    preserves spaces inside quotes, adds one space inside parentheses on each side, removes extra spaces
    applying this treatment to both user input and given solution makes a good test for sameness disregarding whitespace
    """
    lines = string.split('\n')
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped == "":
            new_lines.append(line)
        else:
            # :DOC: http://pymotw.com/2/shlex/
            # encoding 'iso-8859-1' because it is being used in the database, apparently...
            # should maybe be read from the database configuration, somehow...
            lexer = shlex.shlex(stripped.encode("iso-8859-1"))
            tokens = []

            try:
                for token in lexer:
                    tokens.append(token.decode("iso-8859-1"))
            except ValueError, err:
                tokens = [u"___|||___|||___|||___|||___" + unicode(err)]  # definitely not the solution

            line_spaces_removed = " ".join(tokens)

            new_lines.append(line_spaces_removed)

    result = "\n".join(new_lines).rstrip()

    assert type(string) == type(result)
    return result


class Segment(object):
    """
    Models a JSON segment (of the segment list)
    """

    def __unicode__(self):
        return unicode("<%s %s>" % (type(self), id(self)))

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
        assert self.context.get('idx') is None
        self.context['idx'] = idx  # for the template
        self.idx = idx  # for update_user_solution

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
            # TODO: remove the default args here (implement unit test before)
            # because solutions now has a unified_solution_structure
            solution_content = unicode(getattr(s, 'content', s))
            # space replacement only should take place for code
            sol_type = getattr(s, 'type', 'normal')

            if sol_type == "source":
                solution_content = aux_remove_needless_spaces(solution_content)
                user_solution = aux_remove_needless_spaces(user_solution)

            if solution_content in ("True", "False"):
                if user_solution == "on":
                    user_solution = "True"
                else:
                    user_solution = "False"

            res.append(user_solution == solution_content)

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
        user_solution = aux_remove_carriage_returns(user_solution)

        # TODO: more sophisticated test here (multiple solutions)
        # I believe this is already the case... (pit)
        self.user_was_correct = self.test_user_was_correct(user_solution)
        self.context['prefilled_text'] = user_solution
        self.context['user_solution'] = user_solution

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


class GapText(QuestionSegment):
    """
    Models a text with gaps
    """
    template = 'tasks/gaptext.html'

    def __init__(self, dc):
        assert isinstance(dc.content, unicode)
        text = dc.content

        # build list of <input> fields to insert
        input_fields = []
        for sol_dict in dc.solutions:
            answer = sol_dict.answer
            solutions = getattr(sol_dict, 'solutions', None)
            longest_solution = max(solutions, key=len)

            input_field = "<input class='gap' type='text' size='{length}' value='{prefill}'>".format(prefill=answer,
                                                                                                     length=len(longest_solution))

            input_fields.append(input_field)

        # parse text and insert <input> fields instead of "¶" symbol separators
        import re

        pattern = r"(&para;).*?\1"
        text = reduce(lambda x, y: re.sub(pattern, str(y), x, 1), input_fields, text)

        self.c_text = text;
        self.c_solutions = dc.solutions

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
        if self.c_lines == 0:
            self.c_lines = 1

        self.c_prefilled_text = dc.answer.content
        self.c_answer_class = dc.answer.type

        # TODO: this is suboptimal, we need a way to let the template know what "type" each solution is (source, normal)
        #       or do we? Not necessarily, since it most likely is of the same type for each, then this would suffice...
        if type(dc.solution) == list:
            self.c_solution_class = dc.solution[0].type
        else:
            self.c_solution_class = dc.solution.type

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

        QuestionSegment.__init__(self, dc)


# TODO: implement Radio type
class RadioList(QuestionSegment):
    pass


typestr_to_class_map = {'text': Text,
                        'source': Src,
                        'input': InputField,
                        'check': CBox,
                        'gap-fill-text': GapText}


# our json format "specification" by example
# https://gist.github.com/leberwurstsaft/7158911

def make_segment(segment_dict, idx):
    """
    :segment_dict:   dictionary from json parser
    :idx:       number (index) in the segment-list
    """

    assert isinstance(segment_dict, dict)

    segment_type = segment_dict.get('type', None)
    if segment_type is None:
        raise ValueError("segment_dict should have key 'type'")

    segment_class = typestr_to_class_map.get(segment_type, None)

    dc = DictContainer(segment_dict, segment_type)
    segment = segment_class(dc)

    segment.set_idx(idx)
    return segment


def preprocess_task_from_db(task):
    """
    this function takes a task object, coming from the database

    * it parses the json and stores the result in .segment_list
    * it sets the .solution_flag to False

    """

    rd = json.loads(task.body_data)

    dict_list = rd['segments']

    question_counter[0] = 0
    task.segment_list = [make_segment(dict, idx) for idx, dict in enumerate(dict_list)]
    task.solution_flag = False

    return None


#TODO: obsolete
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

