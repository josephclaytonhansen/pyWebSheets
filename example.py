from htmlParse import *
path = "index.html"
r = readHTML(path)
t=tableObject(getTable(r, "numbers"), r)
print("Use object 't' to access the main table on the index page")
