import sqlite3
from libs.dataBaseError import *

class DataBase:

    connect:sqlite3.Connection #数据库连接
    cursor:sqlite3.Cursor #数据库指针

    def __init__(self, db_path:str='./data_base/database.db3'):
        try:
            self.connect = sqlite3.connect(db_path)
            self.cursor = self.connect.cursor()
        except:
            raise ConnectFaild
        else:
            print(f"已成功连接至数据库\n文件路径：{db_path}")

    def __getitem__(self, key:str):
        try:
            return Table(self.connect, self.cursor, key)
        except:
            raise

    #新建表单（未完工）
    def creat_table(self, table_name,item_list:list):
        '''
        用于创建表单
        '''
        cmd = list()
        for line in item_list:
            line_name = line[0]
            #print(len(line),type(line),line)
            if type(line)==str:
                line_name = line
                line_type='TEXT'
                flag='NOT NULL'
            elif type(line)==tuple and len(line)==2:
                line_type=line[1]
                flag='NOT NULL'
            elif type(line)==tuple and len(line)==3:
                if line[1] not in ['INT','TEXT','REAL']: raise TypeNotSupport
                else: line_type=line[1]
                flag = line[2]
            else:
                raise ArgsError
            cmd.append(f"{line_name}  {line_type}  {flag}")
        cmd = ','.join(cmd)
        # print(cmd)
        try:
            self.cursor.execute(f"CREATE TABLE {table_name.upper()}(ID INTEGER PRIMARY KEY AUTOINCREMENT,{cmd});")
        except sqlite3.OperationalError as msg:
            raise OperationalError(error_msg=str(msg))
        else:
            return True

class Table:

    __connect:sqlite3.Connection #数据库连接
    __cursor:sqlite3.Cursor #数据库指针
    __name:str #表单名

    def __init__(self, connect, cursor, name):
        self.__connect = connect
        self.__cursor = cursor
        self.__name = name.upper()

    #数据添加（待优化）
    def add(self, data:list):
        '''添加单条数据'''
        keys = list()
        values = list()
        type_control = 0
        for item in data:
            if type(item)==tuple and len(item)==2 and type_control in [0,1]:
                type_control=1
                keys.append(item[0])
                value = item[1]
                if type(value)==str:values.append(f"'{value}'")
                else:values.append(str(value))
            elif type(item) in [str,int] and type_control in [0,2]:
                type_control=2
                if type(item)==str:values.append(f"'{item}'")
                else:values.append(str(item))
            else:
                raise ArgsError
        if len(keys)>0:
            keys = f'({",".join(keys)})'
            values = f'({",".join(values)})'
        else:
            keys=''
            values = f'(NULL,{",".join(values)})'
        try:
            self.__cursor.execute(f"INSERT INTO {self.__name} {keys} VALUES {values}")
            self.__connect.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as msg:
            raise OperationalError(error_msg=str(msg))
        else:
            return True

    #数据删除
    def delete(self, requirements:list):
        '''删除数据，返回被删除的数据的list'''
        require_list = " and ".join(requirements)
        data = self.check(requirements=requirements)
        self.__cursor.execute(f"DELETE from {self.__name} where {require_list};")
        self.__connect.commit()
        return data

    #数据修改
    def update(self, requirements:list, key:str, value):
        '''修改数据，返回修改后的数据'''
        require_list = " and ".join(requirements)
        if type(value)==str:value=f"'{value}'"
        print('数据库执行操作：',f"UPDATE {self.__name} SET {key} = {value} WHERE {require_list};")
        self.__cursor.execute(f"UPDATE {self.__name} SET {key} = {value} WHERE {require_list};")
        self.__connect.commit()
        data = self.check(requirements=requirements)
        return data        

    #数据查询
    def check(self, requirements:list=None, keys:list=['*'] ):
        '''数据查询，根据查询的关键字返回list'''
        if keys==['*']: 
            keys = self.title()
        values=",".join(keys)
        require_list = ""
        if requirements:
            require_list = "where "+" and ".join(requirements)
        try:
            print('数据库执行操作：',f"SELECT {values}  from {self.__name} {require_list};")
            temp = list(self.__cursor.execute(f"SELECT {values}  from {self.__name} {require_list};"))
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as msg:
            raise OperationalError(error_msg=str(msg))
        else:
            for i in range(len(temp)):
                t = dict()
                index = 0
                for key in keys:
                    t[key]=temp[i][index]
                    index+=1
                temp[i]=t
            return temp
                
    #返回以本表表头为key，空值为value的字典
    def row(self):
        '''返回以本表表头为key，空值为value的字典'''
        try:
            temp = list(self.__cursor.execute(f"PRAGMA table_info({self.__name})"))
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as msg:
            raise OperationalError(error_msg=str(msg))
        else:
            result = dict()
            for item in temp:
                result[item[1]]=None
            return result

    #以list格式返回本表表头
    def title(self):
        '''以list格式返回本表表头'''
        return list(self.row().keys())

    #为此表增加新列
    def addColumn(self, column_name:str, value_type:str='TEXT', flag:str='', default_value=None):
        '''为此表增加新列，返回修改后的表头'''
        try:
            if default_value:
                if type(default_value)==str: default_value=f"default '{default_value}'"
                else: default_value=f"default {default_value}"
            else: default_value=''
            self.__cursor.execute(f"ALTER TABLE {self.__name} ADD COLUMN {column_name} {value_type} {flag} default {default_value};")
            self.__connect.commit()
            return self.title()
        except sqlite3.OperationalError as msg:
            raise OperationalError(error_msg=str(msg))

