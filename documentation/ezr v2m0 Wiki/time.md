# Built-in time library (for v2m0)

## timeStruct Object
**Object returned by utcTime() and localTime() and contains data for time.**
**Can also be created by user with the timeStruct() function**
```
include 'time.py'

item ts: time.localTime(time.time())

show('year: ' + convert(ts.year, 'String'))
show('month: ' + convert(ts.month, 'String'))
show('day of month: ' + convert(ts.monthDay, 'String'))
show('day of week: ' + convert(ts.weekDay, 'String'))
show('day of year: ' + convert(ts.yearDay, 'String'))

show('hour: ' + convert(ts.hour, 'String'))
show('minute: ' + convert(ts.minute, 'String'))
show('second: ' + convert(ts.second, 'String'))

show('timezone: ' + convert(ts.timeZone, 'String'))
show('UTC-offset (in secondS): ' + convert(ts.utcOffset, 'String'))

show('has daylight savings time? : ' + convert(ts.hasDST, 'String'))

@ timeStruct(year, month, month_day, week_day, year_day, hour, minute, second, zone, offset, has_dst)
@ NOTE: has_dst must be true, false or string literal 'UNKNOWN'

item custom_ts: time.timeStruct(1970, 1, 1, 1, 1, 10, 30, 40, 'UTC', 0, false)
show(custom_ts.readableTime())
show(custom_ts.readableDate())
```

### timeStruct.readableTime()
**Returns time (hour:minute:second) as a more readable string form**
```
include 'time.py'

item gmts: time.utcTime(time.time())
show('utcTime: ' + gmts.readableTime())

item lts: time.localTime(time.time())
show('local time: ' + lts.readableTime())
```

### timeStruct.readableDate()
**Returns date (month-day:month:year) as a more readable string form**
```
include 'time.py'

item lts: time.localTime(time.time())
show('local date: ' + lts.readableDate())
```

## epoch: timeStruct
**timeStruct object of Epoch; Same as calling utcTime(0)**
**(Epoch is the point where time starts, and is platform dependent)**
```
include 'time.py'

show(time.epoch.readableTime())
show(time.epoch.readableDate())
```

## time() Function
**Returns current time since Epoch in seconds**
```
include 'time.py'

show(time.time())
```

## utcTime(time: number)
**Converts and returns timeStruct object of given time (in seconds since Epoch) 'time' in UTC**
```
include 'time.py'

item ts: time.utcTime(time.time())
show('utcTime: ' + ts.readableTime())
```

## localTime(time: number)
**Converts and returns timeStruct object of given time (in seconds since Epoch) 'time' in devices' local timezone**
```
include 'time.py'

item ts: time.localTime(time.time())
show('local time: ' + ts.readableTime())
```

## sleep(time: number)
**Pause execution of program for given seconds 'time'**
```
include 'time.py'

show('sleep test start')
time.sleep(3)
show('sleep test over')
```