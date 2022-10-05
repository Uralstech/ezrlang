from ezr import RuntimeResult, RuntimeError, Value, Nothing, Number, Bool, String, List, RTE_INCORRECTTYPE, RTE_MATH
from Libraries.base.base_libObject import base_libObject
import Libraries.stdlib.INT as INT
import Libraries.stdlib.STRING as STRING
# from ezrlibs.Libraries.base.base_libObject import base_libObject # Debug
# import ezrlibs.Libraries.stdlib.INT as INT # Debug
# import ezrlibs.Libraries.stdlib.STRING as STRING # Debug

class FLOAT(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('FLOAT', internal_context)
        
    def copy(self):
        copy = FLOAT(self.internal_context)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)

        return copy

    def new_object(self):
        return FLOAT().set_context(self.context).execute().value
        
    def set_value(self, value):
        self.set_variable('VALUE', Number(float(value.value)))
        return self

    def initialize(self, context):
        self.set_variable('PRECISION', Number(5))
        return RuntimeResult().success(Nothing())

    # Operations
    
    def added_to(self, other):
        if isinstance(other, Number): return Number(self.get_variable('VALUE').value + other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return self.new_object().set_value(Number(self.get_variable('VALUE').value + other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number): return Number(self.get_variable('VALUE').value - other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return self.new_object().set_value(Number(self.get_variable('VALUE').value - other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)
        
    def multed_by(self, other):
        if isinstance(other, Number): return Number(self.get_variable('VALUE').value * other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return self.new_object().set_value(Number(self.get_variable('VALUE').value * other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number): 
            if other.value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Division by zero', self.context)
            return Number(self.get_variable('VALUE').value / other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT):
            if other.get_variable('VALUE').value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Division by zero', self.context)
            return self.new_object().set_value(Number(self.get_variable('VALUE').value / other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)

    def moded_by(self, other):
        if isinstance(other, Number): 
            if other.value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Modulo by zero', self.context)
            return Number(self.get_variable('VALUE').value % other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT):
            if other.get_variable('VALUE').value == 0: return None, RuntimeError(other.start_pos, other.end_pos, RTE_MATH, 'Modulo by zero', self.context)
            return self.new_object().set_value(Number(self.get_variable('VALUE').value % other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number): return Number(self.get_variable('VALUE').value ** other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return self.new_object().set_value(Number(self.get_variable('VALUE').value ** other.get_variable('VALUE').value)), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_eq(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value == other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return Bool(self.get_variable('VALUE').value == other.get_variable('VALUE').value).set_context(self.context), None
        elif isinstance(other, Nothing): return Bool(False).set_context(self.context), None
        elif isinstance(other, Bool): return Bool(self.is_true() == other.value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_ne(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value != other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return Bool(self.get_variable('VALUE').value != other.get_variable('VALUE').value).set_context(self.context), None
        elif isinstance(other, Nothing): return Bool(True).set_context(self.context), None
        elif isinstance(other, Bool): return Bool(self.is_true() != other.value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_lt(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value < other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return Bool(self.get_variable('VALUE').value < other.get_variable('VALUE').value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_gt(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value > other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return Bool(self.get_variable('VALUE').value > other.get_variable('VALUE').value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_lte(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value <= other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return Bool(self.get_variable('VALUE').value <= other.get_variable('VALUE').value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_gte(self, other):
        if isinstance(other, Number): return Bool(self.get_variable('VALUE').value >= other.value).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return Bool(self.get_variable('VALUE').value >= other.get_variable('VALUE').value).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
    
    def compare_and(self, other):
        if isinstance(other, Number): return Bool(self.is_true() and other.is_true()).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return Bool(self.is_true() and other.is_true()).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
        
    def compare_or(self, other):
        if isinstance(other, Number): return Bool(self.is_true() or other.is_true()).set_context(self.context), None
        elif isinstance(other, FLOAT) or isinstance(other, INT.INT): return Bool(self.is_true() or other.is_true()).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)
    
    def check_in(self, other):
        if isinstance(other, List):
            for v in other.elements:
                if isinstance(v, FLOAT) and v.get_variable('VALUE').value == self.get_variable('VALUE').value: return Bool(True).set_context(self.context), None
            return Bool(False).set_context(self.context), None
        else: return None, Value.illegal_operation(self, other)

    def invert(self):
        return self.new_object().set_value(Number(1 if self.get_variable('VALUE').value == 0 else 0)), None

    def is_true(self):
        return self.get_variable('VALUE').value != 0

    # Functions
    
    def function_HEX(self, node, context):
        str_ = STRING.STRING().set_context(context).execute().value
        return RuntimeResult().success(str_.set_value(String(float.hex(self.get_variable('VALUE').value).lstrip('0x'))))
    function_HEX.arg_names = []

    def function_FROMHEX(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING.STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))

        try:
            if isinstance(value, STRING.STRING): new_value = float.fromhex(value.get_variable('VALUE').value)
            else: new_value = float.fromhex(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, str(error).capitalize(), context))

        if isinstance(value, STRING.STRING):
            float_ = res.register(FLOAT().set_context(context).execute())
            if res.should_return(): return res

            return res.success(float_.set_value(Number(new_value)))
        return res.success(Number(new_value))
    function_FROMHEX.arg_names = ['value']

    def function_OCT(self, node, context):
        num, dec = str(self.get_variable('VALUE').value).split('.')
        num, dec = int(num), int(dec)

        result = oct(num).lstrip('0o') + '.'
        if result == '.': result = '0.'

        for _ in range(int(self.get_variable('PRECISION').value)):
            while dec > 1: dec /= 10
            num, dec = str(float(dec * 8)).split('.')

            dec = int(dec)
            result += num

        str_ = STRING.STRING().set_context(context).execute().value
        return RuntimeResult().success(str_.set_value(String(result)))
    function_OCT.arg_names = []

    def function_BIN(self, node, context):
        num, dec = str(self.get_variable('VALUE').value).split('.')
        num, dec = int(num), int(dec)
        
        result = bin(num).lstrip('0b') + '.'
        if result == '.': result = '0.'

        for _ in range(int(self.get_variable('PRECISION').value)):
            while dec > 1: dec /= 10
            num, dec = str(float(dec * 2)).split('.')

            dec = int(dec)
            result += num

        str_ = STRING.STRING().set_context(context).execute().value
        return RuntimeResult().success(str_.set_value(String(result)))
    function_BIN.arg_names = []

    def function_STRING(self, node, context):
        str_ = STRING.STRING().set_context(context).execute().value
        return RuntimeResult().success(str_.set_value(String(str(self.get_variable('VALUE').value))))
    function_STRING.arg_names = []

    def function_FROMSTRING(self, node, context):
        res = RuntimeResult()
        value = context.symbol_table.get('value')

        if not isinstance(value, String) and not isinstance(value, STRING.STRING): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING] or STD.STRING', context))

        try:
            if isinstance(value, STRING.STRING): new_value = float(value.get_variable('VALUE').value)
            else: new_value = float(value.value)
        except Exception: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, f'Could not convert \'{value.value}\' to a [FLOAT]', context))

        if isinstance(value, STRING.STRING):
            float_ = res.register(FLOAT().set_context(context).execute())
            if res.should_return(): return res

            return res.success(float_.set_value(Number(new_value)))
        return res.success(Number(new_value))
    function_FROMSTRING.arg_names = ['value']

    def function_ISINTEGER(self, node, context):
        return RuntimeResult().success(Bool(self.get_variable('VALUE').value.is_integer()))
    function_ISINTEGER.arg_names = []

    def function_ROUND(self, node, context):
        res = RuntimeResult()
        pres = context.symbol_table.get('precision')
        if not isinstance(pres, Number) and not isinstance(pres, INT.INT): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT], [FLOAT] or STD.INT', context))

        if isinstance(pres, INT.INT):
            float_ = res.register(FLOAT().set_context(context).execute())
            if res.should_return(): return res

            return res.success(float_.set_value(Number(round(self.get_variable('VALUE').value, int(pres.value)))))
        return res.success(Number(round(self.get_variable('VALUE').value, int(pres.value))))
    function_ROUND.arg_names = ['precision']

    def function_PRECISION(self, node, context):
        res = RuntimeResult()
        pres = context.symbol_table.get('precision')
        if not isinstance(pres, Number) and not isinstance(pres, INT.INT): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT], [FLOAT] or STD.INT', context))

        if isinstance(pres, INT.INT): self.set_variable('PRECISION', Number(int(pres.get_variable('VALUE').value)))
        else: self.set_variable('PRECISION', Number(int(pres.value)))

        return res.success(Nothing())
    function_PRECISION.arg_names = ['precision']