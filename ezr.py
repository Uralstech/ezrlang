from vendor.string_with_underline import str_w_undln
from os import path, system, name, getcwd
from string import ascii_letters
from importlib import util

# CONSTANTS

VERSION = '1.24.0.1.0'
VERSION_DATE = '28-09-2022'
DIGITS = '0123456789'
LETTERS = ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
LIB_PATH = path.join(path.dirname(path.abspath(__file__)), 'Libraries')

# ERRORS

class Error:
	def __init__(self, err_name, start_pos, end_pos, details):
		self.err_name = err_name
		self.start_pos = start_pos
		self.end_pos = end_pos
		self.details = details

	def as_string(self):
		return f'{self.err_name}: {self.details} (FILE {self.start_pos.fn} | LINE {self.start_pos.ln+1})\n\n{str_w_undln(self.start_pos.ftxt, self.start_pos, self.end_pos)}'

class UnkownCharError(Error):
	def __init__(self, start_pos, end_pos, details):
		super().__init__('UNKNOWN CHARACTER', start_pos, end_pos, details)

class InvalidSyntaxError(Error):
	def __init__(self, start_pos, end_pos, details):
		super().__init__('INVALID SYNTAX', start_pos, end_pos, details)
		
RTE_DEFAULT        = 'RUNTIME'
RTE_CUSTOM         = 'CUSTOM'
RTE_ILLEGALOP      = 'ILLEGAL-OPERATION'
RTE_UNDEFINEDVAR   = 'UNDEFINED-VAR'
RTE_IDXOUTOFRANGE  = 'INDEX-OUT-OF-RANGE'
RTE_TOOMANYARGS    = 'TOO-MANY-FUNCTION-ARGS'
RTE_TOOFEWARGS     = 'TOO-FEW-FUNCTION-ARGS'
RTE_INCORRECTTYPE  = 'INCORRECT-TYPE'
RTE_MATH		   = 'MATH'
RTE_IO	   		   = 'IO'

class RuntimeError(Error):
	def __init__(self, start_pos, end_pos, error_type, details, context):
		super().__init__('RUNTIME ERROR', start_pos, end_pos, details)
		self.error_type = error_type
		self.context = context

	def as_string(self):
		return f'{self.generate_traceback()}{self.err_name}: {self.details}\n\n{str_w_undln(self.start_pos.ftxt, self.start_pos, self.end_pos)}'

	def generate_traceback(self):
		result = ''
		pos = self.start_pos
		context = self.context

		while context:
			result = f'\tFILE {pos.fn} | LINE {str(pos.ln+1)} | IN {context.display_name}\n{result}'
			pos = context.parent_entry_pos
			context = context.parent

		return f'TRACEBACK (MOST RECENT CALL LAST):\n{result}'

# POSITION

class Position:
	def __init__(self, idx, ln, col, fn, ftxt):
		self.idx = idx
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt

	def advance(self, current_char=None):
		self.idx += 1
		self.col += 1

		if current_char == '\n':
			self.ln += 1
			self.col = 0

		return self

	def copy(self):
		return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

# TOKEN

TT_INT     = 'INT'
TT_FLOAT   = 'FLOAT'
TT_STRING  = 'STRING'
TT_ID      = 'ID'
TT_KEY     = 'KEY'
TT_PLUS    = 'PLUS'
TT_MINUS   = 'MINUS'
TT_MUL     = 'MUL'
TT_DIV     = 'DIV'
TT_MOD     = 'MOD'
TT_POW     = 'POW'
TT_EQLS    = 'EQUALS'
TT_LPAREN  = 'LPAREN'
TT_RPAREN  = 'RPAREN'
TT_LSQUARE = 'LSQUARE'
TT_RSQUARE = 'RSQUARE'
TT_EE      = 'IE'
TT_NE      = 'NE'
TT_LT      = 'LT'
TT_GT      = 'GT'
TT_LTE     = 'LTE'
TT_GTE     = 'GTE'
TT_COMMA   = 'COMMA'
TT_DOT     = 'DOT'
TT_NEWLINE = 'NEWLINE'
TT_EOF     = 'EOF'

KEYWORDS = ['ITEM', 'AND', 'OR', 'INVERT', 'IF', 'ELSE', 'DO', 'COUNT', 'FROM', 'AS', 'TO', 'STEP', 'WHILE', 'FUNCTION', 'WITH', 'END', 'RETURN', 'SKIP', 'STOP', 'TRY', 'ERROR', 'IN', 'OBJECT', 'GLOBAL', 'INCLUDE']

class Token:
	def __init__(self, type_, value=None, start_pos=None, end_pos=None):
		self.type = type_
		self.value = value

		if start_pos:
			self.start_pos = start_pos.copy()
			self.end_pos = start_pos.copy()
			self.end_pos.advance()
		if end_pos: self.end_pos = end_pos

	def matches(self, type_, value):
		return self.type == type_ and self.value == value

	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'

# LEXER

class Lexer:
	def __init__(self, fn, input_):
		self.fn = fn
		self.input = input_
		self.pos = Position(-1, 0, -1, fn, input_)
		self.current_char = None
		self.advance()

	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.input[self.pos.idx] if self.pos.idx < len(self.input) else None

	def compile_tokens(self):
		tokens = []

		while self.current_char != None:
			if self.current_char in ' \t':
				self.advance()
			elif self.current_char == '@':
				self.skip_comment()
			elif self.current_char in ';\n':
				tokens.append(Token(TT_NEWLINE, start_pos=self.pos))
				self.advance()
			elif self.current_char == '\'' or self.current_char == '"':
				tokens.append(self.compile_string())
			elif self.current_char == '+':
				tokens.append(Token(TT_PLUS, start_pos=self.pos))
				self.advance()
			elif self.current_char == '-':
				tokens.append(Token(TT_MINUS, start_pos=self.pos))
				self.advance()
			elif self.current_char == '*':
				tokens.append(Token(TT_MUL, start_pos=self.pos))
				self.advance()
			elif self.current_char == '/':
				tokens.append(Token(TT_DIV, start_pos=self.pos))
				self.advance()
			elif self.current_char == '%':
				tokens.append(Token(TT_MOD, start_pos=self.pos))
				self.advance()
			elif self.current_char == '^':
				tokens.append(Token(TT_POW, start_pos=self.pos))
				self.advance()
			elif self.current_char == ':':
				tokens.append(Token(TT_EQLS, start_pos=self.pos))
				self.advance()
			elif self.current_char == '(':
				tokens.append(Token(TT_LPAREN, start_pos=self.pos))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(TT_RPAREN, start_pos=self.pos))
				self.advance()
			elif self.current_char == '[':
				tokens.append(Token(TT_LSQUARE, start_pos=self.pos))
				self.advance()
			elif self.current_char == ']':
				tokens.append(Token(TT_RSQUARE, start_pos=self.pos))
				self.advance()
			elif self.current_char == '=':
				tokens.append(Token(TT_EE, start_pos=self.pos))
				self.advance()
			elif self.current_char == '!':
				tokens.append(Token(TT_NE, start_pos=self.pos))
				self.advance()
			elif self.current_char == ',':
				tokens.append(Token(TT_COMMA, start_pos=self.pos))
				self.advance()
			elif self.current_char == '.':
				tokens.append(Token(TT_DOT, start_pos=self.pos))
				self.advance()
			elif self.current_char == '<':
				tokens.append(self.compile_less_than())
			elif self.current_char == '>':
				tokens.append(self.compile_greater_than())
			elif self.current_char in DIGITS:
				tokens.append(self.compile_num())
			elif self.current_char in LETTERS:
				tokens.append(self.compile_identifier())
			else:
				pos_start = self.pos.copy()
				char = self.current_char
				self.advance()
				return [], UnkownCharError(pos_start, self.pos, f"'{char}'")

		tokens.append(Token(TT_EOF, start_pos=self.pos))
		return tokens, None

	def compile_string(self):
		string_to_return = ''
		start_pos = self.pos.copy()
		escape_char = False
		string_char = self.current_char
		self.advance()

		escape_chars = {'n':'\n', 't':'\t'}
		while self.current_char != None and (self.current_char != string_char or escape_char):
			if escape_char:
				string_to_return += escape_chars.get(self.current_char, self.current_char)
				escape_char = False
			else:
				if self.current_char == '\\':
					escape_char = True
				else:
					string_to_return += self.current_char

			self.advance()
		
		self.advance()
		return Token(TT_STRING, string_to_return, start_pos, self.pos)

	def compile_less_than(self):
		start_pos = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			return Token(TT_LTE, start_pos=start_pos, end_pos=self.pos)
		
		return Token(TT_LT, start_pos=start_pos, end_pos=self.pos)

	def compile_greater_than(self):
		start_pos = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			return Token(TT_GTE, start_pos=start_pos, end_pos=self.pos)
		
		return Token(TT_GT, start_pos=start_pos, end_pos=self.pos)

	def compile_identifier(self):
		id_str = ''
		start_pos = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
			id_str += self.current_char
			self.advance()

		token_type = TT_KEY if id_str in KEYWORDS else TT_ID
		return Token(token_type, id_str, start_pos, self.pos)

	def compile_num(self):
		num_str = ''
		dot_count = 0
		start_pos = self.pos.copy()

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1

			num_str += self.current_char
			self.advance()

		if dot_count == 0: return Token(TT_INT, int(num_str), start_pos, self.pos)
		else: return Token(TT_FLOAT, float(num_str), start_pos, self.pos)

	def skip_comment(self):
		self.advance()
		while self.current_char != '\n' and self.current_char != None: self.advance()

