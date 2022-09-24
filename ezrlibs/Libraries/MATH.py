from ezr import Interpreter, RuntimeResult, RuntimeError, VarAccessNode, CallNode, BaseFunction, Nothing, Number, Bool, RTE_INCORRECTTYPE, RTE_MATH
from math import ceil, floor, exp, log, pow, sqrt, sin, cos, tan, degrees, radians, isinf, isnan, pi, tau, e, inf, nan

class lib_Object(BaseFunction):
    def __init__(self, internal_context=None):
        super().__init__('MATH')
        self.internal_context = internal_context

    def populate_args(self, arg_names, args, context):
        res = RuntimeResult()
        interpreter = Interpreter()

        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = res.register(interpreter.visit(args[i], self.internal_context))
            if res.should_return(): return res

            arg_value.set_context(context)
            context.symbol_table.set(arg_name, arg_value)
        return res.success(Nothing())
    
    def check_and_populate_args(self, arg_names, args, context):
        res = RuntimeResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        res.register(self.populate_args(arg_names, args, context))
        if res.should_return(): return res
        return res.success(Nothing())
        
    def copy(self):
        return self

    def __repr__(self):
        return f'<object {self.name}>'

    def execute(self):
        res = RuntimeResult()

        self.internal_context = self.generate_context()
        res.register(self.initialize(self.internal_context))
        if res.should_return(): return res

        return res.success(self.copy())
    
    def retrieve(self, node):
        res = RuntimeResult()
        
        if isinstance(node, VarAccessNode):
            value_name = f'variable_{node.var_name_token.value}'
            return_value = getattr(self, value_name, Nothing())
        elif isinstance(node, CallNode):
            method_name = f'function_{node.node_to_call.var_name_token.value}'
            method = getattr(self, method_name, Nothing())

            if not isinstance(method, Nothing):
                res.register(self.check_and_populate_args(method.arg_names, node.arg_nodes, self.internal_context))
                if res.should_return(): return res

                return_value = res.register(method(self.internal_context))
                if res.should_return(): return res
            else: return_value = method
        else: raise Exception(f'Unknown node type {type(node).__name__}!')

        return res.success(return_value)

    def initialize(self, context):
        self.variable_PI = Number(pi)
        self.variable_TAU = Number(tau)
        self.variable_E = Number(e)
        self.variable_INF = Number(inf)
        self.variable_NAN = Number(nan)

        return RuntimeResult().success(Nothing())
    
    def function_CEIL(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = ceil(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_CEIL.arg_names = ['value']
    
    def function_FLOOR(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = floor(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_FLOOR.arg_names = ['value']
    
    def function_EXP(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = exp(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_EXP.arg_names = ['value']
    
    def function_LOG(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        base = context.symbol_table.get('base')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        if not isinstance(base, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = log(value.value, base.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_LOG.arg_names = ['value', 'base']
    
    def function_POW(self, context):
        res = RuntimeResult()

        value_a = context.symbol_table.get('value_a')
        value_b = context.symbol_table.get('value_b')
        if not isinstance(value_a, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        if not isinstance(value_b, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = pow(value_a.value, value_b.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_POW.arg_names = ['value_a', 'value_b']
    
    def function_SQRT(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = sqrt(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_SQRT.arg_names = ['value']
    
    def function_SIN(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = sin(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_SIN.arg_names = ['value']
    
    def function_COS(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = cos(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_COS.arg_names = ['value']
    
    def function_TAN(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = tan(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_TAN.arg_names = ['value']
    
    def function_DEGREES(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = degrees(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_DEGREES.arg_names = ['value']
    
    def function_RADIANS(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = radians(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Number(return_value))
    function_RADIANS.arg_names = ['value']
    
    def function_IS_INF(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = isinf(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Bool(return_value))
    function_IS_INF.arg_names = ['value']
    
    def function_IS_NAN(self, context):
        res = RuntimeResult()

        value = context.symbol_table.get('value')
        if not isinstance(value, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', self.context))
        
        try: return_value = isnan(value.value)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_MATH, str(error).capitalize(), self.context))

        return res.success(Bool(return_value))
    function_IS_NAN.arg_names = ['value']