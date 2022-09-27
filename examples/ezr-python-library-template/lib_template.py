# Import needed classes from ezr.py
from ezr import Interpreter, RuntimeResult, RuntimeError, VarAccessNode, CallNode, BaseFunction, Nothing, Bool, Number, String, List, RTE_INCORRECTTYPE

# ezr value classes
# -----------------
#   Value() -> Parent of all value classes
#   BaseFunction(name) -> Parent of Functions and Objects
#
#   Nothing() -> NOTHING value
#
#   Bool(True/False) -> Boolean value
#       'Bool(True)' -> Boolean value of True
#   Number(value) -> Int/Float value
#       'Number(4)' -> Int value of 4
#       'Number(4.45)' -> Float value of 4.45
#   String(value) -> Str value
#       'String('Hello!')' -> Str value of 'Hello!'
#   List(values) -> List of any values
#       'List([String('t'), Number(3), Bool(False)])' -> List of values ['t', 3, False]
#
#   Function(name, body_node, arg_names, should_auto_return) -> Function definition
#   Object(name, body_node, arg_names) -> Object definition
#
# It is not recommended to use ezrs' Function or Object classes
# other than for inheritance; Use Python functions/objects instead
# NOTE: The Value and BaseFunction class are ONLY for inheritance, all others can be returned
# Refer to ezr.py for the code for these classes

# RuntimeResult and error handling
# --------------------------------
# RuntimeResult is the class used for registering expressions and checking for
# errors and SKIP, STOP and RETURN calls
# All functions should have a RuntimeResult().success(return-value) call
# as that is how ezr checks for error, or the lack thereof
# To throw errors, use the failure function in RuntimeResult and return it
# eg: return RuntimeResult().failure(RuntimeError(self.start_pos, self.end_pos, ERROR_TAG, 'Error message', self.context))
# Error tags are str values used to catch errors in the TRY statement
# An error tag can be as simple as this: EXAMPLE_ERRORTAG = 'EXAMPLE-ERRORTAG'
# Any errors thrown with this tag will be caught by TRY statements using the 'EXAMPLE-ERRORTAG' tag
# You can import any error class from ezr.py, such as:
#   UnknownCharError(start_pos, end_pos, details) -> Raised when any undefined characters are found
#   InvalidSyntaxError(start_pos, end_pos, details) -> Raised when the expected syntax is not found
#   RuntimeError(start_pos, end_pos, error_type, details, context) -> Any errors caused while running the code
# It is recommended to only use the RuntimeError class for libraries
# You can also make your own error class by inheriting from the base Error class or the RuntimeError class
# It is recommended to only use the built-in error tags that ezr.py provides; They can be imported into any project
#   RTE_DEFAULT        = 'RUNTIME'
#   RTE_CUSTOM         = 'CUSTOM'
#   RTE_ILLEGALOP      = 'ILLEGAL-OPERATION'
#   RTE_UNDEFINEDVAR   = 'UNDEFINED-VAR'
#   RTE_IDXOUTOFRANGE  = 'INDEX-OUT-OF-RANGE'
#   RTE_TOOMANYARGS    = 'TOO-MANY-FUNCTION-ARGS'
#   RTE_TOOFEWARGS     = 'TOO-FEW-FUNCTION-ARGS'
#   RTE_INCORRECTTYPE  = 'INCORRECT-TYPE'
#   RTE_MATH		   = 'MATH'
#   RTE_FILEREAD	   = 'FILE-READ'
#   RTE_FILEWRITE	   = 'FILE-WRITE'
#   RTE_RUNFILE 	   = 'RUN-FILE'
# More details about these error tags are available in the ezr documentation

# Create main object
# The name HAS to be 'lib_Object', otherwise ezr will show an error
class lib_Object(BaseFunction):
    # Initialization
    def __init__(self, internal_context=None):
        # Replace 'lib_template' with your librarys' name
        super().__init__('IO')
        
        # Set the internal context
        self.internal_context = internal_context

    # Populating the arguments for function calls
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
    
    # Checking no. of args and populating them
    def check_and_populate_args(self, arg_names, args, context):
        res = RuntimeResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        res.register(self.populate_args(arg_names, args, context))
        if res.should_return(): return res
        return res.success(Nothing())
    
    # Function called at initialization
    def execute(self):
        res = RuntimeResult()
        
        # Generate internal context
        self.internal_context = self.generate_context()

        # Call the initialize function
        res.register(self.initialize(self.internal_context))

        # Return if any error
        if res.should_return(): return res

        # Return a copy of self
        return res.success(self.copy())
    
    # Function to 'retrieve' variables/functions from object
    def retrieve(self, node):
        res = RuntimeResult()
        
        # For VarAccessNodes (Variable access)
        if isinstance(node, VarAccessNode):
            # Retrieving variable from object, defaulting to NOTHING
            return_value = self.get_variable(node.var_name_token.value)

        # For CallNodes (Function/object calls)
        elif isinstance(node, CallNode):
            # Getting function name
            method_name = f'function_{node.node_to_call.var_name_token.value}'
            
            # Retrieving function from object, defaulting to NOTHING
            method = getattr(self, method_name, Nothing())

            # If method is not NOTHING
            if not isinstance(method, Nothing):
                # Check and populate args
                res.register(self.check_and_populate_args(method.arg_names, node.arg_nodes, self.internal_context))
                
                # Return if any error
                if res.should_return(): return res

                # Call the function itself
                return_value = res.register(method(node, self.internal_context))

                # Return if any error
                if res.should_return(): return res

            # If method is NOTHING, the return value is also NOTHING
            else: return_value = method
        
        # If any other node is given, raise an error
        else: raise Exception(f'Unknown node type {type(node).__name__}!')

        # Return the value
        return res.success(return_value)

    # Setting variable in internal context
    def set_variable(self, name, value):
        self.internal_context.symbol_table.set(name, value)

    # Getting variable from internal context
    def get_variable(self, name):
        var_ = self.internal_context.symbol_table.get(name)
        return var_ if var_ else Nothing()

    # Copying the object
    def copy(self):
        copy = lib_Object(self.internal_context)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)

        return copy

    # String representation of the object
    def __repr__(self):
        return f'<object {self.name}>'

    # Start of your code

    # Initialization function called at, well, initialization
    # This has to be called 'initialize' unless changed in the execute function
    def initialize(self, context):
        print('lib_tempalte initialized!')
        
        # Define your variables in the internal context!
        self.set_variable('test_var', String('Variable'))

        return RuntimeResult().success(Nothing())

    # All functions should start with 'function_', unless changed in the retrieve function
    def function_test_func(self, node, context):
        print('Function')

        return RuntimeResult().success(Nothing())
    function_test_func.arg_names = [] # Name of the args the function has to take in

    def function_change_test_var(self, node, context):
        new_value = context.symbol_table.get('new') # Retrieving arg 'new' from symbol table
        self.set_variable('test_var', new_value)

        return RuntimeResult().success(Nothing())
    function_change_test_var.arg_names = ['new']

    def function_test_add(self, node, context):
        res = RuntimeResult()
        val_a = context.symbol_table.get('val_a')
        val_b = context.symbol_table.get('val_b')

        if not isinstance(val_a, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument has to be a [NUMBER]', self.context))
        if not isinstance(val_b, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument has to be a [NUMBER]', self.context))

        return res.success(Number(val_a.value + val_b.value))
    function_test_add.arg_names = ['val_a', 'val_b']