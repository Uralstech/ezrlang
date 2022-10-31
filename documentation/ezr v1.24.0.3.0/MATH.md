# Built-in MATH library (for ezr V1.24.0.3.0)

## PI: FLOAT
**The mathematical constant π = 3.141592, to available precision**
```
INCLUDE 'MATH.py'

SHOW(MATH.PI)
```

## TAU: FLOAT
**The mathematical constant τ = 6.283185, to available precision**
```
INCLUDE 'MATH.py'

SHOW(MATH.TAU)
```

## E: FLOAT
**The mathematical constant e = 2.718281, to available precision**
```
INCLUDE 'MATH.py'

SHOW(MATH.E)
```

## INF: FLOAT
**A floating-point positive infinity**
```
INCLUDE 'MATH.py'

SHOW(MATH.INF)
```

## NAN: FLOAT
**A floating-point 'not a number' (NaN) value**
```
INCLUDE 'MATH.py'

SHOW(MATH.NAN)
```

## CEIL(value: INT|FLOAT)
**Returns the ceiling of 'value', the smallest integer greater than or equal to 'value'**
```
INCLUDE 'MATH.py'

SHOW(MATH.CEIL(1.25))
SHOW(MATH.CEIL(1.5))
SHOW(MATH.CEIL(1.75))
```

## FLOOR(value: INT|FLOAT)
**Returns the floor of 'value', the largest integer less than or equal to 'value'**
```
INCLUDE 'MATH.py'

SHOW(MATH.FLOOR(1.25))
SHOW(MATH.FLOOR(1.5))
SHOW(MATH.FLOOR(1.75))
```

## EXP(value: INT|FLOAT)
**Returns E raised to the power 'value', where E = 2.718281**
```
INCLUDE 'MATH.py'

SHOW(MATH.EXP(5))
```

## LOG(value: INT|FLOAT, base: INT|FLOAT)
**Returns the logarithm of 'value' to the given base 'base'**
```
INCLUDE 'MATH.py'

SHOW(MATH.LOG(2, 10))
```

## POW(value_a: INT|FLOAT, value_b: INT|FLOAT)
**Returns 'value_a' raised to the power 'value_b'**
```
INCLUDE 'MATH.py'

SHOW(MATH.POW(3, 3))
```

## SQRT(value: INT|FLOAT)
**Returns the square root of 'value'**
```
INCLUDE 'MATH.py'

SHOW(MATH.SQRT(25))
```

## SIN(value: INT|FLOAT)
**Returns the sine of 'value' radians**
```
INCLUDE 'MATH.py'

SHOW(MATH.SIN(MATH.RADIANS(45)))
```

## COS(value: INT|FLOAT)
**Returns the cosine of 'value' radians**
```
INCLUDE 'MATH.py'

SHOW(MATH.COS(MATH.RADIANS(45)))
```

## TAN(value: INT|FLOAT)
**Returns the tangent of 'value' radians**
```
INCLUDE 'MATH.py'

SHOW(MATH.TAN(MATH.RADIANS(45)))
```

## DEGREES(value: INT|FLOAT)
**Convert angle 'value' from radians to degrees and returns it**
```
INCLUDE 'MATH.py'

SHOW(MATH.DEGREES(1.57079633))
```

## RADIANS(value: INT|FLOAT)
**Convert angle 'value' from degrees to radians and returns it**
```
INCLUDE 'MATH.py'

SHOW(MATH.RADIANS(90))
```
## IS_INF(value: INT|FLOAT)
**Returns TRUE if 'value' is a positive or negative infinity, and FALSE otherwise**
```
INCLUDE 'MATH.py'

SHOW(MATH.IS_INF(MATH.INF))
SHOW(MATH.IS_INF(1))
```

## IS_NAN(value: INT|FLOAT)
**Returns TRUE if 'value' is a NaN (not a number), and FALSE otherwise**
```
INCLUDE 'MATH.py'

SHOW(MATH.IS_NAN(MATH.NAN))
SHOW(MATH.IS_NAN(1))
```