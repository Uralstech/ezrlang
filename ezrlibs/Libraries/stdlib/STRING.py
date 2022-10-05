from ezr import RuntimeResult, RuntimeError, Value, Nothing, Number, Bool, String, List, RTE_INCORRECTTYPE, RTE_MATH
from string import ascii_lowercase, ascii_uppercase, ascii_letters, punctuation, digits, hexdigits, octdigits
from Libraries.base.base_libObject import base_libObject
import Libraries.stdlib.INT as INT
# from ezrlibs.Libraries.base.base_libObject import base_libObject # Debug
# import ezrlibs.Libraries.stdlib.INT as INT # Debug

class STRING(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('STRING', internal_context)
        
    def copy(self):
        copy = STRING(self.internal_context)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)

        return copy
    
    def new_object(self):
        return STRING().set_context(self.context).execute().value
        
    def set_value(self, value):
        self.set_variable('VALUE', String(str(value.value)))
        return self

    def initialize(self, context):
        self.set_variable('ASCII_LOWERCASE', String(ascii_lowercase))
        self.set_variable('ASCII_UPPERCASE', String(ascii_uppercase))
        self.set_variable('ASCII_LETTERS', String(ascii_letters))
        self.set_variable('PUNCTUATION', String(punctuation))
        self.set_variable('DIGITS', String(digits))
        self.set_variable('HEXDIGITS', String(hexdigits))
        self.set_variable('OCTDIGITS', String(octdigits))

        return RuntimeResult().success(Nothing())
        
    # Operations
    
    def added_to(self, other):
        if isinstance(other, String): return String(self.get_variable('VALUE').value + other.value).set_context(self.context), None
        elif isinstance(other, STRING): return self.new_object().set_value(String(self.get_variable('VALUE').value + other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number): return String(self.get_variable('VALUE').value * other.value).set_context(self.context), None
        elif isinstance(other, INT.INT): return self.new_object().set_value(String(self.get_variable('VALUE').value * other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)
        
    def dived_by(self, other):
        if isinstance(other, Number): 
            if other.value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Division by zero', self.context)
            return String(self.get_variable('VALUE').value[:int(len(self.get_variable('VALUE').value)/other.value)]).set_context(self.context), None
        elif isinstance(other, INT.INT): 
            if other.get_variable('VALUE').value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Division by zero', self.context)
            return self.new_object().set_value(String(self.get_variable('VALUE').value[:int(len(self.get_variable('VALUE').value)/other.get_variable('VALUE').value)])), None
        else: return None, Value.illegal_operation(self, other)

    def compare_eq(self, other):
        if isinstance(other, String): return Bool(self.get_variable('VALUE').value == other.value).set_context(self.context), None
        elif isinstance(other, STRING): return Bool(self.get_variable('VALUE').value == other.get_variable('VALUE').value).set_context(self.context), None
        elif isinstance(other, Nothing): return Bool(False).set_context(self.context), None
        elif isinstance(other, Bool): return Bool(self.is_true() == other.value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_ne(self, other):
        if isinstance(other, String): return Bool(self.get_variable('VALUE').value != other.value).set_context(self.context), None
        elif isinstance(other, STRING): return Bool(self.get_variable('VALUE').value != other.get_variable('VALUE').value).set_context(self.context), None
        elif isinstance(other, Nothing): return Bool(True).set_context(self.context), None
        elif isinstance(other, Bool): return Bool(self.is_true() != other.value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_and(self, other):
        if isinstance(other, String): return Bool(self.is_true() and other.is_true()).set_context(self.context), None
        elif isinstance(other, STRING): return Bool(self.is_true() and other.is_true()).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_or(self, other):
        if isinstance(other, String): return Bool(self.is_true() or other.is_true()).set_context(self.context), None
        elif isinstance(other, STRING): return Bool(self.is_true() or other.is_true()).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
    
    def check_in(self, other):
        if isinstance(other, List):
            for v in other.elements:
                if isinstance(v, STRING) and v.get_variable('VALUE').value == self.get_variable('VALUE').value: return Bool(True).set_context(self.context), None
            return Bool(False).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.get_variable('VALUE').value) > 0

    def function_TOUPPER(self, node, context):
        return RuntimeResult().success(self.new_object().set_value(String(self.get_variable('VALUE').value.upper())))
    function_TOUPPER.arg_names = []

    def function_TOLOWER(self, node, context):
        return RuntimeResult().success(self.new_object().set_value(String(self.get_variable('VALUE').value.lower())))
    function_TOLOWER.arg_names = []

    def function_CAPITALIZED(self, node, context):
        return RuntimeResult().success(self.new_object().set_value(String(self.get_variable('VALUE').value.capitalize())))
    function_CAPITALIZED.arg_names = []

    def function_SWAPCASE(self, node, context):
        return RuntimeResult().success(self.new_object().set_value(String(self.get_variable('VALUE').value.swapcase())))
    function_SWAPCASE.arg_names = []

    def function_JOIN(self, node, context):
        res = RuntimeResult()
        list_ = context.symbol_table.get('list')

        if not isinstance(list_, List): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [LIST]', context))

        elements = []
        str_list = False
        for i in list_.elements:
            if not isinstance(i, String) and not isinstance(i, STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'All values in the first argument must be a [STRING] or STD.STRING', context))
            
            if isinstance(i, String): elements.append(i.value)
            else:
                elements.append(i.get_variable('VALUE').value)
                str_list = True
        
        if str_list: return res.success(self.new_object().set_value(String(self.get_variable('VALUE').value.join(elements))))
        return res.success(String(self.get_variable('VALUE').value.join(elements)))
    function_JOIN.arg_names = ['list']

    def function_STARTSWITH(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))
        if isinstance(value, STRING): return res.success(Bool(self.get_variable('VALUE').value.startswith(value.get_variable('VALUE').value)))
        return res.success(Bool(self.get_variable('VALUE').value.startswith(value.value)))
    function_STARTSWITH.arg_names = ['value']

    def function_ENDSWITH(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))
        if isinstance(value, STRING): return res.success(Bool(self.get_variable('VALUE').value.endswith(value.get_variable('VALUE').value)))
        return res.success(Bool(self.get_variable('VALUE').value.endswith(value.value)))
    function_ENDSWITH.arg_names = ['value']

    def function_REMOVEPREFIX(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))
        if isinstance(value, STRING): return res.success(self.new_object().set_value(String(self.get_variable('VALUE').value.removeprefix(value.get_variable('VALUE').value))))
        return res.success(String(self.get_variable('VALUE').value.removeprefix(value.value)))
    function_REMOVEPREFIX.arg_names = ['value']

    def function_REMOVESUFFIX(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))
        if isinstance(value, STRING): return res.success(self.new_object().set_value(String(self.get_variable('VALUE').value.removesuffix(value.get_variable('VALUE').value))))
        return res.success(String(self.get_variable('VALUE').value.removesuffix(value.value)))
    function_REMOVESUFFIX.arg_names = ['value']

    def function_FIND(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))
        if isinstance(value, STRING): return res.success(INT.INT().set_context(context).execute().value.set_value(String(self.get_variable('VALUE').value.find(value.get_variable('VALUE').value))))
        return res.success(Number(self.get_variable('VALUE').value.find(value.value)))
    function_FIND.arg_names = ['value']

    def function_SPLIT(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))
        
        elements = []
        if isinstance(value, STRING):
            split = self.get_variable('VALUE').value.split(value.get_variable('VALUE').value)
            for i in split: elements.append(self.new_object().set_value(String(i)))
        else:
            split = self.get_variable('VALUE').value.split(value.value)
            for i in split: elements.append(String(i))

        return res.success(List(elements))
    function_SPLIT.arg_names = ['value']

    def function_REPLACE(self, node, context):
        res = RuntimeResult()
        old = context.symbol_table.get('old')
        new_ = context.symbol_table.get('new')

        if not isinstance(old, String) and not isinstance(old, STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))
        if not isinstance(new_, type(old)): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be the same type as first argument', context))
        
        if isinstance(old, STRING): return res.success(self.new_object().set_value(String(self.get_variable('VALUE').value.replace(old.get_variable('VALUE').value, new_.get_variable('VALUE').value))))
        return res.success(String(self.get_variable('VALUE').value.replace(old.value, new_.value)))
    function_REPLACE.arg_names = ['old', 'new']

    def function_STRIP(self, node, context):
        return RuntimeResult().success(self.new_object().set_value(String(self.get_variable('VALUE').value.replace(r'\\t', '\t').strip())))
    function_STRIP.arg_names = []
    