# NODES

class NumberNode:
	def __init__(self, token):
		self.token = token

		self.start_pos = token.start_pos
		self.end_pos = token.end_pos

	def __repr__(self):
		return f'{self.token}'

class StringNode:
	def __init__(self, token):
		self.token = token

		self.start_pos = token.start_pos
		self.end_pos = token.end_pos

	def __repr__(self):
		return f'{self.token}'

class ListNode:
	def __init__(self, element_nodes, start_pos, end_pos):
		self.element_nodes = element_nodes
		self.start_pos = start_pos
		self.end_pos = end_pos

class VarAccessNode:
	def __init__(self, var_name_token):
		self.var_name_token = var_name_token

		self.start_pos = self.var_name_token.start_pos
		self.end_pos = self.var_name_token.end_pos

class VarAssignNode:
	def __init__(self, var_name_token, value_node, is_global):
		self.var_name_token = var_name_token
		self.value_node = value_node
		self.is_global = is_global

		self.start_pos = self.var_name_token.start_pos
		self.end_pos = self.var_name_token.end_pos

class BinOpNode:
	def __init__(self, left_node, operator_token, right_node):
		self.left_node = left_node
		self.operator_token = operator_token
		self.right_node = right_node

		self.start_pos = self.left_node.start_pos
		self.end_pos = self.right_node.end_pos

	def __repr__(self):
		return f'({self.left_node}, {self.operator_token}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, operator_token, node):
		self.operator_token = operator_token
		self.node = node
		
		self.start_pos = operator_token.start_pos
		self.end_pos = node.end_pos

	def __repr__(self):
		return f'({self.operator_token}, {self.node})'

class IfNode:
	def __init__(self, cases, else_case):
		self.cases = cases
		self.else_case = else_case

		self.start_pos = self.cases[0][0].start_pos
		self.end_pos = (self.else_case or self.cases[len(self.cases)-1])[0].end_pos

