#!/usr/bin/env python

from __future__ import print_function
from collections import namedtuple
import collections
import os
import json
import sys

# given a number num, generate space of size length
def indent_count_to_string(num):
    s = ""
    for i in range(0, num):
        s = s + "  "
    return s

# the AST for the command line structure
class Program(object):
    def __init__(self, commands):
        self.parent = self
        self.commands = commands
        for cmd in self.commands:
            setattr(cmd, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[Program]" + "\n"
        for c in self.commands:
            result = result + c.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()
    def next_node(self, looked): 
    # what is the next node after visiting this node
        next = []
        next.append("<DONE>")
        for cmd in self.commands:
            if not cmd in looked:
                next.append(*cmd.get_node(looked))
        return next
    def get_node(self, looked): 
    # get the first terminal value starting from this node
        return self.next_node(looked)
    def leave_node(self, looked, last): 
    # after traveral all subtress of this node, seek the next tree to traverse
        return self.next_node(looked)

class Cmd(object):
    def __init__(self, name, option):
        self.name = name
        self.option = option
        setattr(self.option, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[Cmd] " + self.name + "\n"
        result = result +  self.option.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()
    def next_node(self, looked):
        looked.append(self)
        return self.option.get_node(looked)
    def get_node(self, looked):
        return [self]
    def leave_node(self, looked, last):
        looked.append(self)
        return self.parent.leave_node(looked, Cmd)
    def __str__(self):
        return self.name

class FlagOp(object):
    def __init__(self, name):
        self.name = name
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[FlagOp] " + self.name
        return result
    def get_node(self, looked):
        return [self]
    def next_node(self, looked):
        if not self in looked:
            looked.append(self)
        return self.leave_node(looked, self)
    def leave_node(self, looked, last):
        looked.append(self)
        return self.parent.leave_node(looked, self)
    def __str__(self):
        return self.name

class LongFlagOp(object):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg
        if (not self.arg == None):
            setattr(self.arg, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[LongFlagOp] " + self.name + "\n"
        if (not self.arg == None):
            result = result + self.arg.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()
    def get_node(self, looked):
        return [self]
    def next_node(self, looked):
        looked.append(self)
        if not self.arg == None:
            return self.arg.get(looked)
        else:
            return self.leave_node(looked, self)
    def leave_node(self, looked, last):
        looked.append(self)
        return self.parent.leave_node(looked, self)
    def __str__(self):
        return self.name

class ArgOp(object):
    def __init__(self, name, ty, is_list):
        self.name = name
        self.ty = ty
        self.is_list = is_list
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[ArgOp] " + self.name 
        return result.rstrip()
    def get_node(self, looked):
        return [self]
    def next_node(self, looked):
        #TODO: allow a list of file
        looked.append(self)
        result = []
        #if self.is_list:
        #    result.append(self)
        result.extend(self.leave_node(looked, self))
        return result
    def leave_node(self, looked, last):
        looked.append(self)
        return self.parent.leave_node(looked, self)
    def __str__(self):
        return self.name

class OptionalOp(object):
    def __init__(self, option):
        self.option = option
        setattr(self.option, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[OptionalOp]" + "\n"
        result = result + self.option.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()
    def get_node(self, looked):
        return self.next_node(looked)
    def next_node(self, looked):
        looked.append(self)
        result = []
        result.extend(self.option.get_node(looked))        
        result.extend(self.leave_node(looked, self))
        return result
    def leave_node(self, looked, last):
        looked.append(self)
        return self.parent.leave_node(looked, self)

class SeqOp(object):
    def __init__(self, options):
        self.options = options
        for option in self.options:
            setattr(option, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[SeqOp]" + "\n" 
        for c in self.options:
            result = result + c.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()
    def get_node(self, looked):
        return self.next_node(looked)
    def next_node(self, looked):
        looked.append(self)
        if self.options[-1] in looked:
            return self.leave_node(looked, self)
        last = self.options[-1]
        for cmd in reversed(self.options):
            if cmd in looked:
                return last.get_node(looked)
            last = cmd
        return last.get_node(looked)
    def leave_node(self, looked, last):
        looked.append(self)
        if last == self:
            return self.parent.leave_node(looked, last)
        return self.next_node(looked)

class CaseOp(object):
    def __init__(self, options):
        self.options = options
        for option in self.options:
            setattr(option, "parent", self)
    def pretty_print(self, indent_count):
        indent = indent_count_to_string(indent_count)
        result = indent + "[CaseOp]" + "\n"
        for c in self.options:
            result = result + c.pretty_print(indent_count + 1) + "\n"
        return result.rstrip()
    def get_node(self, looked):
        return self.next_node(looked)
    def next_node(self, looked):
        looked.append(self)
        result = []
        for x in self.options:
            result.extend(x.get_node(looked))
        return result
    def leave_node(self, looked, last):
        looked.append(self)
        return self.parent.leave_node(looked, self)

# classes to build tree from json file
def load_syntax(json_files):
    simple_cmds = []
    counts = collections.defaultdict(int)
    for jsonfile in json_files:
        print("loading from {}".format(jsonfile))
        with open(jsonfile, "r") as f:
            syntax = json.loads(f.read())
        for cmd in syntax:
            c = make_grammar_from_json_syntax(cmd)
            simple_cmds.append(c)
            counts[cmd["name"]] += 1
            print(" > loaded {} ({})".format(cmd["name"], counts[cmd["name"]]))
    return Program(simple_cmds)

def make_grammar_from_json_syntax(syntax):
    g = Cmd(name=syntax["name"], option=make_grammar_from_options(syntax["option"]))
    return g

def make_grammar_from_options(x):
    if x["type"] == "compound_options":
        return SeqOp([make_grammar_from_options(o) for o in x["commands"]])
    elif x["type"] == "optional_option":
        return OptionalOp(make_grammar_from_options(x["cmd"]))
    elif x["type"] == "exclusive_options":
        return CaseOp([make_grammar_from_options(o) for o in x["commands"]])
    elif x["type"] == "flag_option":
        return FlagOp(x["flag_name"])
    elif x["type"] == "long_flag_option":
        g = LongFlagOp(x["flag_name"], None)
        if x["arg_exists"]:
            if x["arg_optional"]:
                setattr(g, "arg", OptionalOp(make_grammar_from_options(x["argument"])))
            else:
                setattr(g, "arg", make_grammar_from_options(x["argument"]))
        return g
    elif x["type"] == "argument_option":
        return ArgOp(x["arg_name"], x["arg_type"], x["isList"])
    else:
        raise Exception("unknown type: {}".format(x["type"]))
    return g

# the enumerator class
class Enumerator(object):
    def __init__(self, grammar):
        self.grammar = grammar
        self.history = [grammar]
    def step_back(self):
        if len(self.history) > 1:
        #check whether the list is empty 
            self.history.pop()
    def choices(self):
        # use list to avoid the argument being the alias of history
        return self.history[-1].next_node(list(self.history))
    def make_choice(self, i):
        self.history.append(self.choices()[i]);
    # the return value should be a list of indices
    def choice_indices(self, text):
        choice_list = self.choices()
        indices = []
        for i, x in enumerate(choice_list):
            if str(x) == text:
                indices.append(i)
        return indices
    def deepcopy(self):
        enum = Enumerator(self.grammar)
        enum.history = list(self.history)
        return enum

class Interface(object):
    def __init__(self, grammar):
        self.enumerators = []
        self.enumerators.append(Enumerator(grammar))
    def text_choices(self):
        text_choices = []
        for enumerator in self.enumerators:
            for state in enumerator.choices():
                if not any(x == str(state) for x in text_choices):
                    text_choices.append(str(state))
        return text_choices
    def make_choice(self, input):
        if not input in self.text_choices():
            raise NameError("[" + input + "]" + ' is not a valid choice')
        new_enumerators = []
        for enumerator in self.enumerators:
            indices = enumerator.choice_indices(input)
            for i in indices:
                e = enumerator.deepcopy()
                e.make_choice(i)
                new_enumerators.append(e)
        self.enumerators = new_enumerators
    def is_valid_choice(self, example):
        return (example in self.text_choices())

if __name__ == "__main__":
    g = load_syntax([os.path.join(os.path.dirname(__file__), "..", "data", "primitive_cmds_grammar.json")])
    interface = Interface(g)
    while True:
        print("choices: {}".format(", ".join(interface.text_choices())))
        try:
            inp = raw_input("> ")
            if inp == "<DONE>" and interface.is_valid_choice("<DONE>"):
                break
            interface.make_choice(inp)
        except EOFError as ex:
            break
