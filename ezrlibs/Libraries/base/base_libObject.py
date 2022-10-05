from ezr import Interpreter, RuntimeResult, RuntimeError, VarAccessNode, CallNode, ObjectCallNode, BaseFunction, Nothing, RTE_INCORRECTTYPE

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

    def execute(self):
        res = RuntimeResult()
        self.internal_context = self.generate_context()

        res.register(self.initialize(self.internal_context))

        if res.should_return(): return res
        return res.success(self.copy())

    def retrieve(self, node):
        res = RuntimeResult()

        if isinstance(node, VarAccessNode):
            return_value = self.get_variable(node.var_name_token.value)
        elif isinstance(node, CallNode):
            method_name = f'function_{node.node_to_call.var_name_token.value}'
            method = getattr(self, method_name, Nothing())

            if not isinstance(method, Nothing):
                res.register(self.check_and_populate_args(method.arg_names, node.arg_nodes, self.internal_context))
                if res.should_return(): return res
                
                return_value = res.register(method(node, self.internal_context))
                if res.should_return(): return res
            else: return_value = method
        elif isinstance(node, ObjectCallNode):
            if isinstance(node.object_node, VarAccessNode):
                return_value = self.get_variable(node.object_node.var_name_token.value)
                
                if not isinstance(return_value, Nothing):
                    return_value = res.register(return_value.retrieve(node.node_to_call))
                    if res.should_return(): return res
                else: return_value = return_value
            elif isinstance(node.object_node, CallNode) or isinstance(node.object_node, ObjectCallNode):
                method_name = f'function_{node.object_node.node_to_call.var_name_token.value}'
                method = getattr(self, method_name, Nothing())

                if not isinstance(method, Nothing):
                    res.register(self.check_and_populate_args(method.arg_names, node.object_node.arg_nodes, self.internal_context))
                    if res.should_return(): return res

                    value = res.register(method(node, self.internal_context))
                    if res.should_return(): return res

                    return_value = res.register(value.retrieve(node.node_to_call))
                    if res.should_return(): return res
                else: return_value = method
            else: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, f'Unknown node type {type(node.object_node).__name__}!', self.internal_context))
        else: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, f'Unknown node type {type(node).__name__}!', self.internal_context))
        
        return res.success(return_value.set_context(self.context).set_pos(node.start_pos, node.end_pos))
    
    def set_variable(self, name, value):
        self.internal_context.symbol_table.set(name, value)
    
    def get_variable(self, name):
        var_ = self.internal_context.symbol_table.get(name)
        return var_ if var_ else Nothing()
    
    def copy(self):
        copy = object.__new__(type(self))
        copy.__init__(self.internal_context)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)

        return copy
    
    def __repr__(self):
        return f'<object {self.name}>'
    
    def initialize(self, context):
        return RuntimeResult().success(Nothing())