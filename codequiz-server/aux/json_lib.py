# -*- coding: utf-8 -*-

import json
import shlex
import re

from IPython import embed as IPS

"""
this module is the json backend of the code-quiz server
"""


class DictContainer(object):
    """
    data structure to handle json data (dicts whose values are
    dicts, lists or "flat objects")
    """

    def __init__(self, segment_dict=None, dc_name='unnamed'):
        if segment_dict is None:
            segment_dict = {}
        self.dc_name = dc_name
        self.ext_dict = dict(segment_dict)  # store a flat copy of external dict
        self.ext_attributes = segment_dict.keys()
        # only new keys are allowed
        assert set(self.ext_attributes).intersection(self.__dict__.keys()) == set()
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


def aux_ensure_sequence(arg):
    """
    if arg is not a sequence, return (arg,)
    -> result is always iterable
    """
    if hasattr(arg, '__len__'):
        return arg
    else:
        return (arg,)


class AttributeList(list):
    """
    This is a list to which we can attatch some attributes:

    L1 = []
    L1.name "Adam" # will not work

    L2 = AttributeList()
    L2.name "Eve" # will work
    """
    pass # just deriving the class is already enough


class Solution(object):
    """
    This class models the solution-related information to one segment.

    Most segments have one input field (with multiple possible solutions).
    GapText however has multiple input fields, each with multiple solutions.

    -> Any soltution consists of parts. Each part corresponds to an input
    formular field.

    """

    def __init__(self, dc):
        self.parts=[]
        self.type=dc.type

        if not self.type == "gap-fill-text":
            # there is only one part
            # (should be a sequence of dict_containers)
            tmp_part = aux_ensure_sequence(dc.solution)

            self.parts.append(tmp_part)

            # test assumptions
            for sol_dc in self.parts[0]:
                assert isinstance(sol_dc, DictContainer)
                assert hasattr(sol_dc, 'content')

        else:
            self._process_gt(dc)


    def _process_gt(self, dc):
        """
        convert the solution-sequence of a gap-fill-text-Segment to parts
        """
        for i, part_solution in enumerate(dc.solution):
            tmp_part = AttributeList()
            for j,s in enumerate(part_solution.solutions):
                # convert into DC
                name = "sol_%i_%i_%i" % (dc.idx, i, j)
                sol_dc = DictContainer({"content": s}, name)
                tmp_part.append(sol_dc)
                tmp_part.answer = part_solution.answer
            self.parts.append(tmp_part)

    def get_printed_solution(self):
        """
        returns the appropriate data for the printed solution
        (in case user was wrong) which goes to the context-dict
        """

        #TODO: pass multiple solutions to the context dict
        # could be shown with mouse-over etc.
        if not self.type == "gap-fill-text":
            assert len(self.parts) == 1
            printed_sol = self.parts[0][0].content

            if printed_sol == "":
                printed_sol = "<empty string>"

            return printed_sol
        else:
            res = []
            for p in self.parts:
                res.append(p[0].content)
            return res


# ---------------------- Segments ------------------------
# mutable global variable
question_counter = [0]


def increment_question_counter():
    question_counter[0] += 1


def make_segment(segment_dict, idx):
    """
    Return the right Segment subclass

    :param segment_dict: DictContainer (has to contain a key named 'type')
    :return: Segment subclass
    """
    assert isinstance(segment_dict, dict)

    segment_type = segment_dict.get('type', None)
    if segment_type is None:
        raise ValueError("dc should have key 'type'")

    dc = DictContainer(segment_dict, segment_type)
    dc.idx = idx

    if segment_type == "text":
        segment = Text(dc)
    elif segment_type == "source":
        segment = Src(dc)
    elif segment_type == "input":
        segment = InputField(dc)
    elif segment_type == "check":
        segment = CBox(dc)
    elif segment_type == "gap-fill-text":
        segment = GapText(dc)
    else:
        raise ValueError("Unknown segment type: %s" % segment_type)

    segment.set_idx(idx)
    return segment


class Segment(object):
    """
    Models a JSON segment (of the segment list)
    """

    def __init__(self):
        self.context = None
        self.idx = 0

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
        """Override in subclasses!"""
        pass


class Text(Segment):
    """
    Models Text (and Source) Segments
    """

    template = 'tasks/txt.html'

    def __init__(self, dc):
        super(Text, self).__init__()
        assert isinstance(dc.content, unicode)
        self.c_text = dc.content
        self.c_multiline = "\n" in self.c_text
        self.c_comment = getattr(dc, 'comment', False)
        self.make_context()


class Src(Text):
    template = 'tasks/src.html'

    pass


