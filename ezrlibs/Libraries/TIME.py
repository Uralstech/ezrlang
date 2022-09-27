from ezr import RuntimeResult, RuntimeError, Nothing, Number, Bool, String, RTE_INCORRECTTYPE
# from Libraries.base.base_libObject import base_libObject
from ezrlibs.Libraries.base.base_libObject import base_libObject # Debug
from time import gmtime, localtime, time, sleep

class timestruct_Object(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('TIMESTRUCT', internal_context)

    def update(self, struct):
        self.set_variable('YEAR', Number(struct.tm_year))
        self.set_variable('MONTH', Number(struct.tm_mon))
        self.set_variable('MONTH_DAY', Number(struct.tm_mday))
        self.set_variable('WEEK_DAY', Number(struct.tm_wday+1))
        self.set_variable('YEAR_DAY', Number(struct.tm_yday))
        self.set_variable('HOUR', Number(struct.tm_hour))
        self.set_variable('MINUTE', Number(struct.tm_min))
        self.set_variable('SECOND', Number(struct.tm_sec))

        self.set_variable('ZONE', String(struct.tm_zone))
        self.set_variable('OFFSET', Number(struct.tm_gmtoff))

        has_dst = struct.tm_isdst
        if has_dst == 1: self.set_variable('HAS_DST', Bool(True))
        elif has_dst == 0: self.set_variable('HAS_DST', Bool(False))
        elif has_dst == -1: self.set_variable('HAS_DST', String('UNKNOWN'))

        return self.copy()

    def update_with_values(self, year, month, month_day, week_day, year_day, hour, minute, second, zone, offset, has_dst):
        self.set_variable('YEAR', year)
        self.set_variable('MONTH', month)
        self.set_variable('MONTH_DAY', month_day)
        self.set_variable('WEEK_DAY', week_day)
        self.set_variable('YEAR_DAY', year_day)
        self.set_variable('HOUR', hour)
        self.set_variable('MINUTE', minute)
        self.set_variable('SECOND', second)

        self.set_variable('ZONE', zone)
        self.set_variable('OFFSET', offset)

        self.set_variable('HAS_DST', has_dst)

        return self.copy()
    
    def copy(self):
        copy = timestruct_Object(self.internal_context)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)

        return copy

class lib_Object(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('TIME', internal_context)

    def copy(self):
        copy = lib_Object(self.internal_context)
        copy.set_pos(self.start_pos, self.end_pos)
        copy.set_context(self.context)

        return copy

    def function_TIME(self, node, context):
        return RuntimeResult().success(Number(time()))
    function_TIME.arg_names = []

    def function_TIMESTRUCT(self, node, context):
        res = RuntimeResult()

        year = context.symbol_table.get('year')
        if not isinstance(year, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        month = context.symbol_table.get('month')
        if not isinstance(month, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be an [INT] or [FLOAT]', context))
        if month.value < 1 or month.value > 12: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Second argument must be in range 1-12', context))

        month_day = context.symbol_table.get('month_day')
        if not isinstance(month_day, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Third argument must be an [INT] or [FLOAT]', context))
        if month_day.value < 1 or month_day.value > 31: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Third argument must be in range 1-31', context))
        
        week_day = context.symbol_table.get('week_day')
        if not isinstance(week_day, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Fourth argument must be an [INT] or [FLOAT]', context))
        if week_day.value < 1 or week_day.value > 7: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Fourth argument must be in range 1-7', context))

        year_day = context.symbol_table.get('year_day')
        if not isinstance(year_day, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Fifth argument must be an [INT] or [FLOAT]', context))
        if year_day.value < 1 or year_day.value > 366: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Fifth argument must be in range 1-366', context))

        hour = context.symbol_table.get('hour')
        if not isinstance(hour, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Sixth argument must be an [INT] or [FLOAT]', context))
        if hour.value < 0 or hour.value > 23: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Sixth argument must be in range 0-23', context))

        minute = context.symbol_table.get('minute')
        if not isinstance(minute, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Seventh argument must be an [INT] or [FLOAT]', context))
        if minute.value < 0 or minute.value > 59: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Seventh argument must be in 0-59', context))
        
        second = context.symbol_table.get('second')
        if not isinstance(second, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Eighth argument must be an [INT] or [FLOAT]', context))
        if second.value < 0 or second.value > 61: return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Eighth argument must be in range 0-61', context))
        
        zone = context.symbol_table.get('zone')
        if not isinstance(zone, String): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Ninth argument must be a [STRING]', context))
        
        offset = context.symbol_table.get('offset')
        if not isinstance(offset, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Tenth argument must be an [INT] or [FLOAT]', context))
        
        has_dst = context.symbol_table.get('has_dst')
        if not isinstance(has_dst, Bool) and (not isinstance(has_dst, String) or has_dst.value != 'UNKNOWN'): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'Eleventh argument must be a [BOOL] or [STRING] literal \'UNKNOWN\'', context))
    
        tso = res.register(timestruct_Object().set_context(context).set_pos(node.start_pos, node.end_pos).execute())
        if res.should_return(): return res

        return res.success(tso.update_with_values(year, month, month_day, week_day, year_day, hour, minute, second, zone, offset, has_dst))
    function_TIMESTRUCT.arg_names = ['year', 'month', 'month_day', 'week_day', 'year_day', 'hour', 'minute', 'second', 'zone', 'offset', 'has_dst']

    def function_GMTIME(self, node, context):
        res = RuntimeResult()

        time = context.symbol_table.get('time')
        if not isinstance(time, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        tso = res.register(timestruct_Object().set_context(context).set_pos(node.start_pos, node.end_pos).execute())
        if res.should_return(): return res

        return res.success(tso.update(gmtime(time.value)))
    function_GMTIME.arg_names = ['time']

    def function_LOCALTIME(self, node, context):
        res = RuntimeResult()

        time = context.symbol_table.get('time')
        if not isinstance(time, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        tso = res.register(timestruct_Object().set_context(context).set_pos(node.start_pos, node.end_pos).execute())
        if res.should_return(): return res

        return res.success(tso.update(localtime(time.value)))
    function_LOCALTIME.arg_names = ['time']

    def function_SLEEP(self, node, context):
        res = RuntimeResult()

        time = context.symbol_table.get('time')
        if not isinstance(time, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        sleep(time.value)
        return res.success(Nothing())
    function_SLEEP.arg_names = ['time']

    def function_READABLE_TIME(self, node, context):
        res = RuntimeResult()

        time = context.symbol_table.get('timestruct')
        if not isinstance(time, timestruct_Object): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [TIMESTRUCT]', context))

        hour = time.get_variable('HOUR').value
        minute = time.get_variable('MINUTE').value
        second = time.get_variable('SECOND').value
        return res.success(String(f'{hour}:{minute}:{second}'))
    function_READABLE_TIME.arg_names = ['timestruct']

    def function_READABLE_DATE(self, node, context):
        res = RuntimeResult()

        time = context.symbol_table.get('timestruct')
        if not isinstance(time, timestruct_Object): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be a [TIMESTRUCT]', context))

        month_day = time.get_variable('MONTH_DAY').value
        month = time.get_variable('MONTH').value
        year = time.get_variable('YEAR').value
        return res.success(String(f'{month_day}:{month}:{year}'))
    function_READABLE_DATE.arg_names = ['timestruct']