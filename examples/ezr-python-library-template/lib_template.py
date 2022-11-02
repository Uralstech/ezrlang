# Import needed classes from ezr.py
from ezr import RuntimeResult, RuntimeError, Nothing, Number, String, RTE_INCORRECTTYPE
from Libraries.base.base_libObject import base_libObject

# ezr value classes
# -----------------
#   Value() -> Parent of all returnable value classes
#   BaseFunction(name) -> Parent of Functions, Objects and Function-derivatives
#
#   Nothing() -> NOTHING value
#
#   Bool(True / False) -> Boolean value
#       'Bool(True)' -> true
#   Number(value) -> Int / Float value
#       'Number(4)' -> 4
#       'Number(4.45)' -> 4.45
#   String(value) -> Str value
#       'String('Hello!')' -> 'Hello!'
#   List(values) -> List of any values
#       'List([String('t'), Number(3), Bool(False)])' -> ['t', 3, false]
#   Dict(pairs) -> Dictionary of any values
#       'key1 = String('t'); key2 = Bool(False)
#        Dict({hash(key1):(key1, Number(3)), hash(key2):(key2, List([Number(4)]))})' -> {'t' : 3, false : [4]}
#
#   Function(name, body_node, arg_names, should_auto_return) -> Function definition
#   Object(name, body_node, arg_names) -> Object definition
#
# NOTE: Dictionary keys must be hashable.
# The Value and BaseFunction class are ONLY for inheritance, all others can be returned as output.
# Refer to ezr.py for the code for these classes.

# RuntimeResult and error handling
# --------------------------------
# RuntimeResult is the class used for registering expressions and checking for errors and SKIP, STOP and RETURN calls.
# All functions should have a RuntimeResult().success(return-value) call as that is how ezr checks for error, or the lack thereof.
# To display errors, use the failure function in RuntimeResult and return it-
# eg: return RuntimeResult().failure(RuntimeError(self.start_pos, self.end_pos, ERROR_TAG, 'Error message', self.context))
# You can import any error class from ezr.py, such as:
#   UnknownCharError(start_pos, end_pos, details) -> Raised when any undefined characters are found
#   InvalidSyntaxError(start_pos, end_pos, details) -> Raised when the expected syntax is not found
#   RuntimeError(start_pos, end_pos, error_type, details, context) -> Any errors caused while running the code
# Always return / inherit from the RuntimeError class. The TRY statement is coded to only handle RuntimeErrors-
# as InvalidSyntax and UnknownChar errors MUST NOT occur in the Interpreter.
# 
# Error tags are str values used to catch errors in the TRY statement.
# An error tag can be as simple as this: EXAMPLE_ERRORTAG = 'EXAMPLE-ERRORTAG'
# Any errors thrown with this tag will be caught by TRY statements using the 'EXAMPLE-ERRORTAG' tag.
# ezr.py has some builtin error tags too- they can be imported into any project:
#   RTE_DEFAULT        = 'RUNTIME'
#   RTE_CUSTOM         = 'CUSTOM'
#   RTE_DICTKEY        = 'DICTIONARY-KEY'
#   RTE_ILLEGALOP      = 'ILLEGAL-OPERATION'
#   RTE_UNDEFINEDVAR   = 'UNDEFINED-VAR'
#   RTE_IDXOUTOFRANGE  = 'INDEX-OUT-OF-RANGE'
#   RTE_TOOMANYARGS    = 'TOO-MANY-ARGS'
#   RTE_TOOFEWARGS     = 'TOO-FEW-ARGS'
#   RTE_INCORRECTTYPE  = 'INCORRECT-TYPE'
#   RTE_MATH		   = 'MATH'
#   RTE_IO	   		   = 'IO'
# More details about these error tags are available in the ezr documentation.
#
# ezr library folder
# ------------------
# When making a library for ezr, it should be put in the 'Libraries' folder in ezrShells' installed directory.
# There, you'll find 'base_libObject.py' under the 'base' folder. This helps retrieve variables, call functions
# and handle ObjectCallNodes. Use base_libObject as the parent for the main lib_object class.

# Create main object
# The name HAS to be 'lib_Object', otherwise ezr will show an error
class lib_Object(base_libObject):
    # Initialization
    def __init__(self, internal_context=None):
        # Replace 'lib_template' with your librarys' name
        super().__init__('lib_template', internal_context)

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

        if not isinstance(val_a, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument has to be a [NUMBER]', context))
        if not isinstance(val_b, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument has to be a [NUMBER]', context))

        return res.success(Number(val_a.value + val_b.value))
    function_test_add.arg_names = ['val_a', 'val_b']