# Built-in MATH library (for ezr V1.22.0.0)

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

## FLOOR(value: INT|FLOAT)
**Returns the floor of 'value', the largest integer less than or equal to 'value'**

## EXP(value: INT|FLOAT)
**Returns E raised to the power 'value', where E = 2.718281**

## LOG(value: INT|FLOAT, base: INT|FLOAT)
**Returns the logarithm of 'value' to the given base 'base'**

## POW(value_a: INT|FLOAT, value_b: INT|FLOAT)
**Returns 'value_a' raised to the power 'value_b'**

## SQRT(value: INT|FLOAT)
**Returns the square root of 'value'**

## SIN(value: INT|FLOAT)
**Returns the sine of 'value' radians**

## COS(value: INT|FLOAT)
**Returns the cosine of 'value' radians**

## TAN(value: INT|FLOAT)
**Returns the tangent of 'value' radians**

## DEGREES(value: INT|FLOAT)
**Convert angle 'value' from radians to degrees and returns it**

## RADIANS(value: INT|FLOAT)
**Convert angle 'value' from degrees to radians and returns it**

## IS_INF(value: INT|FLOAT)
**Returns TRUE if 'value' is a positive or negative infinity, and FALSE otherwise**

## IS_NAN(value: INT|FLOAT)
**Returns TRUE if 'value' is a NAN (not a number), and FALSE otherwise**

**Function examples are TODO**