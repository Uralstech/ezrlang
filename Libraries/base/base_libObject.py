from ezr import Interpreter, RuntimeResult, RuntimeError, VarAccessNode, CallNode, ObjectCallNode, BaseFunction, Nothing, RTE_UNDEFINEDVAR, RTE_INCORRECTTYPE

class base_libObject(BaseFunction):
    def __init__(self, name, internal_context=None):
        super().__init__(name)
        self.internal_context = internal_context
        
    def execute(self):
        res = RuntimeResult()
        self.internal_context = self.generate_context()

        res.register(self.initialize(self.internal_context))

        if res.should_return(): return res
        return res.success(self.copy())
    
    def retrieve_and_call_function(self, node):
        res = RuntimeResult()
        interpreter = Interpreter()
        args = []

        for arg_node in node.arg_nodes:
            args.append(res.register(interpreter.visit(arg_node, self.context)))
            if res.should_return(): return res
        
        call_name = node.node_to_call.var_name_token.value
        method_name = f'function_{call_name}'
        method = getattr(self, method_name, None)

        if method:
            res.register(self.check_and_populate_args(method.arg_names, args, self.internal_context))
            if res.should_return(): return res

            return_value = res.register(method(node, self.internal_context))
            if res.should_return(): return res

            return res.success(return_value)
        return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_UNDEFINEDVAR, f'\'{call_name}\' is not defined', self.internal_context))

    def retrieve_variable(self, node):
        res = RuntimeResult()

        var_name = node.var_name_token.value
        return_value = self.get_variable(var_name, None)
        
        if return_value: return res.success(return_value)
        error =  res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_UNDEFINEDVAR, f'\'{var_name}\' is not defined', self.internal_context))
        return error

    def retrieve(self, node):
        res = RuntimeResult()

        if isinstance(node, VarAccessNode):
            return_value = res.register(self.retrieve_variable(node))
            if res.should_return(): return res
        elif isinstance(node, CallNode):
            return_value = res.register(self.retrieve_and_call_function(node))
            if res.should_return(): return res
        elif isinstance(node, ObjectCallNode):
            if not isinstance(node.object_node, (VarAccessNode, CallNode, ObjectCallNode)):
                return res.failure(RuntimeError(node.object_node.start_pos, node.object_node.end_pos, RTE_INCORRECTTYPE, f'Unknown node type \'{type(node.object_node).__name__}\'', self.internal_context))

            if isinstance(node.object_node, VarAccessNode):
                object_ = res.register(self.retrieve_variable(node.object_node))
                if res.should_return(): return res
            elif isinstance(node.object_node, (CallNode, ObjectCallNode)):
                object_ = res.register(self.retrieve_and_call_function(node.object_node))
                if res.should_return(): return res

            object_.set_context(self.context).set_pos(node.start_pos, node.end_pos)
            return_value = res.register(object_.retrieve(node.node_to_call))
            if res.should_return(): return res
        else: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, f'Unknown node type \'{type(node).__name__}\'', self.internal_context))
        
        return res.success(return_value.copy().set_context(self.context).set_pos(node.start_pos, node.end_pos))
    
    def set_variable(self, name, value):
        self.internal_context.symbol_table.set(name, value)
    
    def get_variable(self, name, default=Nothing()):
        return_value = self.internal_context.symbol_table.get(name)
        return return_value if return_value else default
    
    def copy(self):
        copy = object.__new__(type(self))
        copy.__init__(self.internal_context)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)

        return copy
    
    def __repr__(self):
        return f'<libObject {self.name}>'
    
    def initialize(self, context):
        return RuntimeResult().success(Nothing())