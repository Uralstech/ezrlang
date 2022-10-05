from ezr import RuntimeResult, RuntimeError, Nothing, Number, Bool, RTE_INCORRECTTYPE, RTE_MATH
from Libraries.base.base_libObject import base_libObject
# from ezrlibs.Libraries.base.base_libObject import base_libObject # Debug
from math import ceil, floor, exp, log, pow, sqrt, sin, cos, tan, degrees, radians, isinf, isnan, pi, tau, e, inf, nan

class lib_Object(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('MATH', internal_context)

    def initialize(self, context):
        self.set_variable('PI', Number(pi))
        self.set_variable('TAU', Number(tau))
        self.set_variable('E', Number(e))
        self.set_variable('INF', Number(inf))
        self.set_variable('NAN', Number(nan))

        return RuntimeResult().success(Nothing())
    
    def function_CEIL(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = ceil(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_CEIL.arg_names = ['value']
    
    def function_FLOOR(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = floor(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_FLOOR.arg_names = ['value']
    
    def function_EXP(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = exp(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_EXP.arg_names = ['value']
    
    def function_LOG(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        base = context.symbol_table.get('base')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        if not isinstance(base, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = log(value.value, base.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_LOG.arg_names = ['value', 'base']
    
    def function_POW(self, node, context):
        res = RuntimeResult()

        value_a = context.symbol_table.get('value_a')
        value_b = context.symbol_table.get('value_b')
        if not isinstance(value_a, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        if not isinstance(value_b, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = pow(value_a.value, value_b.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_POW.arg_names = ['value_a', 'value_b']
    
    def function_SQRT(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = sqrt(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_SQRT.arg_names = ['value']
    
    def function_SIN(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = sin(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_SIN.arg_names = ['value']
    
    def function_COS(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = cos(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_COS.arg_names = ['value']
    
    def function_TAN(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = tan(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_TAN.arg_names = ['value']
    
    def function_DEGREES(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = degrees(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_DEGREES.arg_names = ['value']
    
    def function_RADIANS(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = radians(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_RADIANS.arg_names = ['value']
    
    def function_IS_INF(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = isinf(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Bool(return_value))
    function_IS_INF.arg_names = ['value']
    
    def function_IS_NAN(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = isnan(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Bool(return_value))
    function_IS_NAN.arg_names = ['value']