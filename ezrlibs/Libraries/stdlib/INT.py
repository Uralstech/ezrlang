from ezr import RuntimeResult, RuntimeError, Value, Nothing, Number, Bool, String, List, RTE_INCORRECTTYPE, RTE_MATH
from Libraries.base.base_libObject import base_libObject
import Libraries.stdlib.FLOAT as FLOAT
import Libraries.stdlib.STRING as STRING
# from ezrlibs.Libraries.base.base_libObject import base_libObject # Debug
# import ezrlibs.Libraries.stdlib.FLOAT as FLOAT # Debug
# import ezrlibs.Libraries.stdlib.STRING as STRING # Debug

class INT(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('INT', internal_context)
        
    def copy(self):
        copy = INT(self.internal_context)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)

        return copy
    
    def new_object(self):
        return INT().set_context(self.context).execute().value
        
    def set_value(self, value):
        self.set_variable('VALUE', Number(int(value.value)))
        return self

    # Operations
    
    def added_to(self, other):
        if isinstance(other, Number): return Number(self.get_variable('VALUE').value + other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return self.new_object().set_value(Number(self.get_variable('VALUE').value + other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number): return Number(self.get_variable('VALUE').value - other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return self.new_object().set_value(Number(self.get_variable('VALUE').value - other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)
        
    def multed_by(self, other):
        if isinstance(other, Number): return Number(self.get_variable('VALUE').value * other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return self.new_object().set_value(Number(self.get_variable('VALUE').value * other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Division by zero', self.context)
            return Number(self.get_variable('VALUE').value / other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT):
            if other.get_variable('VALUE').value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Division by zero', self.context)
            return self.new_object().set_value(Number(self.get_variable('VALUE').value / other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)

    def moded_by(self, other):
        if isinstance(other, Number): 
            if other.value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Modulo by zero', self.context)
            return Number(self.get_variable('VALUE').value % other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT):
            if other.get_variable('VALUE').value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Modulo by zero', self.context)
            return self.new_object().set_value(Number(self.get_variable('VALUE').value % other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number): return Number(self.get_variable('VALUE').value ** other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return self.new_object().set_value(Number(self.get_variable('VALUE').value ** other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_eq(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value == other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return Bool(self.get_variable('VALUE').value == other.get_variable('VALUE').value).set_context(self.context), None
        elif isinstance(other, Nothing): return Bool(False).set_context(self.context), None
        elif isinstance(other, Bool): return Bool(self.is_true() == other.value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_ne(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value != other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return Bool(self.get_variable('VALUE').value != other.get_variable('VALUE').value).set_context(self.context), None
        elif isinstance(other, Nothing): return Bool(True).set_context(self.context), None
        elif isinstance(other, Bool): return Bool(self.is_true() != other.value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_lt(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value < other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return Bool(self.get_variable('VALUE').value < other.get_variable('VALUE').value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_gt(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value > other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return Bool(self.get_variable('VALUE').value > other.get_variable('VALUE').value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_lte(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value <= other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return Bool(self.get_variable('VALUE').value <= other.get_variable('VALUE').value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_gte(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value >= other.value).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return Bool(self.get_variable('VALUE').value >= other.get_variable('VALUE').value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
    
    def compare_and(self, other):
        if isinstance(other, Number): return Bool(self.is_true() and other.is_true()).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return Bool(self.is_true() and other.is_true()).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_or(self, other):
        if isinstance(other, Number): return Bool(self.is_true() or other.is_true()).set_context(self.context), None
        elif isinstance(other, INT) or isinstance(other, FLOAT.FLOAT): return Bool(self.is_true() or other.is_true()).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
    
    def check_in(self, other):
        if isinstance(other, List):
            for v in other.elements:
                if isinstance(v, INT) and v.get_variable('VALUE').value == self.get_variable('VALUE').value: return Bool(True).set_context(self.context), None
            return Bool(False).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)

    def invert(self):
        return self.new_object().set_value(Number(1 if self.get_variable('VALUE').value == 0 else 0)), None

    def is_true(self):
        return self.get_variable('VALUE').value != 0

    # Functions
    
    def function_HEX(self, node, context):
        str_ = STRING.STRING().set_context(context).execute().value
        int_ = hex(self.get_variable('VALUE').value).lstrip('0x')
        if int_ == '': int_ = '0'

        return RuntimeResult().success(str_.set_value(String(int_)))
    function_HEX.arg_names = []

    def function_FROMHEX(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING.STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))

        try:
            if isinstance(value, STRING.STRING): new_value = int(value.get_variable('VALUE').value, 16)
            else: new_value = int(value.value, 16)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, str(error).capitalize(), context))

        if isinstance(value, STRING.STRING):
            int_ = res.register(INT().set_context(context).execute())
            if res.should_return(): return res

            return res.success(int_.set_value(Number(new_value)))
        return res.success(Number(new_value))
    function_FROMHEX.arg_names = ['value']

    def function_OCT(self, node, context):
        str_ = STRING.STRING().set_context(context).execute().value
        int_ = oct(self.get_variable('VALUE').value).lstrip('0o')
        if int_ == '': int_ = '0'

        return RuntimeResult().success(str_.set_value(String(int_)))
    function_OCT.arg_names = []

    def function_FROMOCT(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING.STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))

        try:
            if isinstance(value, STRING.STRING): new_value = int(value.get_variable('VALUE').value, 8)
            else: new_value = int(value.value, 8)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, str(error).capitalize(), context))

        if isinstance(value, STRING.STRING):
            int_ = res.register(INT().set_context(context).execute())
            if res.should_return(): return res

            return res.success(int_.set_value(Number(new_value)))
        return res.success(Number(new_value))
    function_FROMOCT.arg_names = ['value']

    def function_BIN(self, node, context):
        str_ = STRING.STRING().set_context(context).execute().value
        int_ = bin(self.get_variable('VALUE').value).lstrip('0b')
        if int_ == '': int_ = '0'

        return RuntimeResult().success(str_.set_value(String(int_)))
    function_BIN.arg_names = []

    def function_FROMBIN(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING.STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))

        try:
            if isinstance(value, STRING.STRING): new_value = int(value.get_variable('VALUE').value, 2)
            else: new_value = int(value.value, 2)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, str(error).capitalize(), context))

        if isinstance(value, STRING.STRING):
            int_ = res.register(INT().set_context(context).execute())
            if res.should_return(): return res
    
            return res.success(int_.set_value(Number(new_value)))
        return res.success(Number(new_value))
    function_FROMBIN.arg_names = ['value']

    def function_STRING(self, node, context):
        str_ = STRING.STRING().set_context(context).execute().value
        return RuntimeResult().success(str_.set_value(String(str(self.get_variable('VALUE').value))))
    function_STRING.arg_names = []

    def function_FROMSTRING(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING.STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))

        try: 
            if isinstance(value, STRING.STRING): new_value = int(value.get_variable('VALUE').value)
            else: new_value = int(value.value)
        except Exception: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, f'Could not convert \'{value.value}\' to an [INT]', context))

        if isinstance(value, STRING.STRING):
            int_ = res.register(INT().set_context(context).execute())
            if res.should_return(): return res

            return res.success(int_.set_value(Number(new_value)))
        return res.success(Number(new_value))
    function_FROMSTRING.arg_names = ['value']