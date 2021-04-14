# pyWebSheets
 Edit HTML tables from Python- a tool to help convert spreadsheets to HTML with back-end functionality. So far there's not much going on, I'll add to this readme as I go. This is for work, so it takes lower priority than my other projects. 
 
 ## Basic usage- pulling a table from HTML:
 Pretty much everything happens with a `tableObject`. This object relies on the `getTable` function. The usage for defining a `tableObject` is:
```python
t= tableObject(getTable(readHTML(path), table_id), readHTML(path))
```
Given an example table starting at line 7, with the first cell at line 10:

one | two
-----|----
three | four

`tableObject` contains:
* cells (line references to the HTML document), for example:
`t.cells: [[10, 15], [11, 16]]`
notice that cells and data are stored in a nested array- rows and columns. `t.cells[0][1]` will give you the first row and the second column. 
* data (the actual content of the line):
`t.data: [['                <td>one</td>', '                <td>three</td>'], ['                <td>two</td>', '                <td>four</td>']]'`
* start position (first line) of the table:
`t.start: 7`
* end position of the table:
`t.end: 19`
* and the pure HTML text, for adding into the main HTML: `t.text: '                <td>one</td>\n                <td>three</td>\n                <td>two</td>\n                <td>four</td>\n'`

## Getting a cell value
Use `tableObject.get(row,column)` to get the value of a cell (stripped of whitespace and tags.) For example, `t.get(0,0)` would give you `"one"` with this table.

## Setting a cell value
This class  contains a `set` function, which allows the value of a row/column cell to be changed. This updates `t.text` as well, allowing for easy table editing that copies over into the HTML document. Use as `tableObject.set(row,column,value)`.
```python
>>> t.set(0,1,"new_value")
>>> t.text
'                <td>one</td>\n                <td>new_value</td>\n                <td>two</td>\n                <td>four</td>\n'
>>> t.data
[['                <td>one</td>', '                <td>new_value</td>'], ['                <td>two</td>', '                <td>four</td>']]
```
## Getting and changing between tags
`getLines` takes data from `readHTML` and finds the lines containing any given HTML tag such as `<p>` or `<input>`, returning them as a list. This list can be used for `getBetweenTags`, which takes one line and isolates the content between given tags. `changeBetweenTags` takes this a step further by allowing the content between tags on the specified line to be replaced. `writeHTML` updates the HTML document with any changes made this way. 
