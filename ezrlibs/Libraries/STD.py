from ezr import RuntimeResult, RuntimeError, Nothing, Number, RTE_INCORRECTTYPE
# from Libraries.base.base_libObject import base_libObject
# from Libraries.stdlib.INT import INT
from ezrlibs.Libraries.base.base_libObject import base_libObject # Debug
from ezrlibs.Libraries.stdlib.INT import INT # Debug

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

        return res.success(Nothing())

    def copy(self):
        copy = lib_Object(self.internal_context)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)

        return copy
    
    def function_INT(self, node, context):
        res = RuntimeResult()
        
        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        return_value = res.register(INT().set_context(context).set_pos(node.start_pos, node.end_pos).execute())
        if res.should_return(): return res

        return res.success(return_value.set_value(Number(int(value.value))))
    function_INT.arg_names = ['value']