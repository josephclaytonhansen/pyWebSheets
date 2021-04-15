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
`t.cells: [[10, 15], [11, 16]]`.
Notice that cells and data are stored in a nested array- columns and rows. `t.cells[0][1]` will give you the first column and the second row. **This is not the best way to access this data: it's both confusing in order and choked up with excess data. Use `tableObject.get(row,column)`.**
* data (the actual content of the line):
`t.data: [['                <td>one</td>', '                <td>three</td>'], ['                <td>two</td>', '                <td>four</td>']]'`
* start position (first line) of the table:
`t.start: 7`
* end position of the table:
`t.end: 19`
* and the pure HTML text, for adding into the main HTML: `t.text: '                <td>one</td>\n                <td>three</td>\n                <td>two</td>\n                <td>four</td>\n'`

## Getting a cell value
Use `tableObject.get(row,column)` to get the value of a cell (stripped of whitespace and tags.) For example, `t.get(0,1)` would give you `"two"` with this table. **Because rows and columns work the way they would in a spreadsheet with this function, it should always be used instead of accessing data from `tableObject.cells`.** This function can get a cell value as *type* by passing a third parameter. type is 'i' for integer, 'f' for float, or 'b' for bool. String is the default, `get` will always return a string if a type is not set. 

## Setting a cell value
This class  contains a `set` function, which allows the value of a row/column cell to be changed. This updates `t.text` as well, allowing for easy table editing that copies over into the HTML document. Use as `tableObject.set(row,column,value)`. This works very well in combination with `tableObject.get()`:
```python
>>> t.get(0,1)
'two'
>>> t.set(0,1,"new")
>>> t.get(0,1)
'new'
```
## Updating HTML with changes
Once changes have been made to the table, use `tableObject.putBack(path)` to re-write the HTML file with the updates. `writeHTML` is for changes made by `changeBetweenTags`- **don't use `writeHTML` to put a table back (it won't work.)** Generally speaking, you'll use `putBack()` for all your HTML updating needs.
## Complete example: changing a cell value
```python
t=tableObject(getTable(r, "numbers"), r) #where r is readHTML(path)
t.set(0,0,"new")
t.putBack(path)
```

## Getting and changing between tags
`getLines` takes data from `readHTML` and finds the lines containing any given HTML tag such as `<p>` or `<input>`, returning them as a list. This list can be used for `getBetweenTags`, which takes one line and isolates the content between given tags. `changeBetweenTags` takes this a step further by allowing the content between tags on the specified line to be replaced. `writeHTML` updates the HTML document with any changes made this way. 
## TODO
### tableObject:
- [ ] addRow()
- [ ] addColumn()
- [ ] clear(row, column)
