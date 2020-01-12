# py-rename
Rename is a Python program for batch renaming files using patterns.

## Usage

### How it works
Rename works by allowing users to identify patterns that occur within items they wish to rename. They can then reuse any of these patterns in the new item name. Patterns in the original names are identified using regex groups.  Any items with names which do not match the initial pattern, are ignored. 

(For help with regex visit - https://www.debuggex.com/cheatsheet/regex/python)



### Program help

The output of ```rename.py -h``` and ```rename.py --help``` is as follows -

```
usage: rename.py [-h] (-f | -d) [-s] directory initial desired

Bulk rename files using regex

positional arguments:
  directory             the directory containing items to be renamed
  initial               the initial regex pattern of all items to be renamed
  desired               the desired pattern of all items to be renamed

optional arguments:
  -h, --help            show this help message and exit
  -f, --files           rename files
  -d, --directories     rename directories
  -s, --subdirectories  rename items inside of subdirectories

Report any issues at - https://github.com/alwian/py-rename/issues
```



### Example

```
exampleDirectory-
	File1.mp4
	File2.mp4
	exampleSubdirectory -
		File3.mp4
		File4.mp4
```

Given the above file tree, say we wish to move the number from the end of each filename to the beginning. To do this we would execute the following command -

```
rename.py -s exampleDirectory File(?P<number>[0-9]+) [number]File
```

After executing the command the command, the tree would look as follows -

```
exampleDirectory-
	1File.mp4
	2File.mp4
	exampleSubdirectory -
		3File.mp4
		4File.mp4
```

As you can see, files in the subdirectory have also been renamed as we used the ```-s``` flag.  For other available flags, see ***Program help*** above.