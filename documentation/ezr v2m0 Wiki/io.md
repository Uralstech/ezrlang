# Built-in io library (for v2m0)

## read(filepath: string, mode: string)
**Reads file at 'filepath' and returns data in mode 'mode'**
```
include 'io.py'

@ Returns all data in file as string (\n = newline, \t = tab-space)
item f_read: io.read('path/to/file', 'READ')
show(f_read)

@ Returns first line of file as string
item f_read_line: io.read('path/to/file', 'READ_LINE')
show(f_read_line)

@ Returns all lines of file as list
item f_read_lines: io.read('path/to/file', 'READ_LINES')
show(f_read_lines)
```

## write(filepath: string, mode: string, data: any type)
**Writes data 'data' to file at 'filepath' in mode 'mode'**
```
include 'io.py'

@ Appends data to file
io.write('path/to/file', 'EXTEND', 'test\ndata')

@ Overwrites all existing data in file
io.write('path/to/file', 'OVERWRITE', 'test\ndata')
```

## delete(filepath: string)
**Deletes file at 'filepath'**
```
include 'io.py'

io.delete('path/to/file')
```

## makeDir(dirpath: string)
**Creates directory at 'dirpath'**
```
include 'io.py'

io.makeDir('path/to/dir/dir-name')
```

## removeDir(dirpath: string)
**Deletes directory at 'dirpath'**
```
include 'io.py'

io.removeDir('path/to/dir/dir-name')
```