class CountNode:
	def __init__(self, var_name_token, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
		self.var_name_token = var_name_token
		self.start_value_node = start_value_node
		self.end_value_node = end_value_node
		self.step_value_node = step_value_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.start_pos = self.var_name_token.start_pos
		self.end_pos = self.body_node.end_pos

class WhileNode:
	def __init__(self, condition_node, body_node, should_return_null):
		self.condition_node = condition_node
		self.body_node = body_node
		self.should_return_null = should_return_null

		self.start_pos = self.condition_node.start_pos
		self.end_pos = self.body_node.end_pos

class TryNode:
	def __init__(self, body_node, catches, should_return_null, start_pos, end_pos):
		self.body_node = body_node
		self.catches = catches
		self.should_return_null = should_return_null

		self.start_pos = start_pos
		self.end_pos = end_pos

class FuncDefNode:
	def __init__(self, var_name_token, arg_name_tokens, body_node, should_auto_return):
		self.var_name_token = var_name_token
		self.arg_name_tokens = arg_name_tokens
		self.body_node = body_node
		self.should_auto_return = should_auto_return

		if self.var_name_token:
			self.start_pos = self.var_name_token.start_pos
		elif len(self.arg_name_tokens) > 0:
			self.start_pos = self.arg_name_tokens[0].start_pos
		else:
			self.start_pos = self.body_node.start_pos
		self.end_pos = self.body_node.end_pos

class ObjectDefNode:
	def __init__(self, var_name_token, arg_name_tokens, body_node):
		self.var_name_token = var_name_token
		self.arg_name_tokens = arg_name_tokens
		self.body_node = body_node

		self.start_pos = self.var_name_token.start_pos
		self.end_pos = self.body_node.end_pos

class CallNode:
	def __init__(self, node_to_call, arg_nodes):
		self.node_to_call = node_to_call
		self.arg_nodes = arg_nodes

		self.start_pos = self.node_to_call.start_pos
		if len(self.arg_nodes) > 0:
			self.end_pos = self.arg_nodes[len(self.arg_nodes)-1].end_pos
		else:
			self.end_pos = self.node_to_call.end_pos

class ObjectCallNode:
	def __init__(self, object_node, node_to_call):
		self.object_node = object_node
		self.node_to_call = node_to_call

		self.start_pos = self.object_node.start_pos
		self.end_pos = self.node_to_call.end_pos

class IncludeNode:
	def __init__(self, name_node, nickname_node):
		self.name_node = name_node
		self.nickname_node = nickname_node

		self.start_pos = self.name_node.start_pos
		self.end_pos = nickname_node.end_pos if nickname_node else self.name_node.end_pos

class ReturnNode:
	def __init__(self, node_to_return, start_pos, end_pos):
		self.node_to_return = node_to_return

		self.start_pos = start_pos
		self.end_pos = end_pos

class SkipNode:
	def __init__(self, start_pos, end_pos):
		self.start_pos = start_pos
		self.end_pos = end_pos

class StopNode:
	def __init__(self, start_pos, end_pos):
		self.start_pos = start_pos
		self.end_pos = end_pos


# PARSE RESULT

class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.advance_count = 0
		self.to_reverse_count = 0

	def register_advance(self):
		self.advance_count += 1

	def register(self, res):
		self.advance_count += res.advance_count
		if res.error: self.error = res.error
		return res.node

	def try_register(self, res):
		if res.error:
			self.to_reverse_count = res.advance_count
			return None
		return self.register(res)

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		if not self.error or self.advance_count == 0:
			self.error = error
		return self

# PARSER

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.token_idx = -1
		self.current_token = None
		self.advance()

	def advance(self):
		self.token_idx += 1
		self.update_current_token()
		return self.current_token

	def reverse(self, amount=1):
		self.token_idx -= amount
		self.update_current_token()
		return self.current_token

	def update_current_token(self):
		if self.token_idx >= 0 and self.token_idx < len(self.tokens):
			self.current_token = self.tokens[self.token_idx]

	def parse(self):
		res = self.statements()
		if not res.error and self.current_token.type != TT_EOF: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'+\', \'-\', \'*\', \'/\', \'^\' or \'%\''))
		return res

	def statements(self):
		res = ParseResult()
		statements = []
		start_pos = self.current_token.start_pos.copy()

		while self.current_token.type == TT_NEWLINE:
			res.register_advance()
			self.advance()
		
		statement = res.register(self.statement())
		if res.error: return res
		statements.append(statement)

		more_statements = True
		while True:
			newline_count = 0
			while self.current_token.type == TT_NEWLINE:
				res.register_advance()
				self.advance()
				newline_count += 1

			if newline_count == 0:
				more_statements = False
			
			if not more_statements: break
			statement = res.try_register(self.statement())
			if not statement:
				self.reverse(res.to_reverse_count)
				more_statements = False
				continue

			statements.append(statement)

		return res.success(ListNode(statements, start_pos, self.current_token.end_pos.copy()))

	def statement(self):
		res = ParseResult()
		start_pos = self.current_token.start_pos.copy()

		if self.current_token.matches(TT_KEY, 'RETURN'):
			res.register_advance()
			self.advance()

			expression = res.try_register(self.expression())
			if not expression: self.reverse(res.to_reverse_count)
			return res.success(ReturnNode(expression, start_pos, self.current_token.start_pos.copy()))
		elif self.current_token.matches(TT_KEY, 'SKIP'):
			res.register_advance()
			self.advance()
			return res.success(SkipNode(start_pos, self.current_token.start_pos.copy()))
		elif self.current_token.matches(TT_KEY, 'STOP'):
			res.register_advance()
			self.advance()
			return res.success(StopNode(start_pos, self.current_token.start_pos.copy()))
		
		expression = res.register(self.expression())
		if res.error: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [INT], [FLOAT], [IDENTIFIER], \'ITEM\', \'IF\', \'COUNT\', \'WHILE\', \'FUNCTION\', \'RETURN\', \'SKIP\', \'STOP\', \'+\', \'-\', \'(\' or \'[\''))
		return res.success(expression)

	def expression(self):
		res = ParseResult()

		is_global = False
		if self.current_token.matches(TT_KEY, 'GLOBAL'):
			is_global = True
			res.register_advance()
			self.advance()

		if self.current_token.matches(TT_KEY, 'ITEM'):
			res.register_advance()
			self.advance()

			if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected identifier'))

			var_name = self.current_token
			res.register_advance()
			self.advance()

			if self.current_token.type != TT_EQLS: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \':\''))
			res.register_advance()
			self.advance()

			expression = res.register(self.expression())
			if res.error: return res
			return res.success(VarAssignNode(var_name, expression, is_global))
		elif is_global: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'ITEM\''))
		
		node = res.register(self.binary_operation(self.comp_expr, ((TT_KEY, 'AND'), (TT_KEY, 'OR'))))
		if res.error: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [INT], [FLOAT], [IDENTIFIER], \'ITEM\', \'IF\', \'COUNT\', \'WHILE\', \'FUNCTION\', \'+\', \'-\', \'(\' or \'[\''))
		return res.success(node)

	def comp_expr(self):
		res = ParseResult()

		if self.current_token.matches(TT_KEY, 'INVERT'):
			operator_token = self.current_token
			res.register_advance()
			self.advance()

			node = res.register(self.comp_expr())
			if res.error: return res
			return res.success(UnaryOpNode(operator_token, node))
		
		node = res.register(self.binary_operation(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
		if res.error: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [INT], [FLOAT], [IDENTIFIER], \'INVERT\', \'+\', \'-\', \'(\' or \'[\''))
		return res.success(node)

	def arith_expr(self):
		return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))

	def term(self):
		return self.binary_operation(self.factor, (TT_MUL, TT_DIV, TT_MOD))

	def factor(self):
		res = ParseResult()
		token = self.current_token

		if token.type in (TT_PLUS, TT_MINUS):
			res.register_advance()
			self.advance()
			factor = res.register(self.factor())

			if res.error: return res
			return res.success(UnaryOpNode(token, factor))

		return self.power()
	
	def power(self):
		return self.binary_operation(self.in_expr, (TT_POW, ), self.factor)

	def in_expr(self):
		return self.binary_operation(self.object_call, ((TT_KEY, 'IN'), ), self.object_call)

	def object_call(self):
		res = ParseResult()
		call = res.register(self.call())
		if res.error: return res

		if self.current_token.type == TT_DOT:
			res.register_advance()
			self.advance()

			node_to_call = res.register(self.object_call())
			if res.error: return res

			return res.success(ObjectCallNode(call, node_to_call))
		
		return res.success(call)

	def call(self):
		res = ParseResult()
		atom = res.register(self.atom())
		if res.error: return res

		if self.current_token.type == TT_LPAREN:
			res.register_advance()
			self.advance()
			arg_nodes = []

			if self.current_token.type == TT_RPAREN:
				res.register_advance()
				self.advance()
			else:
				arg_nodes.append(res.register(self.expression()))
				if res.error: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [INT], [FLOAT], [IDENTIFIER], \'ITEM\', \'COUNT\', \'WHILE\', \'FUNCTION\', \'+\', \'-\', \'(\', \'[\', \')\''))

				while self.current_token.type == TT_COMMA:
					res.register_advance()
					self.advance()

					arg_nodes.append(res.register(self.expression()))
					if res.error: return res
				
				if self.current_token.type != TT_RPAREN: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \',\' or \')\''))
				res.register_advance()
				self.advance()
		
			return res.success(CallNode(atom, arg_nodes))
		return res.success(atom)

	def atom(self):
		res = ParseResult()
		token = self.current_token

		if token.type in (TT_INT, TT_FLOAT):
			res.register_advance()
			self.advance()
			return res.success(NumberNode(token))
		elif token.type == TT_STRING:
			res.register_advance()
			self.advance()
			return res.success(StringNode(token))
		elif token.type == TT_ID:
			res.register_advance()
			self.advance()
			return res.success(VarAccessNode(token))
		elif token.type == TT_LPAREN:
			res.register_advance()
			self.advance()
			expression = res.register(self.expression())
			if res.error: return res
			
			if self.current_token.type == TT_RPAREN:
				res.register_advance()
				self.advance()
				return res.success(expression)
			else: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \')\''))
		elif token.type == TT_LSQUARE:
			list_expression = res.register(self.list_expr())
			if res.error: return res
			return res.success(list_expression)
		elif token.matches(TT_KEY, 'IF'):
			if_expression = res.register(self.if_expr()[0])
			if res.error: return res
			return res.success(if_expression)
		elif token.matches(TT_KEY, 'COUNT'):
			count_expression = res.register(self.count_expr())
			if res.error: return res
			return res.success(count_expression)
		elif token.matches(TT_KEY, 'WHILE'):
			while_expression = res.register(self.while_expr())
			if res.error: return res
			return res.success(while_expression)
		elif token.matches(TT_KEY, 'TRY'):
			try_expression = res.register(self.try_expr())
			if res.error: return res
			return res.success(try_expression)
		elif token.matches(TT_KEY, 'FUNCTION'):
			function_expression = res.register(self.function_def())
			if res.error: return res
			return res.success(function_expression)
		elif token.matches(TT_KEY, 'OBJECT'):
			object_expression = res.register(self.object_def())
			if res.error: return res
			return res.success(object_expression)
		elif token.matches(TT_KEY, 'INCLUDE'):
			include_expression = res.register(self.include_expr())
			if res.error: return res
			return res.success(include_expression)
			
		return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [INT], [FLOAT], [IDENTIFIER], \'IF\', \'COUNT\', \'WHILE\', \'FUNCTION\', \'+\', \'-\', \'(\' or \'[\''))

	def list_expr(self):
		res = ParseResult()
		element_nodes = []
		start_pos = self.current_token.start_pos.copy()

		if self.current_token.type != TT_LSQUARE: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'[\'')), None
		res.register_advance()
		self.advance()

		if self.current_token.type == TT_RSQUARE:
			res.register_advance()
			self.advance()
		else:
			while self.current_token.type == TT_NEWLINE: res.register_advance(); self.advance()
				
			element_nodes.append(res.register(self.expression()))
			if res.error: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [INT], [FLOAT], [IDENTIFIER], \'ITEM\', \'COUNT\', \'WHILE\', \'FUNCTION\', \'+\', \'-\', \'(\', \'[\' or \']\''))

			while self.current_token.type == TT_NEWLINE: res.register_advance(); self.advance()
			while self.current_token.type == TT_COMMA:
				res.register_advance()
				self.advance()
				
				while self.current_token.type == TT_NEWLINE: res.register_advance(); self.advance()

				element_nodes.append(res.register(self.expression()))
				if res.error: return res
				
			while self.current_token.type == TT_NEWLINE: res.register_advance(); self.advance()
			if self.current_token.type != TT_RSQUARE: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \',\' or \']\''))
			res.register_advance()
			self.advance()

		return res.success(ListNode(element_nodes, start_pos, self.current_token.end_pos.copy()))

	def if_expr(self, secondary_call=False):
		res = ParseResult()
		cases = []
		else_case = None
		has_ended = False

		if not self.current_token.matches(TT_KEY, 'IF'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'IF\'')), None, has_ended
		res.register_advance()
		self.advance()

		condition = res.register(self.expression())
		if res.error: return res, None, has_ended

		if not self.current_token.matches(TT_KEY, 'DO'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'DO\'')), None, has_ended
		res.register_advance()
		self.advance()

		if self.current_token.type == TT_NEWLINE:
			res.register_advance()
			self.advance()

			statements = res.register(self.statements())
			if res.error: return res, None, has_ended
			cases.append((condition, statements, True))

			if self.current_token.matches(TT_KEY, 'END'):
				has_ended = True
				res.register_advance()
				self.advance()
			else:
				if not self.current_token.matches(TT_KEY, 'ELSE'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'ELSE\' or \'END\'')), None
				res.register_advance()
				self.advance()
            
				if self.current_token.matches(TT_KEY, 'IF'):
					if_expr, added_cases, has_ended = self.if_expr(secondary_call=True)
					res.register(if_expr)
					if res.error: return res, None, has_ended
					cases.extend(added_cases)
            
				if not has_ended and not secondary_call:
					if self.tokens[self.token_idx-1].matches(TT_KEY, 'ELSE'):
						self.reverse()

					if self.current_token.matches(TT_KEY, 'ELSE'):
						res.register_advance()
						self.advance()
	
						if not self.current_token.matches(TT_KEY, 'DO'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'DO\'')), None, has_ended
						res.register_advance()
						self.advance()
	
						else_case = (res.register(self.statements()), True)
						if res.error: return res, None, has_ended

						if not self.current_token.matches(TT_KEY, 'END'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'ELSE\' or \'END\'')), None, has_ended
						res.register_advance()
						self.advance()
					elif not self.current_token.matches(TT_KEY, 'ELSE'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'ELSE\' or \'END\'')), None, has_ended
		else:
			expression = res.register(self.statement())
			if res.error: return res, None, has_ended
			cases.append((condition, expression, False))

			if not secondary_call:
				while self.current_token.matches(TT_KEY, 'ELSE'):
					res.register_advance()
					self.advance()

					if self.current_token.matches(TT_KEY, 'IF'):
						if_expr, added_cases, has_ended = self.if_expr(secondary_call=True)
						res.register(if_expr)
						if res.error: return res, None, has_ended
						cases.extend(added_cases)
					else:
						if not self.current_token.matches(TT_KEY, 'DO'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'DO\'')), None, has_ended
						res.register_advance()
						self.advance()

						else_case = (res.register(self.statement()), False)
						if res.error: return res, None, has_ended

		return res.success(IfNode(cases, else_case)), cases, has_ended

	def count_expr(self):
		res = ParseResult()

		if not self.current_token.matches(TT_KEY, 'COUNT'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'COUNT\''))
		res.register_advance()
		self.advance()

		if not self.current_token.matches(TT_KEY, 'FROM'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'FROM\''))
		res.register_advance()
		self.advance()

		start_value = res.register(self.expression())
		if res.error: return res

		if not self.current_token.matches(TT_KEY, 'AS'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'AS\''))
		res.register_advance()
		self.advance()

		if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER]'))
		var_name = self.current_token
		res.register_advance()
		self.advance()

		if not self.current_token.matches(TT_KEY, 'TO'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'TO\''))
		res.register_advance()
		self.advance()

		end_value = res.register(self.expression())
		if res.error: return res

		if self.current_token.matches(TT_KEY, 'STEP'):
			res.register_advance()
			self.advance()

			step_value = res.register(self.expression())
			if res.error: return res
		else:
			step_value = None
		
		if not self.current_token.matches(TT_KEY, 'DO'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'DO\''))
		res.register_advance()
		self.advance()

		if self.current_token.type == TT_NEWLINE:
			res.register_advance()
			self.advance()
			
			body = res.register(self.statements())
			if res.error: return res
			
			if not self.current_token.matches(TT_KEY, 'END'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'END\''))
			res.register_advance()
			self.advance()
			
			return res.success(CountNode(var_name, start_value, end_value, step_value, body, True))
		else:
			body = res.register(self.statement())
			if res.error: return res
			return res.success(CountNode(var_name, start_value, end_value, step_value, body, False))

	def while_expr(self):
		res = ParseResult()

		if not self.current_token.matches(TT_KEY, 'WHILE'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'WHILE\''))
		res.register_advance()
		self.advance()

		condition = res.register(self.expression())
		if res.error: return res

		if not self.current_token.matches(TT_KEY, 'DO'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'DO\''))
		res.register_advance()
		self.advance()

		if self.current_token.type == TT_NEWLINE:
			res.register_advance()
			self.advance()

			body = res.register(self.statements())
			if res.error: return res

			if not self.current_token.matches(TT_KEY, 'END'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'END\''))
			res.register_advance()
			self.advance()
			
			return res.success(WhileNode(condition, body, True))
		else:
			body = res.register(self.statement())
			if res.error: return res
			return res.success(WhileNode(condition, body, False))

	def try_expr(self):
		res = ParseResult()
		start_pos = self.current_token.start_pos
		body_node = None
		catches = []

		if not self.current_token.matches(TT_KEY, 'TRY'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'TRY\''))
		res.register_advance()
		self.advance()

		if not self.current_token.matches(TT_KEY, 'DO'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'DO\''))
		res.register_advance()
		self.advance()

		if self.current_token.type == TT_NEWLINE:
			res.register_advance()
			self.advance()

			statements = res.register(self.statements())
			if res.error: return res
			body_node = statements

			empty_errors = []
			while self.current_token.matches(TT_KEY, 'ERROR'):
				res.register_advance()
				self.advance()

				error = None
				var_name = None
				if self.current_token.type == TT_STRING:
					error = self.current_token
					res.register_advance()
					self.advance()

				if self.current_token.matches(TT_KEY, 'AS'):
					res.register_advance()
					self.advance()

					if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER]'))
					
					var_name = self.current_token
					res.register_advance()
					self.advance()

				if not self.current_token.matches(TT_KEY, 'DO'):
					if error == None and var_name == None: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [STRING], \'AS\' or \'DO\''))
					elif error != None and var_name == None: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'AS\' or \'DO\''))
					return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'DO\''))
				res.register_advance()
				self.advance()

				expression = res.register(self.statements())
				if res.error: return res

				if error == None: empty_errors.append(len(catches))
				catches.append((error, var_name, expression))

			if len(empty_errors) != 0:
				if len(empty_errors) > 1: return res.failure(InvalidSyntaxError(start_pos, self.current_token.end_pos, 'There cannot be more than one \'empty\' \'ERROR\' statements'))
				if empty_errors[0] != len(catches)-1: return res.failure(InvalidSyntaxError(start_pos, self.current_token.end_pos, 'The \'empty\' \'ERROR\' statement should always be declared last'))

			if not self.current_token.matches(TT_KEY, 'END'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'END\''))
			res.register_advance()
			self.advance()

			return res.success(TryNode(body_node, catches, True, start_pos, self.current_token.end_pos))
		else:
			expression = res.register(self.statement())
			if res.error: return res
			body_node = expression

			empty_errors = []
			while self.current_token.matches(TT_KEY, 'ERROR'):
				res.register_advance()
				self.advance()

				error = None
				var_name = None
				if self.current_token.type == TT_STRING:
					error = self.current_token
					res.register_advance()
					self.advance()

				if self.current_token.matches(TT_KEY, 'AS'):
					res.register_advance()
					self.advance()

					if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER]'))
					
					var_name = self.current_token
					res.register_advance()
					self.advance()

				if not self.current_token.matches(TT_KEY, 'DO'):
					if error == None and var_name == None: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [STRING], \'AS\' or \'DO\''))
					elif error != None and var_name == None: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'AS\' or \'DO\''))
					return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'DO\''))
				res.register_advance()
				self.advance()

				expression = res.register(self.statement())
				if res.error: return res

				if error == None: empty_errors.append(len(catches))
				catches.append((error, var_name, expression))
			
			if len(empty_errors) != 0:
				if len(empty_errors) > 1: return res.failure(InvalidSyntaxError(start_pos, self.current_token.end_pos, 'There cannot be more than one \'empty\' \'ERROR\' statements'))
				if empty_errors[0] != len(catches)-1: return res.failure(InvalidSyntaxError(start_pos, self.current_token.end_pos, 'The \'empty\' \'ERROR\' statement should always be declared last'))

			return res.success(TryNode(body_node, catches, False, start_pos, self.current_token.end_pos))

	def function_def(self):
		res = ParseResult()

		if not self.current_token.matches(TT_KEY, 'FUNCTION'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'FUNCTION\''))
		res.register_advance()
		self.advance()

		if self.current_token.type == TT_ID:
			var_name = self.current_token
			res.register_advance()
			self.advance()
		else:
			var_name = None

		arg_names = []
		if self.current_token.matches(TT_KEY, 'WITH'):
			res.register_advance()
			self.advance()

			if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER]'))
			arg_names.append(self.current_token)
			res.register_advance()
			self.advance()

			while self.current_token.type == TT_COMMA:
				res.register_advance()
				self.advance()

				if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER]'))
				arg_names.append(self.current_token)
				res.register_advance()
				self.advance()
		
			if not self.current_token.matches(TT_KEY, 'DO'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \',\' or \'DO\''))
		else:
			if not self.current_token.matches(TT_KEY, 'DO'):
				if var_name == None: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER], \'WITH\' or \'DO\''))
				else: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'WITH\' or \'DO\''))
		res.register_advance()
		self.advance()

		if self.current_token.type == TT_NEWLINE:
			node_to_return = res.register(self.statements())
			if res.error: return res

			if not self.current_token.matches(TT_KEY, 'END'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'END\''))
			res.register_advance()
			self.advance()

			return res.success(FuncDefNode(var_name, arg_names, node_to_return, False))
		else:
			node_to_return = res.register(self.expression())
			if res.error: return res

			return res.success(FuncDefNode(var_name, arg_names, node_to_return, True))

	def object_def(self):
		res = ParseResult()

		if not self.current_token.matches(TT_KEY, 'OBJECT'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'OBJECT\''))
		res.register_advance()
		self.advance()

		if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER]'))
		var_name = self.current_token
		res.register_advance()
		self.advance()

		arg_names = []
		if self.current_token.matches(TT_KEY, 'WITH'):
			res.register_advance()
			self.advance()

			if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER]'))
			arg_names.append(self.current_token)
			res.register_advance()
			self.advance()

			while self.current_token.type == TT_COMMA:
				res.register_advance()
				self.advance()

				if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER]'))
				arg_names.append(self.current_token)
				res.register_advance()
				self.advance()
		
			if not self.current_token.matches(TT_KEY, 'DO'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \',\' or \'DO\''))
		else:
			if not self.current_token.matches(TT_KEY, 'DO'):
				if var_name == None: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER], \'WITH\' or \'DO\''))
				else: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'WITH\' or \'DO\''))
		res.register_advance()
		self.advance()

		if self.current_token.type == TT_NEWLINE:
			node_to_return = res.register(self.statements())
			if res.error: return res

			if not self.current_token.matches(TT_KEY, 'END'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'END\''))
			res.register_advance()
			self.advance()
		else:
			node_to_return = res.register(self.expression())
			if res.error: return res

		return res.success(ObjectDefNode(var_name, arg_names, node_to_return))

	def include_expr(self):
		res = ParseResult()

		if not self.current_token.matches(TT_KEY, 'INCLUDE'): return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected \'INCLUDE\''))
		res.register_advance()
		self.advance()

		if self.current_token.type != TT_STRING: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [STRING]'))
		name = self.current_token
		res.register_advance()
		self.advance()

		nickname = None
		if self.current_token.matches(TT_KEY, 'AS'):
			res.register_advance()
			self.advance()

			if self.current_token.type != TT_ID: return res.failure(InvalidSyntaxError(self.current_token.start_pos, self.current_token.end_pos, 'Expected [IDENTIFIER]'))
			nickname = self.current_token
			res.register_advance()
			self.advance()
		
		return res.success(IncludeNode(name, nickname))
			
	def binary_operation(self, func_a, ops, func_b=None):
		if func_b == None: func_b = func_a

		res = ParseResult()
		left = res.register(func_a())
		if res.error: return res

		while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
			operator_token = self.current_token
			res.register_advance()
			self.advance()
			right = res.register(func_b())
			if res.error: return res

			left = BinOpNode(left, operator_token, right)

		return res.success(left)

