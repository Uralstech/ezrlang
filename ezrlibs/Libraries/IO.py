from ezr import Interpreter, RuntimeResult, RuntimeError, VarAccessNode, CallNode, BaseFunction, Nothing, String, List, RTE_INCORRECTTYPE, RTE_IO
from os import remove, mkdir, rmdir

class lib_Object(BaseFunction):
    def __init__(self, internal_context=None):
        super().__init__('IO')
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
        
    def function_READ(self, context):
        res = RuntimeResult()
        fn = context.symbol_table.get('filepath')
        mode = context.symbol_table.get('mode')

        if not isinstance(fn, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        if not isinstance(mode, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be a [STRING]', context))

        mode = mode.value
        if mode not in ['READ', 'READ_LINE', 'READ_LINES']: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be \'READ\', \'READ_LINE\' or \'READ_LINES\'', context))

        fn = fn.value
        try:
            data = None
            with open(fn, 'r') as f:
                if mode == 'READ': data = f.read()
                elif mode == 'READ_LINE': data = f.readline()
                elif mode == 'READ_LINES': data = f.readlines()
                else: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be \'READ\', \'READ_LINE\' or \'READ_LINES\'', context))
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_IO, f'Failed to load data from \'{fn}\'\n{str(error)}', context))
        
        output = Nothing()
        if isinstance(data, str): output = String(data)
        else:
            elements = []
            for i in data: elements.append(String(i))
            output = List(elements)

        return res.success(output)
    function_READ.arg_names = ['filepath', 'mode']

    def function_WRITE(self, context):
        res = RuntimeResult()
        fn = context.symbol_table.get('filepath')
        mode = context.symbol_table.get('mode')
        data = context.symbol_table.get('data')
        
        if not isinstance(fn, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        if not isinstance(mode, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be a [STRING]', context))
        if isinstance(data, BaseFunction): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Third argument cannot be a [FUNCTION]', context))
        
        mode = mode.value
        if mode not in ['OVERWRITE', 'EXTEND']: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Second argument must be \'OVERWRITE\' or \'EXTEND\'', context))
        
        if isinstance(data, List):
            data_temp = ''
            for i in data.elements:
                if isinstance(i, BaseFunction): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'Third argument cannot contain a [FUNCTION]', context))
                data_temp = f'{data_temp}\n{str(i)}'
            data = data_temp
        else: data = str(data.value)
        
        fn = fn.value
        try:
            if mode == 'OVERWRITE':
                with open(fn, 'w') as f: f.write(data)
            else:
                with open(fn, 'a') as f: f.write(data)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_IO, f'Failed to write data to \'{fn}\'\n{str(error)}', context))
        
        return res.success(Nothing())
    function_WRITE.arg_names = ['filepath', 'mode', 'data']

    def function_DELETE(self, context):
        res = RuntimeResult()
        fn = context.symbol_table.get('filepath')
        if not isinstance(fn, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        
        fn = fn.value
        try: remove(fn)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_IO, f'Failed to delete file \'{fn}\'\n{str(error)}', context))

        return res.success(Nothing())
    function_DELETE.arg_names = ['filepath']

    def function_CREATE_DIR(self, context):
        res = RuntimeResult()
        dn = context.symbol_table.get('dirpath')
        if not isinstance(dn, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        
        dn = dn.value
        try: mkdir(dn)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_IO, f'Failed to create directory \'{dn}\'\n{str(error)}', context))

        return res.success(Nothing())
    function_CREATE_DIR.arg_names = ['dirpath']

    def function_DELETE_DIR(self, context):
        res = RuntimeResult()
        dn = context.symbol_table.get('dirpath')
        if not isinstance(dn, String): return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        
        dn = dn.value
        try: rmdir(dn)
        except Exception as error: return res.failure(RuntimeError(self.start_pos, self.end_pos, RTE_IO, f'Failed to delete directory \'{dn}\'\n{str(error)}', context))

        return res.success(Nothing())
    function_DELETE_DIR.arg_names = ['dirpath']