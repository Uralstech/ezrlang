from ezr import Interpreter, RuntimeResult, RuntimeError, VarAccessNode, CallNode, BaseFunction, Nothing, Number, Bool, String, RTE_INCORRECTTYPE
from time import gmtime, localtime, time, sleep

class base_libObject(BaseFunction):
    def __init__(self, name, internal_context=None):
        super().__init__(name)
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
        return RuntimeResult().success(Nothing())

class timestruct_Object(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('TIMESTRUCT', internal_context)

    def update(self, struct):
        self.variable_YEAR       = Number(struct.tm_year)
        self.variable_MONTH      = Number(struct.tm_mon)
        self.variable_MONTH_DAY  = Number(struct.tm_mday)
        self.variable_WEEK_DAY   = Number(struct.tm_wday+1)
        self.variable_YEAR_DAY   = Number(struct.tm_yday)
        self.variable_HOUR       = Number(struct.tm_hour)
        self.variable_MINUTE     = Number(struct.tm_min)
        self.variable_SECOND     = Number(struct.tm_sec)

        self.variable_ZONE       = String(struct.tm_zone)
        self.variable_OFFSET     = Number(struct.tm_gmtoff)

        has_dst = struct.tm_isdst
        if has_dst == 1: self.variable_HAS_DST    = Bool(True)
        elif has_dst == 0: self.variable_HAS_DST  = Bool(False)
        elif has_dst == -1: self.variable_HAS_DST = String('UNKNOWN')

        return self
    
    def update_struct(self, other):
        self.variable_YEAR       = other.variable_YEAR
        self.variable_MONTH      = other.variable_MONTH
        self.variable_MONTH_DAY  = other.variable_MONTH_DAY
        self.variable_WEEK_DAY   = other.variable_WEEK_DAY
        self.variable_YEAR_DAY   = other.variable_YEAR_DAY
        self.variable_HOUR       = other.variable_HOUR
        self.variable_MINUTE     = other.variable_MINUTE
        self.variable_SECOND     = other.variable_SECOND

        self.variable_ZONE       = other.variable_ZONE
        self.variable_OFFSET     = other.variable_OFFSET

        self.variable_HAS_DST    = other.variable_HAS_DST
    
    def copy(self):
        copy = timestruct_Object(self.internal_context)
        copy.set_context(self.context)
        copy.set_pos(self.start_pos, self.end_pos)

        copy.update_struct(self)
        return copy

class lib_Object(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('TIME', internal_context)

    def function_TIME(self, context):
        return RuntimeResult().success(Number(time()))
    function_TIME.arg_names = []

    def function_GMTIME(self, context):
        res = RuntimeResult()

        time = context.symbol_table.get('time')
        if not isinstance(time, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        return res.success(timestruct_Object().update(gmtime(time.value)))
    function_GMTIME.arg_names = ['time']

    def function_LOCALTIME(self, context):
        res = RuntimeResult()

        time = context.symbol_table.get('time')
        if not isinstance(time, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        return res.success(timestruct_Object().update(localtime(time.value)))
    function_LOCALTIME.arg_names = ['time']

    def function_SLEEP(self, context):
        res = RuntimeResult()

        time = context.symbol_table.get('time')
        if not isinstance(time, Number): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        sleep(time.value)
        return res.success(Nothing())
    function_SLEEP.arg_names = ['time']

    def function_READABLE_TIME(self, context):
        res = RuntimeResult()

        time = context.symbol_table.get('timestruct')
        if not isinstance(time, timestruct_Object): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [TIMESTRUCT]', context))

        return res.success(String(f'{time.variable_HOUR}:{time.variable_MINUTE}:{time.variable_SECOND}'))
    function_READABLE_TIME.arg_names = ['timestruct']

    def function_READABLE_DATE(self, context):
        res = RuntimeResult()

        time = context.symbol_table.get('timestruct')
        if not isinstance(time, timestruct_Object): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [TIMESTRUCT]', context))

        return res.success(String(f'{time.variable_MONTH_DAY}:{time.variable_MONTH}:{time.variable_YEAR}'))
    function_READABLE_DATE.arg_names = ['timestruct']