# RUNTIME RESULT

class RuntimeResult:
	def __init__(self):
		self.reset()

	def reset(self):
		self.value = None
		self.error = None
		self.function_return_value = None
		self.loop_should_skip = False
		self.loop_should_stop = False

	def register(self, res):
		if res.error: self.error = res.error
		self.function_return_value = res.function_return_value
		self.loop_should_skip = res.loop_should_skip
		self.loop_should_stop = res.loop_should_stop
		return res.value

	def success(self, value):
		self.reset()
		self.value = value
		return self
	
	def success_return(self, value):
		self.reset()
		self.function_return_value = value
		return self
	
	def success_skip(self):
		self.reset()
		self.loop_should_skip = True
		return self
	
	def success_stop(self):
		self.reset()
		self.loop_should_stop = True
		return self

	def failure(self, error):
		self.reset()
		self.error = error
		return self

	def should_return(self):
		return (self.error or self.function_return_value or self.loop_should_skip or self.loop_should_stop)

# VALUES

class Value:
	def __init__(self):
		self.set_pos()
		self.set_context()

	def set_pos(self, start_pos=None, end_pos=None):
		self.start_pos = start_pos
		self.end_pos = end_pos
		return self

	def set_context(self, context=None):
		self.context = context
		return self
	
	def added_to(self, other):
		return None, self.illegal_operation(other)

	def subbed_by(self, other):
		return None, self.illegal_operation(other)
		
	def multed_by(self, other):
		return None, self.illegal_operation(other)

	def dived_by(self, other):
		return None, self.illegal_operation(other)

	def moded_by(self, other):
		return None, self.illegal_operation(other)

	def powed_by(self, other):
		return None, self.illegal_operation(other)
		
	def compare_eq(self, other):
		return None, self.illegal_operation(other)
		
	def compare_ne(self, other):
		return None, self.illegal_operation(other)
		
	def compare_lt(self, other):
		return None, self.illegal_operation(other)
		
	def compare_gt(self, other):
		return None, self.illegal_operation(other)
		
	def compare_lte(self, other):
		return None, self.illegal_operation(other)
		
	def compare_gte(self, other):
		return None, self.illegal_operation(other)
	
	def compare_and(self, other):
		return None, self.illegal_operation(other)
		
	def compare_or(self, other):
		return None, self.illegal_operation(other)
		
	def check_in(self, other):
		return None, self.illegal_operation(other)
	
	def invert(self):
		return None, self.illegal_operation()

	def execute(self, args):
		return None, self.illegal_operation()

	def retrieve(self, node):
		return None, self.illegal_operation()

	def is_true(self):
		return False

	def copy(self):
		raise Exception('No copy method defined')

	def illegal_operation(self, other=None):
		if not other: other = self
		return RuntimeError(self.start_pos, self.end_pos, RTE_ILLEGALOP, 'Illegal operation', self.context)