class QuestionSegment(Segment):
    """
    models anything with a solution
    """

    def __init__(self, dc):
        super(QuestionSegment, self).__init__()
        if 0:
            items = dc.ext_dict.items()

            # mark the name of the keys which will go to self.context later
            # solution should not be part of self.context
            new_items = [('c_%s' % k, v) for k, v in items
                         if not k.startswith('sol')]
            self.__dict__.update(new_items)

        increment_question_counter()

        self.user_was_correct = False
        self.c_question_counter = question_counter[0]

        self.solution = Solution(dc)
        self.make_context()

    def test_user_was_correct(self, user_solution):

        res = []
        for part in self.solution.parts:
            for s in part:
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
        user_solution = sol_dict[unicode(self.idx)]

        user_solution = aux_remove_carriage_returns(user_solution)

        self.context['prefilled_text'] = user_solution
        self.context['user_solution'] = user_solution

        self.user_was_correct = self.test_user_was_correct(user_solution)

        if self.user_was_correct:
            self.context['css_class'] = "sol_right"
            self.context['printed_solution'] = "OK"
        else:
            self.context['css_class'] = "sol_wrong"
            self.context['printed_solution'] = \
                                self.solution.get_printed_solution()


class GapText(QuestionSegment):
    """
    Models a text with gaps
    implements its own rendering and solution_handling methods
    """
    template = 'tasks/gaptext.html'

    def __init__(self, dc):
        super(GapText, self).__init__(dc)
        assert isinstance(dc.content, unicode)
        self.raw_text = dc.content
        self.idx = dc.idx


        self.render_text_with_fields()
        self.make_context()

    def render_text_with_fields(self, css=None, sol=None):
        """
        render the gap-fill-text
        :css: optional list of addtional css classes
              (eg. "gap_right or "gap_wrong")
        :sol: optional list of print_solutions
        """
        N = len(self.solution.parts)

        field_data_list = self._get_field_data()
        assert len(field_data_list) == N

        if css is None:
            css = ['']*N
        assert len(css) == N
        css_list = ["gap {add}".format(add=c).strip() for c in css]

        if not sol is None:
            assert len(sol) == N
            prefill_list = sol
        else:
            prefill_list = [fd.answer for fd in field_data_list]

        field_str = "<input class='{css_class}' type='text' "\
                            "size='{length}' value='{prefill}' name='{name}'>"

        rendered_fields = []
        for fd, css, pf in zip(field_data_list, css_list, prefill_list):
            tmp = field_str.format(css_class=css, length=fd.longest_solution,
                                              prefill=pf, name=fd.name)
            rendered_fields.append(tmp)

        pattern = r"(&para;).*?\1"
        text = reduce(lambda x, y: re.sub(pattern, str(y), x, 1), rendered_fields, self.raw_text)

        self.c_text = text
        return text

    def _get_field_data(self):
        """
        assembles the data (name, length, default value) for every field of
        the gap text
        """

        # we need the length of the solution-strings for the input fields
        field_data_list = []
        for i, part in enumerate(self.solution.parts):

            field_data = DictContainer()
            field_data.answer = part.answer

            sol_lengths = [len(sol.content) for sol in part]
            field_data.longest_solution = max(sol_lengths)

            field_data.name = \
                            "answer_{idx}:{part}".format(idx =self.idx, part=i)

            field_data_list.append(field_data)
        return field_data_list


    def update_user_solution(self, sol_dict):
        """
        This function decides whether the users answer was correct and
        sets the respective attributes (css_class, printed_solution)

        special version for gap-fill-text
        """

        # get the matching solution for this segment
        start = "{idx}:".format(idx = self.idx)
        user_solutions = [(k, v) for k,v in sol_dict.items() \
                                                if k.startswith(start)]

        user_solutions.sort(key = lambda t:t[0])
        keys, sol_values = zip(*user_solutions)


        assert len(sol_values) == len(self.solution.parts)
        sol_lists = [[dc.content for dc in p] for p in self.solution.parts]
        user_results = [sv in sl for sv, sl in zip(sol_values, sol_lists)]

        css = ['gap_right' if r else "gap_wrong" for r in user_results]
        printed_solutions = self.solution.get_printed_solution()

        # write the detail information directly into the text
        txt = self.render_text_with_fields(css, printed_solutions)
        self.context['text'] = txt


class InputField(QuestionSegment):
    template = 'tasks/cq2_input_field.html'

    def __init__(self, dc):

        assert isinstance(dc.content, list)
        self.c_text_slots = None
        self.make_description_cells(dc.content)

        self.c_lines = len(dc.answer.content.splitlines())
        if self.c_lines == 0:
            self.c_lines = 1

        self.c_prefilled_text = dc.answer.content
        self.c_answer_class = dc.answer.type

        if type(dc.solution) == list:
            self.c_solution_class = dc.solution[0].type
        else:
            self.c_solution_class = dc.solution.type

        super(InputField, self).__init__(dc)

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
        super(CBox, self).__init__(dc)


# TODO: implement Radio type
class RadioList(QuestionSegment):
    pass


# our json format "specification" by example
# https://gist.github.com/leberwurstsaft/7158911


def preprocess_task_from_db(task):
    """
    this function takes a task object, coming from the database

    * it parses the json and stores the result in .segment_list
    * it sets the .solution_flag to False

    """

    body_data = json.loads(task.body_data)

    dict_list = body_data['segments']

    question_counter[0] = 0
    task.segment_list = [make_segment(segment_dict, idx) for idx, segment_dict in enumerate(dict_list)]
    task.solution_flag = False

    return None
