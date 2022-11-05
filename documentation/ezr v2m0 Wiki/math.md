# Built-in math library (for v2m0)

## pi: number
**The mathematical constant π = 3.141592, to available precision**
```
include 'math.py'

show(math.pi)
```

## tau: number
**The mathematical constant τ = 6.283185, to available precision**
```
include 'math.py'

show(math.tau)
```

## e: number
**The mathematical constant e = 2.718281, to available precision**
```
include 'math.py'

show(math.e)
```

## inf: number
**A floating-point positive infinity**
```
include 'math.py'

show(math.inf)
```

## nan: number
**A floating-point 'not a number' (NaN) value**
```
include 'math.py'

show(math.nan)
```

## ceil(value: number)
**Returns the ceiling of 'value', the smallest 'integer' number greater than or equal to 'value'**
```
include 'math.py'

show(math.ceil(1.25))
show(math.ceil(1.5))
show(math.ceil(1.75))
```

## floor(value: number)
**Returns the floor of 'value', the largest 'integer' number less than or equal to 'value'**
```
include 'math.py'

show(math.floor(1.25))
show(math.floor(1.5))
show(math.floor(1.75))
```

## exp(value: number)
**Returns e raised to the power 'value', where e = 2.718281**
```
include 'math.py'

show(math.exp(5))
```

## log(value: number, base: number)
**Returns the logarithm of 'value' to the given base 'base'**
```
include 'math.py'

show(math.log(2, 10))
```

## pow(value_a: number, value_b: number)
**Returns 'value_a' raised to the power 'value_b'**
```
include 'math.py'

show(math.pow(3, 3))
```

## sqrt(value: number)
**Returns the square root of 'value'**
```
include 'math.py'

show(math.sqrt(25))
```

## sin(value: number)
**Returns the sine of 'value' radians**
```
include 'math.py'

show(math.sin(math.radians(45)))
```

## cos(value: number)
**Returns the cosine of 'value' radians**
```
include 'math.py'

show(math.cos(math.radians(45)))
```

## tan(value: number)
**Returns the tangent of 'value' radians**
```
include 'math.py'

show(math.tan(math.radians(45)))
```

## degrees(value: number)
**Convert angle 'value' from radians to degrees and returns it**
```
include 'math.py'

show(math.degrees(1.57079633))
```

## radians(value: number)
**Convert angle 'value' from degrees to radians and returns it**
```
include 'math.py'

show(math.radians(90))
```
## isInf(value: number)
**Returns true if 'value' is a positive or negative infinity, and false otherwise**
```
include 'math.py'

show(math.isInf(math.inf))
show(math.isInf(1))
```

## isNan(value: number)
**Returns true if 'value' is a NaN (not a number), and false otherwise**
```
include 'math.py'

show(math.isNan(math.nan))
show(math.isNan(1))
```