class Bool(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value
		
	def compare_eq(self, other):
		return Bool(other.is_true() == self.value).set_context(self.context), None
		
	def compare_ne(self, other):
		return Bool(other.is_true() != self.value).set_context(self.context), None

	def compare_and(self, other):
		return Bool(self.is_true() and other.is_true()).set_context(self.context), None
	
	def compare_or(self, other):
		return Bool(self.is_true() or other.is_true()).set_context(self.context), None

	def check_in(self, other):
		if isinstance(other, List):
			for v in other.elements:
				if isinstance(v, Bool) and v.value == self.value: return Bool(True), None
			return Bool(False), None
		else: return None, Value.illegal_operation(self, other)

	def invert(self):
		return Bool(not self.value).set_context(self.context), None
		
	def is_true(self):
		return self.value

	def copy(self):
		copy = Bool(self.value)
		copy.set_pos(self.start_pos, self.end_pos)
		copy.set_context(self.context)
		return copy

	def __repr__(self):
		return f'{str(self.value).upper()}'

Bool.true  = Bool(True)
Bool.false = Bool(False)

class Nothing(Value):
	def __init__(self):
		super().__init__()
		
	def compare_eq(self, other):
		return Bool(isinstance(other, Nothing)).set_context(self.context), None
		
	def compare_ne(self, other):
		return Bool(not isinstance(other, Nothing)).set_context(self.context), None

	def compare_and(self, other):
		return Bool(False).set_context(self.context), None
	
	def compare_or(self, other):
		return other.copy(), None

	def check_in(self, other):
		if isinstance(other, List):
			for v in other.elements:
				if isinstance(v, Nothing): return Bool(True), None
			return Bool(False), None
		else: return None, Value.illegal_operation(self, other)
		
	def is_true(self):
		return False

	def copy(self):
		copy = Nothing()
		copy.set_pos(self.start_pos, self.end_pos)
		copy.set_context(self.context)
		return copy

	def __repr__(self):
		return 'NOTHING'

Nothing.nothing = Nothing()

class Number(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def added_to(self, other):
		if isinstance(other, Number): return Number(self.value + other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)

	def subbed_by(self, other):
		if isinstance(other, Number): return Number(self.value - other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
		
	def multed_by(self, other):
		if isinstance(other, Number): return Number(self.value * other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number): 
			if other.value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Division by zero', self.context)
			return Number(self.value / other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)

	def moded_by(self, other):
		if isinstance(other, Number): 
			if other.value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Modulo by zero', self.context)
			return Number(self.value % other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)

	def powed_by(self, other):
		if isinstance(other, Number): return Number(self.value ** other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_eq(self, other):
		if isinstance(other, Number): return Bool(self.value == other.value).set_context(self.context), None
		elif isinstance(other, Nothing): return Bool(False), None
		elif isinstance(other, Bool): return Bool(self.is_true() == other.value), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_ne(self, other):
		if isinstance(other, Number): return Bool(self.value != other.value).set_context(self.context), None
		elif isinstance(other, Nothing): return Bool(True), None
		elif isinstance(other, Bool): return Bool(self.is_true() != other.value), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_lt(self, other):
		if isinstance(other, Number): return Bool(self.value < other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_gt(self, other):
		if isinstance(other, Number): return Bool(self.value > other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_lte(self, other):
		if isinstance(other, Number): return Bool(self.value <= other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_gte(self, other):
		if isinstance(other, Number): return Bool(self.value >= other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
	
	def compare_and(self, other):
		if isinstance(other, Number): return Bool(self.value and other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_or(self, other):
		if isinstance(other, Number): return Bool(self.value or other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
	
	def check_in(self, other):
		if isinstance(other, List):
			for v in other.elements:
				if isinstance(v, Number) and v.value == self.value: return Bool(True), None
			return Bool(False), None
		else: return None, Value.illegal_operation(self, other)

	def invert(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None

	def is_true(self):
		return self.value != 0

	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.start_pos, self.end_pos)
		copy.set_context(self.context)
		return copy

	def __repr__(self):
		return str(self.value)

class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value
	
	def added_to(self, other):
		if isinstance(other, String): return String(self.value + other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
	
	def multed_by(self, other):
		if isinstance(other, Number): return String(self.value * int(other.value)).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number): 
			if other.value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Division by zero', self.context)
			return String(self.value[:int(len(self.value)/other.value)]).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_lte(self, other):
		if isinstance(other, Number):
			try: return String(self.value[int(other.value)]), None
			except Exception: return None, RuntimeError(other.start_pos, other.end_pos, RTE_IDXOUTOFRANGE, 'Character at this index could not be accessed from [STRING] because index is out of bounds', self.context)
		else: return None, Value.illegal_operation(self, other)

	def compare_eq(self, other):
		if isinstance(other, String): return Bool(self.value == other.value).set_context(self.context), None
		elif isinstance(other, Nothing): return Bool(False), None
		elif isinstance(other, Bool): return Bool(self.is_true() == other.value), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_ne(self, other):
		if isinstance(other, String): return Bool(self.value != other.value).set_context(self.context), None
		elif isinstance(other, Nothing): return Bool(True), None
		elif isinstance(other, Bool): return Bool(self.is_true() != other.value), None
		else: return None, Value.illegal_operation(self, other)
	
	def compare_and(self, other):
		if isinstance(other, String): return String(self.value and other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
		
	def compare_or(self, other):
		if isinstance(other, String): return String(self.value or other.value).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
	
	def check_in(self, other):
		if isinstance(other, String): return Bool(self.value in other.value), None
		elif isinstance(other, List):
			for v in other.elements:
				if isinstance(v, String) and v.value == self.value: return Bool(True), None
			return Bool(False), None
		else: return None, Value.illegal_operation(self, other)

	def is_true(self):
		return len(self.value) > 0

	def copy(self):
		copy = String(self.value)
		copy.set_pos(self.start_pos, self.end_pos)
		copy.set_context(self.context)
		return copy

	def __str__(self):
		return f'{self.value}'

	def __repr__(self):
		return f'\'{repr(self.value)[1:-1]}\''

String.ezr_version = String(VERSION)

class List(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements
	
	def added_to(self, other):
		new_list = self.copy()
		if isinstance(other, List): new_list.elements.extend(other.elements)
		else: new_list.elements.append(other)

		return new_list, None
	
	def subbed_by(self, other):
		if isinstance(other, Number):
			new_list = self.copy()
			try:
				new_list.elements.pop(int(other.value))
				return new_list, None
			except Exception: return None, RuntimeError(other.start_pos, other.end_pos, RTE_IDXOUTOFRANGE, 'Element at this index could not be removed from [LIST] because index is out of bounds', self.context)
		else: return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number): return List(self.elements * int(other.value)).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number): 
			if other.value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Division by zero', self.context)
			elements = self.elements[0:int(len(self.elements)/other.value)]
			return List(elements).set_context(self.context), None
		else: return None, Value.illegal_operation(self, other)
	
	def compare_lte(self, other):
		if isinstance(other, Number):
			try: return self.elements[int(other.value)], None
			except Exception: return None, RuntimeError(other.start_pos, other.end_pos, RTE_IDXOUTOFRANGE, 'Element at this index could not be accessed from [LIST] because index is out of bounds', self.context)
		else: return None, Value.illegal_operation(self, other)

	def compare_eq(self, other):
		if isinstance(other, List):
			same = True
			if len(self.elements) == len(other.elements):
				for i in range(len(self.elements)):
					if type(self.elements[i]) != type(other.elements[i]): same = False
					else:
						if isinstance(self.elements[i], (String, Number)):
							if self.elements[i].value != other.elements[i].value: same = False
						else: return None, RuntimeError(self.start_pos, other.end_pos, RTE_ILLEGALOP, 'Cannot compare nested [LIST]s', self.context)
			else: same = False

			return Bool(same).set_context(self.context), None
		elif isinstance(other, Nothing): return Bool(False), None
		elif isinstance(other, Bool): return Bool(self.is_true() == other.value), None
		else: return None, Value.illegal_operation(self, other)

	def compare_ne(self, other):
		if isinstance(other, List):
			same = True
			if len(self.elements) == len(other.elements):
				for i in range(len(self.elements)):
					if type(self.elements[i]) != type(other.elements[i]): same = False
					else:
						if isinstance(self.elements[i], (String, Number)):
							if self.elements[i].value != other.elements[i].value: same = False
						else: return None, RuntimeError(self.start_pos, other.end_pos, RTE_ILLEGALOP, 'Cannot compare nested [LIST]s', self.context)
			else: same = False

			return Bool(not same).set_context(self.context), None
		elif isinstance(other, Nothing): return Bool(True), None
		elif isinstance(other, Bool): return Bool(self.is_true() != other.value), None
		else: return None, Value.illegal_operation(self, other)

	def compare_and(self, other):
		if isinstance(other, List):
			new_list = None
			if self.is_true() and other.is_true(): new_list = other.copy()
			else: new_list = List([]).set_context(self.context)

			return new_list, None
		else: return None, Value.illegal_operation(self, other)
	
	def compare_or(self, other):
		if isinstance(other, List):
			new_list = None
			if other.is_true: new_list = other.copy()
			else: new_list = self.copy()

			return new_list, None
		else: return None, Value.illegal_operation(self, other)

	def is_true(self):
		return len(self.elements) > 0

	def copy(self):
		copy = List(self.elements)
		copy.set_context(self.context)
		copy.set_pos(self.start_pos, self.end_pos)
		return copy

	def __repr__(self):
		elements = ', '.join([repr(i) for i in self.elements])
		return f'[{elements}]'

class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name or '<anonymous>'

	def generate_context(self):
		new_context = Context(self.name, self.context, self.start_pos)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		return new_context

	def check_args(self, arg_names, args):
		res = RuntimeResult()
		if len(args) > len(arg_names): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_TOOMANYARGS, f'{len(args)-len(arg_names)} too many arguments passed into \'{self.name}\'', self.context))
		if len(args) < len(arg_names): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_TOOFEWARGS, f'{len(arg_names)-len(args)} too few arguments passed into \'{self.name}\'', self.context))

		return res.success(None)
	
	def populate_args(self, arg_names, args, context):
		for i in range(len(args)):
			arg_name = arg_names[i]
			arg_value = args[i]
			arg_value.set_context(context)
			context.symbol_table.set(arg_name, arg_value)

	def check_and_populate_args(self, arg_names, args, context):
		res = RuntimeResult()
		res.register(self.check_args(arg_names, args))
		if res.should_return(): return res
		self.populate_args(arg_names, args, context)
		return res.success(None)

class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names, should_auto_return):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.should_auto_return = should_auto_return

	def execute(self, args):
		res = RuntimeResult()
		interpreter = Interpreter()
		new_context = self.generate_context()
		res.register(self.check_and_populate_args(self.arg_names, args, new_context))
		if res.should_return(): return res

		value = res.register(interpreter.visit(self.body_node, new_context))
		if res.should_return() and res.function_return_value == None: return res

		return_value = (value if self.should_auto_return else None) or res.function_return_value or Nothing()
		return res.success(return_value)
	
	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
		copy.set_context(self.context)
		copy.set_pos(self.start_pos, self.end_pos)
		return copy
	
	def __repr__(self):
		return f'<function {self.name}>'

class BuiltInFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RuntimeResult()
		context = self.generate_context()

		method_name = f'execute_{self.name}'
		method = getattr(self, method_name, self.no_visit_method)
		res.register(self.check_and_populate_args(method.arg_names, args, context))
		if res.should_return(): return res

		return_value = res.register(method(context))
		if res.should_return(): return res
		return res.success(return_value)

	def no_visit_method(self, node, context):
		raise Exception(f'No execute_{self.name} method defined!')

	def execute_show(self, context):
		print(str(context.symbol_table.get('out')))
		return RuntimeResult().success(Nothing())
	execute_show.arg_names = ['out']

	def execute_show_error(self, context):
		return RuntimeResult().failure(RuntimeError(self.start_pos, self.end_pos, RTE_CUSTOM, str(context.symbol_table.get('out')), context.parent))
	execute_show_error.arg_names = ['out']
	
	def execute_get(self, context):
		return RuntimeResult().success(String(input(str(context.symbol_table.get('out')))))
	execute_get.arg_names = ['out']
	
	def execute_get_int(self, context):
		while True:
			text = input(str(context.symbol_table.get('out')))
			try: number = int(text); break
			except ValueError: print(f'\'{text}\' must be an [INT]. Try again!')

		return RuntimeResult().success(Number(number))
	execute_get_int.arg_names = ['out']
	
	def execute_get_float(self, context):
		while True:
			text = input(str(context.symbol_table.get('out')))
			try: number = float(text); break
			except ValueError: print(f'\'{text}\' must be an [INT] or [FLOAT]. Try again!')

		return RuntimeResult().success(Number(number))
	execute_get_float.arg_names = ['out']
	
	def execute_clear_screen(self, context):
		system('cls' if name == 'nt' else 'clear')
		return RuntimeResult().success(Nothing())
	execute_clear_screen.arg_names = []

	def execute_type_of(self, context):
		value = context.symbol_table.get('value')
		type_ = 'UNKNOWN'

		if isinstance(value, Number):
			if isinstance(value.value, int): type_ = 'INT'
			elif isinstance(value.value, float): type_ = 'FLOAT'
			else: type_ = 'NUMBER'
		elif isinstance(value, String): type_ = 'STRING'
		elif isinstance(value, List): type_ = 'LIST'
		elif isinstance(value, Object): type_ = value.name
		elif isinstance(value, BaseFunction): type_ = 'FUNCTION'
		elif isinstance(value, Bool): type_ = 'BOOLEAN'
		elif isinstance(value, Nothing): type_ = 'NOTHING'

		return RuntimeResult().success(String(type_))
	execute_type_of.arg_names = ['value']
	
	def execute_convert(self, context):
		res = RuntimeResult()
		value = context.symbol_table.get('value')
		type_ = context.symbol_table.get('type')

		if not isinstance(type_, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be a [STRING]', context))
		if type_ == 'FUNCTION': return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Cannot convert items to a [FUNCTION]', context))
		if type_ == 'LIST': return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Cannot convert items to a [LIST]', context))

		new_value = Nothing()
		if isinstance(value, (String, Number, Bool)):
			if type_.value == 'STRING': new_value = String(str(value))
			elif type_.value == 'INT':
				try: new_value = Number(int(value.value))
				except Exception: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, f'Could not convert \'{value.value}\' to an [INT]', context))
			elif type_.value == 'FLOAT':
				try: new_value = Number(float(value.value))
				except Exception: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, f'Could not convert \'{value.value}\' to a [FLOAT]', context))
			elif type_.value == 'BOOLEAN': new_value = Bool(value.is_true())
			else: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Unknown type', context))
		elif isinstance(value, (BaseFunction, List)):
			if type_.value == 'STRING': new_value = String(str(value))
			else: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Can only convert [FUNCTION]s and [LIST]s to [STRING]s', context))
		else: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Unknown value type', context))
		return res.success(new_value)
	execute_convert.arg_names = ['value', 'type']

	def execute_extend(self, context):
		res = RuntimeResult()
		list_ = context.symbol_table.get('list')
		value = context.symbol_table.get('value')

		if not isinstance(list_, List): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [LIST]', context))

		if isinstance(value, List): list_.elements.extend(value.elements)
		else: list_.elements.append(value)
		return res.success(Nothing())
	execute_extend.arg_names = ['list', 'value']
	
	def execute_remove(self, context):
		res = RuntimeResult()
		list_ = context.symbol_table.get('list')
		index = context.symbol_table.get('index')
		
		if not isinstance(list_, List): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [LIST]', context))
		if not isinstance(index, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be an [INT]', context))

		try: element = list_.elements.pop(index.value)
		except Exception: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_IDXOUTOFRANGE, 'Element at this index could not be removed from list because index is out of bounds', context))
		return res.success(element)
	execute_remove.arg_names = ['list', 'index']

	def execute_insert(self, context):
		res = RuntimeResult()
		list_ = context.symbol_table.get('list')
		index = context.symbol_table.get('index')
		value = context.symbol_table.get('value')
		
		if not isinstance(list_, List): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [LIST]', context))
		if not isinstance(index, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be an [INT]', context))
		
		if isinstance(value, List):
			index_ = index.value
			for i in range(len(value.elements)):
				list_.elements.insert(index_, value.elements[i])
				index_ += 1
		else: list_.elements.insert(index.value, value)
		return res.success(Nothing())
	execute_insert.arg_names = ['list', 'index', 'value']

	def execute_len(self, context):
		res = RuntimeResult()
		value = context.symbol_table.get('value')

		if not isinstance(value, List) and not isinstance(value, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Argument must be a [LIST] or [STRING]', context))

		if isinstance(value, List): return res.success(Number(len(value.elements)))
		elif isinstance(value, String): return res.success(Number(len(value.value)))
	execute_len.arg_names = ['value']

	def execute_split(self, context):
		res = RuntimeResult()
		value = context.symbol_table.get('value')
		sep = context.symbol_table.get('separator')

		if not isinstance(value, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
		if not isinstance(sep, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be a [STRING]', context))

		elements = []
		split_ = value.value.split(sep.value)
		for i in split_: elements.append(String(i))
		return res.success(List(elements))
	execute_split.arg_names = ['value', 'separator']

	def execute_join(self, context):
		res = RuntimeResult()
		list_ = context.symbol_table.get('list')
		sep = context.symbol_table.get('separator')

		if not isinstance(list_, List): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [LIST]', context))
		if not isinstance(sep, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be a [STRING]', context))

		elements = []
		for i in list_.elements:
			if isinstance(i, (BaseFunction, List)): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument cannot contain type [FUNCTION] or [LIST]', context))
			elements.append(str(i))

		joined = sep.value.join(elements)
		return res.success(String(joined))
	execute_join.arg_names = ['list', 'separator']

	def execute_replace(self, context):
		res = RuntimeResult()
		value = context.symbol_table.get('value')
		sub_a = context.symbol_table.get('arg_a')
		sub_b = context.symbol_table.get('arg_b')

		if isinstance(value, String):
			if not isinstance(sub_a, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be a [STRING]', context))
			if not isinstance(sub_b, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Third argument must be a [STRING]', context))
			return res.success(String(value.value.replace(sub_a.value, sub_b.value)))
		elif isinstance(value, List):
			if not isinstance(sub_a, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be a [INT]', context))
			new_list = value.copy()
			new_list.elements[sub_a.value] = sub_b
			return res.success(new_list)

		return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or [LIST]', context))
	execute_replace.arg_names = ['value', 'arg_a', 'arg_b']

	def execute_run(self, context):
		res = RuntimeResult()
		fn = context.symbol_table.get('filepath')

		if not isinstance(fn, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Argument must be a [STRING]', context))

		fn = fn.value
		if not path.isfile(fn): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_IO, f'File \'{fn}\' does not exist', context))

		try:
			with open(fn, 'r') as f:
				script = f.read()
		except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_IO, f'Failed to load script \'{fn}\'\n{str(error)}', context))
		
		_, error = run(fn, script)
		if error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_IO, f'Failed to finish executing script \'{fn}\'\n\n{error.as_string()}', context))
		return res.success(Nothing())
	execute_run.arg_names = ['filepath']

	def copy(self):
		copy = BuiltInFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.start_pos, self.end_pos)
		return copy

	def __repr__(self):
		return f'<built-in function <{self.name}>>'

BuiltInFunction.show               = BuiltInFunction('show')
BuiltInFunction.show_error         = BuiltInFunction('show_error')
BuiltInFunction.get                = BuiltInFunction('get')
BuiltInFunction.get_int            = BuiltInFunction('get_int')
BuiltInFunction.get_float          = BuiltInFunction('get_float')
BuiltInFunction.clear_screen       = BuiltInFunction('clear_screen')
BuiltInFunction.type_of            = BuiltInFunction('type_of')
BuiltInFunction.convert            = BuiltInFunction('convert')
BuiltInFunction.extend             = BuiltInFunction('extend')
BuiltInFunction.remove             = BuiltInFunction('remove')
BuiltInFunction.insert             = BuiltInFunction('insert')
BuiltInFunction.len                = BuiltInFunction('len')
BuiltInFunction.split              = BuiltInFunction('split')
BuiltInFunction.join               = BuiltInFunction('join')
BuiltInFunction.replace            = BuiltInFunction('replace')
BuiltInFunction.run                = BuiltInFunction('run')

class Object(BaseFunction):
	def __init__(self, name, body_node, arg_names, internal_context=None):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.internal_context = internal_context

	def execute(self, args):
		res = RuntimeResult()
		interpreter = Interpreter()
		self.internal_context = self.generate_context()
		res.register(self.check_and_populate_args(self.arg_names, args, self.internal_context))
		if res.should_return(): return res

		res.register(interpreter.visit(self.body_node, self.internal_context))
		if res.should_return() and res.function_return_value == None: return res

		return res.success(self.copy())

	def retrieve(self, node):
		res = RuntimeResult()
		interpreter = Interpreter()

		value = res.register(interpreter.visit(node, self.internal_context))
		if res.should_return() and res.function_return_value == None: return res

		return_value = value
		return res.success(return_value)
	
	def copy(self):
		copy = Object(self.name, self.body_node, self.arg_names, self.internal_context)
		copy.set_context(self.context)
		copy.set_pos(self.start_pos, self.end_pos)
		return copy
	
	def __repr__(self):
		return f'<object {self.name}>'

# CONTEXT

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None

# SYMBOL TABLE

class SymbolTable:
	def __init__(self, parent=None):
		self.symbols = {}
		self.parent = parent

	def get(self, name):
		value = self.symbols.get(name, None)

		if value == None and self.parent: return self.parent.get(name)
		return value
	
	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]

# INTERPRETER

class Interpreter:
	def visit(self, node, context):
		method_name= f'visit_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context):
		raise Exception(f'No visit_{type(node).__name__} method defined!')

	def visit_NumberNode(self, node, context):
		return RuntimeResult().success(Number(node.token.value).set_context(context).set_pos(node.start_pos, node.end_pos))

	def visit_StringNode(self, node, context):
		return RuntimeResult().success(String(node.token.value).set_context(context).set_pos(node.start_pos, node.end_pos))

	def visit_ListNode(self, node, context):
		res = RuntimeResult()
		elements = []

		for element_node in node.element_nodes:
			elements.append(res.register(self.visit(element_node, context)))
			if res.should_return(): return res
		
		return res.success(List(elements).set_context(context).set_pos(node.start_pos, node.end_pos))
		
	def visit_VarAccessNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_token.value
		value = context.symbol_table.get(var_name)

		if not value: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_UNDEFINEDVAR, f'\'{var_name}\' is not defined', context))

		value = value.copy().set_pos(node.start_pos, node.end_pos).set_context(context)
		return res.success(value)

	def visit_VarAssignNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_token.value
		value = res.register(self.visit(node.value_node, context))
		if res.should_return(): return res
		
		if node.is_global and context.parent != None: context.symbol_table.parent.set(var_name, value)
		else: context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_BinOpNode(self, node, context):
		res = RuntimeResult()
		left = res.register(self.visit(node.left_node, context))
		if res.should_return(): return res
		right = res.register(self.visit(node.right_node, context))
		if res.should_return(): return res

		if node.operator_token.type == TT_PLUS:
			result, error = left.added_to(right)
		elif node.operator_token.type == TT_MINUS:
			result, error = left.subbed_by(right)
		elif node.operator_token.type == TT_MUL:
			result, error = left.multed_by(right)
		elif node.operator_token.type == TT_DIV:
			result, error = left.dived_by(right)
		elif node.operator_token.type == TT_MOD:
			result, error = left.moded_by(right)
		elif node.operator_token.type == TT_POW:
			result, error = left.powed_by(right)
		
		elif node.operator_token.type == TT_EE:
			result, error = left.compare_eq(right)
		elif node.operator_token.type == TT_NE:
			result, error = left.compare_ne(right)
		elif node.operator_token.type == TT_LT:
			result, error = left.compare_lt(right)
		elif node.operator_token.type == TT_GT:
			result, error = left.compare_gt(right)
		elif node.operator_token.type == TT_LTE:
			result, error = left.compare_lte(right)
		elif node.operator_token.type == TT_GTE:
			result, error = left.compare_gte(right)
		elif node.operator_token.matches(TT_KEY, 'AND'):
			result, error = left.compare_and(right)
		elif node.operator_token.matches(TT_KEY, 'OR'):
			result, error = left.compare_or(right)

		elif node.operator_token.matches(TT_KEY, 'IN'):
			result, error = left.check_in(right)

		if error: return res.failure(error)
		else: return res.success(result.set_pos(node.start_pos, node.end_pos))

	def visit_UnaryOpNode(self, node, context):
		res = RuntimeResult()
		number = res.register(self.visit(node.node, context))
		if res.should_return(): return res

		error = None
		if node.operator_token.type == TT_MINUS: number, error = number.multed_by(Number(-1))
		elif node.operator_token.matches(TT_KEY, 'INVERT'): number, error = number.invert()
		
		if error: return res.failure(error)
		else: return res.success(number.set_pos(node.start_pos, node.end_pos))

	def visit_IfNode(self, node, context):
		res = RuntimeResult()

		for condition, expression, should_return_null in node.cases:
			condition_value = res.register(self.visit(condition, context))
			if res.should_return(): return res

			if condition_value.is_true():
				expression_value = res.register(self.visit(expression, context))
				if res.should_return(): return res
				return res.success(Nothing() if should_return_null else expression_value)
		
		if node.else_case:
			expression, should_return_null = node.else_case
			else_value = res.register(self.visit(expression, context))
			if res.should_return(): return res
			return res.success(Nothing() if should_return_null else else_value)
		
		return res.success(Nothing())

	def visit_CountNode(self, node, context):
		res = RuntimeResult()
		elements = []

		start_value = res.register(self.visit(node.start_value_node, context))
		if res.should_return(): return res

		end_value = res.register(self.visit(node.end_value_node, context))
		if res.should_return(): return res

		if node.step_value_node:
			step_value = res.register(self.visit(node.step_value_node, context))
			if res.should_return(): return res
		else:
			step_value = Number(1)
		
		i = start_value.value
		if step_value.value > 0: condition = lambda: i < end_value.value
		else: condition = lambda: i > end_value.value

		while condition():
			context.symbol_table.set(node.var_name_token.value, Number(i))
			i += step_value.value

			value = res.register(self.visit(node.body_node, context))
			if res.should_return() and not res.loop_should_skip and not res.loop_should_stop: return res
			if res.loop_should_skip: continue
			if res.loop_should_stop: break
			elements.append(value)

		return res.success(Nothing() if node.should_return_null else List(elements).set_context(context).set_pos(node.start_pos, node.end_pos))
	
	def visit_WhileNode(self, node, context):
		res = RuntimeResult()
		elements = []

		while True:
			condition = res.register(self.visit(node.condition_node, context))
			if res.should_return(): return res

			if not condition.is_true(): break

			value = res.register(self.visit(node.body_node, context))
			if res.should_return() and not res.loop_should_skip and not res.loop_should_stop: return res
			if res.loop_should_skip: continue
			if res.loop_should_stop: break
			elements.append(value)
		
		return res.success(Nothing() if node.should_return_null else List(elements).set_context(context).set_pos(node.start_pos, node.end_pos))
	
	def visit_TryNode(self, node, context):
		res = RuntimeResult()
		value = res.register(self.visit(node.body_node, context))

		if res.error:
			error = res.error.error_type
			value = Nothing()
			res.reset()

			if len(node.catches) >= 1:
				for i in node.catches:
					if (i[0] == None):
						if i[1] != None: context.symbol_table.set(i[1].value, String(error))

						value = res.register(self.visit(i[2], context))
						if res.should_return(): return res
						break
					elif (i[0].value == error):
						if i[1] != None: context.symbol_table.set(i[1].value, String(error))

						value = res.register(self.visit(i[2], context))
						if res.should_return(): return res
						break

		return res.success(Nothing() if node.should_return_null else value.set_context(context).set_pos(node.start_pos, node.end_pos))

	def visit_FuncDefNode(self, node, context):
		res = RuntimeResult()

		func_name = node.var_name_token.value if node.var_name_token else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
		func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.start_pos, node.end_pos)

		if node.var_name_token: context.symbol_table.set(func_name, func_value)

		return res.success(func_value)

	def visit_ObjectDefNode(self, node, context):
		res = RuntimeResult()

		object_name = node.var_name_token.value
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
		object_value = Object(object_name, body_node, arg_names).set_context(context).set_pos(node.start_pos, node.end_pos)

		context.symbol_table.set(object_name, object_value)
		return res.success(object_value)

	def visit_CallNode(self, node, context):
		res = RuntimeResult()
		args = []

		value_to_call = res.register(self.visit(node.node_to_call, context))
		if res.should_return(): return res
		value_to_call = value_to_call.copy().set_pos(node.start_pos, node.end_pos)

		for arg_node in node.arg_nodes:
			args.append(res.register(self.visit(arg_node, context)))
			if res.should_return(): return res

		return_value = res.register(value_to_call.execute(args))

		if res.should_return(): return res
		return_value = return_value.copy().set_pos(node.start_pos, node.end_pos).set_context(context)
		return res.success(return_value)

	def visit_ObjectCallNode(self, node, context):
		res = RuntimeResult()

		object_ = res.register(self.visit(node.object_node, context))
		if res.should_return(): return res
		object_ = object_.copy().set_pos(node.start_pos, node.end_pos)

		return_value = res.register(object_.retrieve(node.node_to_call))
		if res.should_return(): return res
		return_value = return_value.copy().set_pos(node.start_pos, node.end_pos).set_context(context)
		return res.success(return_value)

	def visit_IncludeNode(self, node, context):
		res = RuntimeResult()

		filename = node.name_node.value
		plausible = [path.join(getcwd(), filename), filename, *[path.join(i, filename) for i in local_lib_path], path.join(LIB_PATH, filename)]

		filepath = None
		for i in plausible:
			if path.isfile(i):
				filepath = i
				break

		if filepath == None: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'File \'{filename}\' does not exist', context))

		if len(path.splitext(filepath)) > 1 and path.splitext(filepath)[1] == '.py':
			try:
				location, lib_name = path.abspath(filepath), path.splitext(path.basename(filepath))[0]
				spec = util.spec_from_file_location(lib_name, location)
				lib = util.module_from_spec(spec)
				spec.loader.exec_module(lib)
			except ImportError as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'Failed to load script \'{filename}\'\n{str(error).capitalize()}', context))

			try: object_ = res.register(lib.lib_Object().set_context(context).set_pos(node.start_pos, node.end_pos).execute())
			except AttributeError: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'\'lib_Object\' not defined in \'{filename}\'', context))

			if res.should_return(): return res
			name = node.nickname_node.value if node.nickname_node else object_.name

			fname = ''
			for i in name:
				if i not in LETTERS_DIGITS + '_': fname = f'{fname}_'
				else: fname = f'{fname}{i}'

			object_.name = fname
			context.symbol_table.set(fname, object_)
		else:
			try:
				with open(filepath, 'r') as f: script = f.read()
			except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'Failed to load script \'{filename}\'\n{str(error)}', context))

			tokens, error = Lexer(filename, script).compile_tokens()
			if error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'Failed to finish executing script \'{filename}\'\n\n{error.as_string()}', context))

			ast = Parser(tokens).parse()
			if ast.error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'Failed to finish executing script \'{filename}\'\n\n{ast.error.as_string()}', context))
		
			name = node.nickname_node.value if node.nickname_node else path.splitext(path.basename(node.name_node.value))[0]

			fname = ''
			for i in name:
				if i not in LETTERS_DIGITS + '_': fname = f'{fname}_'
				else: fname = f'{fname}{i}'

			object_ = res.register(Object(fname, ast.node, []).set_context(context).set_pos(node.start_pos, node.end_pos).execute([]))
			if res.should_return(): return res

			context.symbol_table.set(fname, object_)

		return res.success(Nothing())

	def visit_ReturnNode(self, node, context):
		res = RuntimeResult()

		if node.node_to_return:
			value = res.register(self.visit(node.node_to_return, context))
			if res.should_return(): return res
		else: value = Nothing()

		return res.success_return(value)
	
	def visit_SkipNode(self, node, context):
		return RuntimeResult().success_skip()

	def visit_StopNode(self, node, context):
		return RuntimeResult().success_stop()

