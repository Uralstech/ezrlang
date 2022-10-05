from ezr import RuntimeResult, RuntimeError, BaseFunction, Nothing, String, List, RTE_INCORRECTTYPE, RTE_IO
from Libraries.base.base_libObject import base_libObject
# from ezrlibs.Libraries.base.base_libObject import base_libObject # Debug
from os import remove, mkdir, rmdir

class lib_Object(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('IO', internal_context)

    def initialize(self, context):
        return RuntimeResult().success(Nothing())
        
    def function_READ(self, node, context):
        res = RuntimeResult()
        fn = context.symbol_table.get('filepath')
        mode = context.symbol_table.get('mode')

        if not isinstance(fn, String): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        if not isinstance(mode, String): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be a [STRING]', context))

        mode = mode.value
        if mode not in ['READ', 'READ_LINE', 'READ_LINES']: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be \'READ\', \'READ_LINE\' or \'READ_LINES\'', context))

        fn = fn.value
        try:
            data = None
            with open(fn, 'r') as f:
                if mode == 'READ': data = f.read()
                elif mode == 'READ_LINE': data = f.readline()
                elif mode == 'READ_LINES': data = f.readlines()
                else: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be \'READ\', \'READ_LINE\' or \'READ_LINES\'', context))
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'Failed to load data from \'{fn}\'\n{str(error)}', context))
        
        output = Nothing()
        if isinstance(data, str): output = String(data)
        else:
            elements = []
            for i in data: elements.append(String(i))
            output = List(elements)

        return res.success(output)
    function_READ.arg_names = ['filepath', 'mode']

    def function_WRITE(self, node, context):
        res = RuntimeResult()
        fn = context.symbol_table.get('filepath')
        mode = context.symbol_table.get('mode')
        data = context.symbol_table.get('data')
        
        if not isinstance(fn, String): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        if not isinstance(mode, String): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be a [STRING]', context))
        if isinstance(data, BaseFunction): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Third argument cannot be a [FUNCTION]', context))
        
        mode = mode.value
        if mode not in ['OVERWRITE', 'EXTEND']: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be \'OVERWRITE\' or \'EXTEND\'', context))
        
        if isinstance(data, List):
            data_temp = ''
            for i in data.elements:
                if isinstance(i, BaseFunction): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Third argument cannot contain a [FUNCTION]', context))
                data_temp = f'{data_temp}\n{str(i)}'
            data = data_temp
        else: data = str(data.value)
        
        fn = fn.value
        try:
            if mode == 'OVERWRITE':
                with open(fn, 'w') as f: f.write(data)
            else:
                with open(fn, 'a') as f: f.write(data)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'Failed to write data to \'{fn}\'\n{str(error)}', context))
        
        return res.success(Nothing())
    function_WRITE.arg_names = ['filepath', 'mode', 'data']

    def function_DELETE(self, node, context):
        res = RuntimeResult()
        fn = context.symbol_table.get('filepath')
        if not isinstance(fn, String): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        
        fn = fn.value
        try: remove(fn)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'Failed to delete file \'{fn}\'\n{str(error)}', context))

        return res.success(Nothing())
    function_DELETE.arg_names = ['filepath']

    def function_CREATE_DIR(self, node, context):
        res = RuntimeResult()
        dn = context.symbol_table.get('dirpath')
        if not isinstance(dn, String): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        
        dn = dn.value
        try: mkdir(dn)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'Failed to create directory \'{dn}\'\n{str(error)}', context))

        return res.success(Nothing())
    function_CREATE_DIR.arg_names = ['dirpath']

    def function_DELETE_DIR(self, node, context):
        res = RuntimeResult()
        dn = context.symbol_table.get('dirpath')
        if not isinstance(dn, String): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [STRING]', context))
        
        dn = dn.value
        try: rmdir(dn)
        except Exception as error: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_IO, f'Failed to delete directory \'{dn}\'\n{str(error)}', context))

        return res.success(Nothing())
    function_DELETE_DIR.arg_names = ['dirpath']