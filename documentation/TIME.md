# Built-in TIME library (for ezr V1.24.0.1.0)
## TIMESTRUCT Object
**Object returned by GMTIME() and LOCALTIME() and accepted by READABLE_TIME() and READABLE_DATE(); Contains data for time**
> Can also be created by user with the TIMESTRUCT() function
```
INCLUDE 'TIME.py'

ITEM ts: TIME.LOCALTIME(TIME.TIME())

SHOW('YEAR: ' + CONVERT(ts.YEAR, 'STRING'))
SHOW('MONTH: ' + CONVERT(ts.MONTH, 'STRING'))
SHOW('DAY OF MONTH: ' + CONVERT(ts.MONTH_DAY, 'STRING'))
SHOW('DAY OF WEEK: ' + CONVERT(ts.WEEK_DAY, 'STRING'))
SHOW('DAY OF YEAR: ' + CONVERT(ts.YEAR_DAY, 'STRING'))

SHOW('HOUR: ' + CONVERT(ts.HOUR, 'STRING'))
SHOW('MINUTE: ' + CONVERT(ts.MINUTE, 'STRING'))
SHOW('SECOND: ' + CONVERT(ts.SECOND, 'STRING'))

SHOW('TIMEZONE: ' + CONVERT(ts.ZONE, 'STRING'))
SHOW('GMT-OFFSET (IN SECONDS): ' + CONVERT(ts.OFFSET, 'STRING'))

SHOW('HAS DAYLIGHT SAVINGS TIME? : ' + CONVERT(ts.HAS_DST, 'STRING'))

@ TIMESTRUCT(year, month, month_day, week_day, year_day, hour, minute, second, zone, offset, has_dst)
@ NOTE: has_dst must be TRUE, FALSE or STRING literal 'UNKNOWN'

ITEM custom_ts: TIME.TIMESTRUCT(1970, 1, 1, 1, 1, 10, 30, 40, 'GMT', 0, FALSE)
SHOW(TIME.READABLE_TIME(custom_ts))
SHOW(TIME.READABLE_DATE(custom_ts))
```

## EPOCH: TIMESTRUCT
**TIMESTRUCT object of Epoch; Same as calling GMTIME(0)**
> The Epoch is the point where time starts, and is platform dependent
```
INCLUDE 'TIME.py'

SHOW(TIME.READABLE_TIME(TIME.EPOCH))
SHOW(TIME.READABLE_DATE(TIME.EPOCH))
```

## TIME() Function
**Returns current time since Epoch in seconds**
```
INCLUDE 'TIME.py'

SHOW(TIME.TIME())
```

## GMTIME(time: INT|FLOAT)
**Converts and returns TIMESTRUCT object of given time (in seconds since Epoch) 'time' in UTC|GMT**
```
INCLUDE 'TIME.py'

ITEM ts: TIME.GMTIME(TIME.TIME())
SHOW('GMTIME: ' + TIME.READABLE_TIME(ts))
```

## LOCALTIME(time: INT|FLOAT)
**Converts and returns TIMESTRUCT object of given time (in seconds since Epoch) 'time' in devices' local timezone**
```
INCLUDE 'TIME.py'

ITEM ts: TIME.LOCALTIME(TIME.TIME())
SHOW('LOCAL TIME: ' + TIME.READABLE_TIME(ts))
```

## READABLE_TIME(timestruct: TIMESTRUCT)
**Returns time (HOUR:MINUTE:SECOND) in 'timestruct' as a more readable STRING form**
```
INCLUDE 'TIME.py'

ITEM gmts: TIME.GMTIME(TIME.TIME())
SHOW('GMTIME: ' + TIME.READABLE_TIME(gmts))

ITEM lts: TIME.LOCALTIME(TIME.TIME())
SHOW('LOCAL TIME: ' + TIME.READABLE_TIME(lts))
```

## READABLE_DATE(timestruct: TIMESTRUCT)
**Returns date (MONTH-DAY:MONTH:YEAR) in 'timestruct' as a more readable STRING form**
```
INCLUDE 'TIME.py'

ITEM lts: TIME.LOCALTIME(TIME.TIME())
SHOW('LOCAL DATE: ' + TIME.READABLE_DATE(lts))
```

## SLEEP(time: INT|FLOAT)
**Pause execution of program for given seconds 'time'**
```
INCLUDE 'TIME.py'

SHOW('SLEEP TEST')
TIME.SLEEP(3)
SHOW('SLEEP TEST OVER')
```