# RUN

global_symbol_table = SymbolTable()

# Main variables
global_symbol_table.set('NOTHING', Nothing.nothing)
global_symbol_table.set('TRUE', Bool.true)
global_symbol_table.set('FALSE', Bool.false)
global_symbol_table.set('EZR_VERSION', String.ezr_version)

# Main functions
global_symbol_table.set('SHOW', BuiltInFunction.show)
global_symbol_table.set('SHOW_ERROR', BuiltInFunction.show_error)
global_symbol_table.set('GET', BuiltInFunction.get)
global_symbol_table.set('GET_INT', BuiltInFunction.get_int)
global_symbol_table.set('GET_FLOAT', BuiltInFunction.get_float)
global_symbol_table.set('CLEAR_SCREEN', BuiltInFunction.clear_screen)
global_symbol_table.set('TYPE_OF', BuiltInFunction.type_of)
global_symbol_table.set('CONVERT', BuiltInFunction.convert)
global_symbol_table.set('EXTEND', BuiltInFunction.extend)
global_symbol_table.set('REMOVE', BuiltInFunction.remove)
global_symbol_table.set('INSERT', BuiltInFunction.insert)
global_symbol_table.set('LEN', BuiltInFunction.len)
global_symbol_table.set('SPLIT', BuiltInFunction.split)
global_symbol_table.set('JOIN', BuiltInFunction.join)
global_symbol_table.set('REPLACE', BuiltInFunction.replace)
global_symbol_table.set('RUN', BuiltInFunction.run)

local_lib_path = []

def run(fn, input_):
	global local_lib_path
	filepath = path.abspath(path.dirname(fn))
	local_lib_path.append(filepath)

	# Generate tokens
	lexer = Lexer(fn, input_)
	tokens, error = lexer.compile_tokens()
	if error: return None, error

	# Generate abstract syntax tree
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# Run program
	interpreter = Interpreter()
	context = Context('<main>')
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error
