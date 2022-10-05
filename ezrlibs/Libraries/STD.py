from ezr import RuntimeResult, RuntimeError, Nothing, Number, String, RTE_INCORRECTTYPE
from Libraries.base.base_libObject import base_libObject
from Libraries.stdlib.INT import INT
from Libraries.stdlib.FLOAT import FLOAT
from Libraries.stdlib.STRING import STRING
# from ezrlibs.Libraries.base.base_libObject import base_libObject # Debug
# from ezrlibs.Libraries.stdlib.INT import INT # Debug
# from ezrlibs.Libraries.stdlib.FLOAT import FLOAT # Debug
# from ezrlibs.Libraries.stdlib.STRING import STRING # Debug

# This library is a WIP

class lib_Object(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('STD', internal_context)

    def initialize(self, context):
        res = RuntimeResult()

        int_ = res.register(INT().set_context(context).set_pos(self.start_pos, self.end_pos).execute())
        if res.should_return(): return res
        int_ = int_.set_value(Number(0))
        self.set_variable('INT', int_)

        float_ = res.register(FLOAT().set_context(context).set_pos(self.start_pos, self.end_pos).execute())
        if res.should_return(): return res
        float_ = float_.set_value(Number(0.0))
        self.set_variable('FLOAT', float_)

        string_ = res.register(STRING().set_context(context).set_pos(self.start_pos, self.end_pos).execute())
        if res.should_return(): return res
        string_ = string_.set_value(String(''))
        self.set_variable('STRING', string_)

        return res.success(Nothing())
    
    def function_INT(self, node, context):
        res = RuntimeResult()
        
        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        return_value = res.register(INT().set_context(context).execute())
        if res.should_return(): return res

        return res.success(return_value.set_value(Number(int(value.value))))
    function_INT.arg_names = ['value']
    
    def function_FLOAT(self, node, context):
        res = RuntimeResult()
        
        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        return_value = res.register(FLOAT().set_context(context).execute())
        if res.should_return(): return res

        return res.success(return_value.set_value(Number(float(value.value))))
    function_FLOAT.arg_names = ['value']
    
    def function_STRING(self, node, context):
        res = RuntimeResult()
        
        value = context.symbol_table.get('value')
        return_value = res.register(STRING().set_context(context).execute())
        if res.should_return(): return res

        return res.success(return_value.set_value(String(str(value.value))))
    function_STRING.arg_names = ['value']