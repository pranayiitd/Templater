from Errors import TemplateContextError, TemplateSyntaxError

class Node(object):
	
	def __init__(self, token):
		"""Intialize the node of tree with proper meta data
			keeping the grammer in mind.
		"""
		self.children =[]
		self.raw = token
		self.type, self.fragment = self.process_fragment(token)
		self.scope = self.set_scope(token)

	def process_fragment(self, token):
		"""
			Process the token to remove unnecessary whitespace
			and syntax sugar.
		"""
		if(token.find("<*") == -1):
			return "HTML", token
		else:
			try:
				fragment = token[2:-2].strip()
			except:
				raise TemplateSyntaxError(token)

			if(token.find("EACH") == -1):			
				return "VAR", fragment
			else:
				if(token.find("END") == -1):
					return "EACH", fragment
				else:
					return "END", fragment

	def set_scope(self, token):
		"""Returns true if the element can create
		   scope for the program. eg: FOR, if, Else etc.
		"""
		if(token.find("EACH") > -1):
			return True
		else:
			return False


def build_tree(tokens):
	"""Builds the Abstract Syntax Tree for the source
	   code using the tokens
	"""
	root = Node("root")
	scope_stack = [root]

	for token in tokens:
		new_node = Node(token)
		if(new_node.type == "END"):
			scope_stack.pop()
			continue

		parent_node = scope_stack[-1]
		parent_node.children.append(new_node)
		if(new_node.scope):
			scope_stack.append(new_node)
	return root


def render_html(root, scope_context):
	s = ""
	for child in root.children:
		s += resolve(child, scope_context)
	return s

def resolve(node, scope_context):
	"""Spits out html for the AST subtree
		under node.
	"""
	if(node.type == "END"):
		return
	elif(node.type == "HTML"):
		return node.fragment
	else:
		if(node.type == "VAR"):
			ref = node.fragment.split(".")
			return deRefer(ref, scope_context, 0)
		else:
			# EACH type
			# <* EACH varArray it *>
			loop = node.fragment.split(" ")

			# Dereferencing from the current scope context
			varArray = deRefer(loop[1].strip().split('.'), scope_context, 0)
			it  = loop[2]
			s = ""
			for var in varArray:
				# Adding the correct symbol mapping in the current
				# context scope.
				scope_context[it] = var
				for child in node.children:
					s += resolve(child, scope_context)
				scope_context.pop(it)
			return s

def deRefer(ref, context, i):
	if(len(ref) == i):
		return context
	else:
		try:
			ret = deRefer(ref, context[ref[i]], i+1)
		except KeyError:
			raise TemplateContextError(ref)
		return ret	