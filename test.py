import re
import ast
import json
from Node import Node

VAR_TOKEN_START = '<\*'
VAR_TOKEN_END = '\*>'
TOK_REGEX = re.compile(r"(%s.*?%s)" % (
    VAR_TOKEN_START,
    VAR_TOKEN_END
))


f = open("template.panoramatemplate", "r")
s = f.read();
f.close()
arr = TOK_REGEX.split(s)

f = open("data.json", "r")
data = f.read()
f.close()
scope_context = json.loads(data)

root = Node("root")
scope_stack = [root]

for elem in arr:
	
	if(elem.find("END") > 0):
		scope_stack.pop()
		continue
	
	parent_node = scope_stack[-1]
	new_node = Node(elem)
	parent_node.children.append(new_node)
	if(new_node.fragment.find("EACH") > -1):
		scope_stack.append(new_node)


def solve(ref, context, i):
	if(len(ref) == i):
		return context
	else:
		return solve(ref, context[ref[i]], i+1)


def render(root):
	s = ""
	for child in root.children:
		s += resolve(child, scope_context)
	print s
	print scope_context

def resolve(node, scope_context):
	"""pass"""
	if(node.fragment.find("<*") == -1):
		return node.fragment
	else:
		if(node.fragment.find("EACH") == -1):
			ref = node.fragment[2:-2].strip().split(".")
			return solve(ref, scope_context, 0)
		else:
			loop = node.fragment[2:-2].strip().split(" ")
			var = solve(loop[1].strip().split('.'), scope_context, 0)
			it  = loop[2]
			s = ""
			for i in var:
				scope_context[it] = i
				for child in node.children:
					s += resolve(child, scope_context)
				scope_context.pop(it)
			return s


render(root)