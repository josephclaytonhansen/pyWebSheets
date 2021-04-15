import copy

def readHTML(path):
    with open(path, "r") as readfile:
        r=readfile.read().strip()
        r = r.split("\n")
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

    row_number = len(n_rows[0])
    cells = getLines(table_data, "td")
    for x in range(len(cells)):
        cells[x] += 1

    n_columns = int(len(cells)+1 / row_number)
    n_columns /= row_number
    n_columns = int(n_columns)
    
    for y in range(n_columns):
        n_rows.append([])

    active_row = -1
    tmp_rows = []
    for y in range(n_columns):
        tmp_rows.append([])
        
    for g in cells:
        active_row+=1
        if active_row == int(len(cells)/n_columns):
            active_row= 0
        tmp_rows[active_row].append(g+start_line)
        distance_between = int(n_columns + 2)
    new_tm = []
    for k in range(n_columns):
        new_tm.append([])
        for x in range(n_columns - 1):
            new_tm[k].append(cells[k]+start_line+(distance_between*x))
        
    n_rows = new_tm
        
            
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
                
    def columnToLetter(self, column):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                   "K", "L", "M", "N", "O", "P", "Q", "R", "T", "U",
                   "V", "W", "X", "Y", "Z", "AA", "BB", "CC", "DD",
                   "EE", "FF", "GG", "HH", "II", "JJ", "KK", "LL",
                   "MM", "NN", "OO", "PP", "QQ", "RR", "SS", "TT",
                   "UU", "VV", "WW", "XX", "YY", "ZZ"]
        return letters[column]
    def letterToColumn(self, letter):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                   "K", "L", "M", "N", "O", "P", "Q", "R", "T", "U",
                   "V", "W", "X", "Y", "Z", "AA", "BB", "CC", "DD",
                   "EE", "FF", "GG", "HH", "II", "JJ", "KK", "LL",
                   "MM", "NN", "OO", "PP", "QQ", "RR", "SS", "TT",
                   "UU", "VV", "WW", "XX", "YY", "ZZ"]
        if letter[0].upper() in letters:
            return letters.index(letter[0].upper())
        elif letter[0:1].upper() in letters:
            return letters.index(letter[0:1].upper())


    def set(self, notation = None, value="", row=0, column=0):
        if notation != None:
            column = self.letterToColumn(notation)
            if len(notation) == 2:
                row = int(notation[1])-1
            elif len(notation) == 3:
                row = int(notation[2])-1
                
        self.value = str(value)
        self.s_index = self.data[column][row].find("<td>")+4
        self.e_index = self.data[column][row].find("</td>")
        self.new_line = self.data[column][row][:self.s_index] + self.value + "</td>"
        self.data[column][row] = self.new_line
        self.text = ""
        for x in range(len(self.data)):
            for y in range(len(self.data[x])):
                self.text = self.text + self.data[x][y]+"\n"

    def get(self, notation = None, row=0, column=0, t='s'):
        if notation != None:
            column = self.letterToColumn(notation)
            if len(notation) == 2:
                row = int(notation[1])-1
            elif len(notation) == 3:
                row = int(notation[2])-1
                
        if t.startswith('i'):
            return int(self.data[column][row][self.data[column][row].find("<td>")+4:self.data[column][row].find("</td>")])
        elif t.startswith('f'):
            return float(self.data[column][row][self.data[column][row].find("<td>")+4:self.data[column][row].find("</td>")])
        elif t.startswith('b'):
            return bool(self.data[column][row][self.data[column][row].find("<td>")+4:self.data[column][row].find("</td>")])
        else:
            return self.data[column][row][self.data[column][row].find("<td>")+4:self.data[column][row].find("</td>")]

    def putBack(self,path):
        data=readHTML(path)
        count=-1
        lines = []
        table_lines = []
        for line in data:
            count+=1
            lines.append(count)
        for x in self.cells:
            for y in x:
                table_lines.append(y)
        html = ""
        tl_count = 0
        tl_r_count = 0
        t_columns = len(self.data)
        t_rows = len(table_lines) / t_columns
        for x in lines:
            html +="\n"
            if x  in table_lines:
                html += self.data[tl_count][tl_r_count]
                tl_count += 1
                if tl_count == t_columns:
                    tl_count = 0
                    tl_r_count += 1
            else:
                html += data[x]
        with open(path, "w") as writefile:
            writefile.write(html)

    def addRow(self):
        pass
        #add <td></td> to the END of each <tr> segment, and get the line number Y > X
        #for each <tr> segment, increase self.end by 1
        #for each sub-list in self.cells, append the <td> line number to the sub-list    
            
    def getRange(self, r):
        r = r.split(":")
        cells = []
        start_column = self.letterToColumn(r[0])
        end_column = self.letterToColumn(r[1])
        if len(r[0]) == 2:
            start_row = int(r[0][1])-1
        elif len(r[0]) == 3:
            start_row = int(r[0][2])-1
        if len(r[1]) == 2:
            end_row = int(r[1][1])-1
        elif len(r[1]) == 3:
            end_row = int(r[1][2])-1

        for x in range(start_row, end_row+1):
            for y in range(start_column, end_column+1):
                c = self.columnToLetter(y)
                cells.append(c+str(x+1))
        return cells

    def sum(self, r):
        s = self.getRange(r)
        st = 0
        for g in range(len(s)):
            st += self.get(s[g],t='i')
        return st

    def average(self, r):
        s = self.sum(r)
        sl = len(self.getRange(r))
        s = s / sl
        return s

    def count(self, r):
        s = len(self.getRange(r))
        return s

    def high(self, r):
        s = self.getRange(r)
        h = 0
        for g in range(len(s)):
            n = int(self.get(s[g],t='i'))
            if  n > h:
                h = n
        return h

    def low(self, r):
        s = self.getRange(r)
        h = 1000000000
        for g in range(len(s)):
            n = int(self.get(s[g],t='i'))
            if  n < h:
                h = n
        return h
           
def writeHTML(data, path):
    html = ""
    for k in data:
        html += k
        html += "\n"
    with open(path, "w") as writefile:
        writefile.write(html)

