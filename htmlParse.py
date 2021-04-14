import copy

def readHTML(path):
    with open(path, "r") as readfile:
        r = readfile.read().split("\n")
        return r

def getLines(data, tag):
    lines = []
    count = -1
    for line in data:
        count += 1
        if tag in line:
            lines.append(count)
    return lines

def getBetweenTags(data, line, tag):
    tag_length = len(tag)+2
    inner = data[line][data[line].find("<"+tag+">")+tag_length:data[line].find("</"+tag+">")]
    return inner

def changeBetweenTags(data, line, tag, new_text):
    tag_length = len(tag)+2
    s_index = data[line].find("<"+tag+">")+tag_length
    e_index = data[line].find("</"+tag+">")
    new_line = data[line][:s_index] + new_text + "</"+tag+">"
    data[line] = new_line
    return data

def getTable(data, table_id):
    start = getLines(data, "table")
    count = -1
    for l in start:
        count +=1
        if table_id in data[l]:
            start_line = l
            end_line = start[count+1]
            
    line_count = start_line
    table_data = []
    while line_count != end_line:
        line_count += 1
        table_data.append(data[line_count])

    rows = getLines(table_data, "tr")
    n_rows = [[]]
    row_number = 0
    for x in rows:
        if rows.index(x) % 2 == 0:
            n_rows[0].append(x+start_line+2)
    row_number = len(n_rows)
    cells = getLines(table_data, "td")

    n_columns = len(cells) - row_number
    for y in range(n_columns-2):
        n_rows.append([])

    active_column = -1
    active_row = 0
    for g in cells:
        if len(n_rows[active_row]) == n_columns-1:
            active_row +=1
        else:
            active_column+=1
            n_rows[active_row].append(g+start_line+active_row+active_column)
            
    return [start_line, end_line, n_rows]

class tableObject():
    def __init__(self, table, data):
        self.start = table[0]
        self.text = ""
        self.end = table[1]
        self.cells = copy.deepcopy(table[2])
        self.data = copy.deepcopy(table[2])
        
        for x in range(len(self.data)):
            for y in range(len(self.data[x])):
                self.data[x][y] = data[self.data[x][y]]

        for x in range(len(self.data)):
            for y in range(len(self.data[x])):
                self.text = self.text + self.data[x][y]+"\n"

    def set(self, row, column, value):
        self.value = value
        self.s_index = self.data[column][row].find("<td>")+4
        self.e_index = self.data[column][row].find("</td>")
        self.new_line = self.data[column][row][:self.s_index] + self.value + "</td>"
        self.data[column][row] = self.new_line
        self.text = ""
        for x in range(len(self.data)):
            for y in range(len(self.data[x])):
                self.text = self.text + self.data[x][y]+"\n"

    def get(self, row, column):
        return self.data[column][row][self.data[column][row].find("<td>")+4:self.data[column][row].find("</td>")]

    def getT(self,row,column,t):
        if t.startswith('i'):
            return int(self.data[column][row][self.data[column][row].find("<td>")+4:self.data[column][row].find("</td>")])
        elif t.startswith('f'):
            return float(self.data[column][row][self.data[column][row].find("<td>")+4:self.data[column][row].find("</td>")])
        elif t.startswith('b'):
            return bool(self.data[column][row][self.data[column][row].find("<td>")+4:self.data[column][row].find("</td>")])




def writeHTML(data, path):
    html = ""
    for k in data:
        html += k
        html += "\n"
    with open(path, "w") as writefile:
        writefile.write(html)
        
be_read = readHTML("/Users/frozendessertsupplies/Desktop/edit_HTML_table_from_Python/pyWebSheets/index.html")
