from flask import Flask, request
import sqlite3
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        data = request.data.decode().rstrip(']').lstrip('[')
        data = data.split(', ')
        print(data)
        data = list(map(lambda x: x.rstrip('"').lstrip('"'), data))
        data1 = []
        for el in data:
            string = ''
            for symbol in el:
                if symbol != '\\':
                    string += symbol
            data1.append(string)
        data = data1.copy()
        print(data)
        table = data[1]
        param = data[0]
        where = data[2]
        if '=' in where:
            where += '"'
        qwe = f'select {param} from {table} where {where}'
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        ans = cur.execute(qwe).fetchall()
        ans = json.dumps(ans)
        return ans
    if request.method == 'POST':
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        data = request.data.decode().rstrip(']').lstrip('[')
        if data[1] == 'u':
            command = 'update'
        if data[1] == 'i':
            command = 'insert'
        if command == 'insert':
            data = data.split('"')
            data = filter(lambda x: x != '' and x != ', ', data)
            data = list(map(lambda x: x.rstrip('"').lstrip('"'), data))
            table = data[1]
            values = data[2].split()
            if table[:table.index('(')] in ['user', 'test', 'tg']:
                cur.execute(f'insert into {table} values(?, ?, ?)', values)
                con.commit()
                return '0'
        if command == 'update':
            data = data.split(', ')
            data = list(map(lambda x: x.rstrip('"').lstrip('"'), data))
            data1 = []
            for el in data:
                string = ''
                for symbol in el:
                    if symbol != '\\':
                        string += symbol
                data1.append(string)
            data = data1.copy()
            table = data[1]
            values = data[2] + '"'
            where = data[3] + '"'
            if table in ['user', 'test', 'Tg']:
                cur.execute(f'update {table} set {values} where {where}')
                con.commit()
                return '0'


if __name__ == '__main__':
    app.run(debug=True)
