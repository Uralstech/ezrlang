from ezr import RuntimeResult, RuntimeError, Nothing, Number, Bool, String, RTE_INCORRECTTYPE
from time import gmtime, localtime, time, sleep

from Libraries.base.base_libObject import base_libObject

class time_timeStruct(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('timeStruct', internal_context)

    @classmethod
    def new_object(cls, context, start_pos, end_pos):
        return time_timeStruct().set_context(context).set_pos(start_pos, end_pos).execute()
    
    def function_readableTime(self, node, context):
        res = RuntimeResult()
        hour = self.get_variable('hour').value
        minute = self.get_variable('minute').value
        second = self.get_variable('second').value
        return res.success(String(f'{hour}:{minute}:{second}'))
    function_readableTime.arg_names = []

    def function_readableDate(self, node, context):
        res = RuntimeResult()
        month_day = self.get_variable('month_day').value
        month = self.get_variable('month').value
        year = self.get_variable('year').value
        return res.success(String(f'{month_day}:{month}:{year}'))
    function_readableDate.arg_names = []

    def update(self, struct):
        self.set_variable('year', Number(struct.tm_year))
        self.set_variable('month', Number(struct.tm_mon))
        self.set_variable('month_day', Number(struct.tm_mday))
        self.set_variable('week_day', Number(struct.tm_wday+1))
        self.set_variable('year_day', Number(struct.tm_yday))
        self.set_variable('hour', Number(struct.tm_hour))
        self.set_variable('minute', Number(struct.tm_min))
        self.set_variable('second', Number(struct.tm_sec))

        self.set_variable('timeZone', String(struct.tm_zone))
        self.set_variable('utcOffset', Number(struct.tm_gmtoff))

        has_dst = struct.tm_isdst
        if has_dst == 1: self.set_variable('hasDST', Bool(True))
        elif has_dst == 0: self.set_variable('hasDST', Bool(False))
        elif has_dst == -1: self.set_variable('hasDST', String('UNKNOWN'))

        return self.copy()

    def update_with_values(self, year, month, month_day, week_day, year_day, hour, minute, second, zone, offset, has_dst):
        self.set_variable('year', year)
        self.set_variable('month', month)
        self.set_variable('month_day', month_day)
        self.set_variable('week_day', week_day)
        self.set_variable('year_day', year_day)
        self.set_variable('hour', hour)
        self.set_variable('minute', minute)
        self.set_variable('second', second)

        self.set_variable('timeZone', zone)
        self.set_variable('utcOffset', offset)

        self.set_variable('hasDST', has_dst)

        return self.copy()


class lib_Object(base_libObject):
    def __init__(self, internal_context=None):
        super().__init__('time', internal_context)

    def initialize(self, context):
        res = RuntimeResult()

        tso = res.register(time_timeStruct.new_object(context, self.start_pos, self.end_pos))
        if res.should_return(): return res

        self.set_variable('epoch', tso.update(gmtime(0)))

        return res.success(Nothing())

    def function_time(self, node, context):
        return RuntimeResult().success(Number(time()))
    function_time.arg_names = []

    def function_timeStruct(self, node, context):
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
    
        tso = res.register(time_timeStruct.new_object(context, node.start_pos, node.end_pos))
        if res.should_return(): return res

        return res.success(tso.update_with_values(year, month, month_day, week_day, year_day, hour, minute, second, zone, offset, has_dst))
    function_timeStruct.arg_names = ['year', 'month', 'month_day', 'week_day', 'year_day', 'hour', 'minute', 'second', 'zone', 'offset', 'has_dst']

    def function_utcTime(self, node, context):
        res = RuntimeResult()

        time = context.symbol_table.get('time')
        if not isinstance(time, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        tso = res.register(time_timeStruct.new_object(context, node.start_pos, node.end_pos))
        if res.should_return(): return res

        return res.success(tso.update(gmtime(time.value)))
    function_utcTime.arg_names = ['time']

    def function_localTime(self, node, context):
        res = RuntimeResult()

        time = context.symbol_table.get('time')
        if not isinstance(time, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        tso = res.register(time_timeStruct.new_object(context, node.start_pos, node.end_pos))
        if res.should_return(): return res

        return res.success(tso.update(localtime(time.value)))
    function_localTime.arg_names = ['time']

    def function_sleep(self, node, context):
        res = RuntimeResult()

        time = context.symbol_table.get('time')
        if not isinstance(time, Number): return res.failure(RuntimeError(node.start_pos, node.end_pos, RTE_INCORRECTTYPE, 'First argument must be an [INT] or [FLOAT]', context))

        sleep(time.value)
        return res.success(Nothing())
    function_sleep.arg_names = ['time']