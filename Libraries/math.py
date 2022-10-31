from ezr import RuntimeResult, RuntimeError, Nothing, Number, Bool, RTE_INCORRECTTYPE, RTE_MATH
from math import ceil, floor, exp, log, pow, sqrt, sin, cos, tan, degrees, radians, isinf, isnan, pi, tau, e, inf, nan

from Libraries.base.base_libObject import base_libObject

class lib_Object(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('math', internal_context)

    def initialize(self, context):
        self.set_variable('pi', Number(pi))
        self.set_variable('tau', Number(tau))
        self.set_variable('e', Number(e))
        self.set_variable('inf', Number(inf))
        self.set_variable('nan', Number(nan))

        return RuntimeResult().success(Nothing())
    
    def function_ceil(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = ceil(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_ceil.arg_names = ['value']
    
    def function_floor(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = floor(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_floor.arg_names = ['value']
    
    def function_exp(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = exp(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_exp.arg_names = ['value']
    
    def function_log(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        base = context.symbol_table.get('base')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        if not isinstance(base, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = log(value.value, base.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_log.arg_names = ['value', 'base']
    
    def function_pow(self, node, context):
        res = RuntimeResult()

        value_a = context.symbol_table.get('value_a')
        value_b = context.symbol_table.get('value_b')
        if not isinstance(value_a, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        if not isinstance(value_b, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = pow(value_a.value, value_b.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_pow.arg_names = ['value_a', 'value_b']
    
    def function_sqrt(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = sqrt(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_sqrt.arg_names = ['value']
    
    def function_sin(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = sin(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_sin.arg_names = ['value']
    
    def function_cos(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = cos(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_cos.arg_names = ['value']
    
    def function_tan(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = tan(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_tan.arg_names = ['value']
    
    def function_degrees(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = degrees(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_degrees.arg_names = ['value']
    
    def function_radians(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = radians(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_radians.arg_names = ['value']
    
    def function_isInf(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = isinf(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Bool(return_value))
    function_isInf.arg_names = ['value']
    
    def function_isNan(self, node, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = isnan(value.value)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Bool(return_value))
    function_isNan.arg_names = ['value']