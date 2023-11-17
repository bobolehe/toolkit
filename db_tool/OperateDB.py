"""自行封装数据库工具类"""

import datetime
import re
import logging
import mysql.connector
from mysql.connector.errors import IntegrityError


class MysqlData:
    # 初始化
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # 链接数据库对象
        self.DB = None
        # 链接游标
        self.curr = None
        # 链接数据库库名
        self.data = None
        # 链接表表名
        self.table = None
        # 第一次链接数据时间
        self.ks_time = datetime.datetime.now()
        self.logger.info(f"数据类实例化成功")

    # 创建连接
    def connect(self, host: str, user: str, password: str, port: int):
        """
        提供链接参数，返回链接数据库对象
        :param host: 连接地址：默认'127.0.0.1'
        :param user: 数据库用户名：默认“root”
        :param password:数据库密码：默认“123456”
        :param port: 连接数据库端口3306
        :return: 返回结果，操作游标以及数据库链接对象
        """
        try:
            # 连接数据库并创建游标
            self.DB = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                port=port,
                auth_plugin='mysql_native_password',
                # autocommit=False  # 确保自动提交模式关闭

            )
            self.curr = self.DB.cursor()
        except Exception as e:
            # 返回结果字典
            retu = {
                'error': f"数据库连接失败{e}"
            }
            self.logger.error(retu['error'])
            return retu
        else:
            # 连接成功返回结果字典，携带数据库对象以及游标对象
            retu = {
                'error': "数据库链接成功",
                'cursor': self.curr,
                'db': self.DB
            }
            self.logger.info(f"数据库链接成功")
            return retu

    # 查询所有数据库名
    def query_database(self):
        """

        :return: 返回所有的数据库库名
        """
        self.curr.execute('SHOW DATABASES;')
        result = self.curr.fetchall()
        self.logger.info(f"{str(datetime.datetime.now())},查询数据库所有库名")
        return result

    # 查询库中所有表名
    def query_sheet(self, db_name: str):
        """
        db_name: 可指定查询数据库
        :return: 返回数据库所有的表名
        """
        if db_name:
            self.curr.execute('SHOW TABLES;')
            result = self.curr.fetchall()
            return result
        else:
            self.switch_database(db_name=db_name)
            self.curr.execute('SHOW TABLES')
            result = self.curr.fetchall()
            return result

    # 切换数据库
    def switch_database(self, db_name: str):
        """
        切换数据库，如果数据库不存在则创建后切换
        :param db_name: 指定数据库游标切换
        :return: 返回提示信息
        """
        # 创建数据库的sql(如果数据库存在就不创建，防止异常)
        self.data = db_name
        sql = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        try:
            # 执行创建数据库的sql
            self.curr.execute(sql)
            self.DB.commit()
        except:
            # 失败回滚，返回失败信息
            self.DB.rollback()
            return f"判断数据库{db_name}是否存在失败"
        else:
            # 数据库存在无需创建
            self.logger.info(f"数据库{db_name}切换成功")
            self.curr.execute(f'use {db_name};')
            return f"数据库{db_name}切换成功数据库"

    # 查询数据表是否存在
    def create_table(self, table: str, sql_str: str = ""):
        """
        判断数据库表是否存在,不存在进行创建
        :param table: 指定数据表
        :param sql_str: 可指定创建表的sql语句
        :return: 返回提示信息
        """
        # 列出所有表名
        self.table = table
        sql = "show tables"
        try:
            self.curr.execute(sql)
            tables = self.curr.fetchall()
        except:
            return "查询数据库表结构失败"
        else:
            # 解析查询到的数据库表
            tables_list = re.findall('(\'.*?\')', str(tables))
            tables_list = [re.sub("'", '', each) for each in tables_list]

        # 判断指定表名是否存在其中
        if table in tables_list:
            return f"{table}表存在数据库"
        else:
            # 创建表结构
            try:
                if not sql_str:
                    sql = f"""CREATE TABLE {table}  (
                                  `id` bigint(0) NOT NULL,
                                  PRIMARY KEY (`id`) USING BTREE
                                ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
                                """
                else:
                    sql = sql_str
                self.curr.execute(sql)
                self.DB.commit()
                return f"数据表{table}不存在进行初始化创建表结构成功"
            except Exception as e:
                self.DB.rollback()
                return f"数据表{table}不存在进行创建表结构失败,请提供正确的spl语句"

    # 表结构添加字段
    def table_add_fields(self, field: str, fields: list, table: str):
        """
        实现数据表字段的添加
        :return:
        """
        sql = f"ALTER TABLE `{self.data}`.`{table}` "
        if not len(fields):
            return "无需创建"
        try:
            for i, k in enumerate(fields):
                # 添加第一条字段依据原有字段进行添加
                if k == 'url':
                    sql_new = sql + f"ADD COLUMN `{k}` varchar(255) NULL DEFAULT '' AFTER `{field}`;"
                elif 'time' in k:
                    sql_new = sql + f"ADD COLUMN `{k}` datetime(0) NULL AFTER `{field}`;"
                    # sql_new = sql + f"ADD COLUMN `{k}` datetime(255) NULL ON UPDATE CURRENT_TIMESTAMP(255) AFTER `{field}`;"
                # elif k.endswith("id"):
                #     sql_new = sql + f"ADD COLUMN `{k}` bigint(0) NULL AFTER `{field}`;"
                else:
                    sql_new = sql + f"ADD COLUMN `{k}` json NULL AFTER `{field}`;"
                self.curr.execute(sql_new)
                self.DB.commit()
        except Exception as e:
            return f"{table}表结构字段添加创建失败" + f"{e}"
        else:
            return f"{table}字段添加创建成功"

    # 判断字段是否存在
    def field_exists(self, fields: dict, table: str):
        """
        接收字段，判断字段是否存在，字段存在无需操作，字段不存在自行创建
        :param fields: 接收item字典判断字段是否存在
        :param table: 指定表名
        :return:
        """
        # 查询表结构所有字段
        try:
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '%s' AND TABLE_NAME = '%s'" % (
                self.data, table)
            self.curr.execute(sql)
            results = self.curr.fetchall()
        except:
            return '查询数据表所有字段失败'
        # 表结构字段进行格式化
        results_list = []
        for result in results:
            results_list.append(result[0])

        if not len(fields):
            return '没有传递字段参数'

        # 校验所需字段在数据表中是否存在
        fields_list = []
        for field in fields:
            if not (field in results_list):
                fields_list.append(field)
        # 待添加字段中存在需要添加字段，执行添加字段方法
        if fields_list:
            return self.table_add_fields(field=results_list[-1], fields=fields_list, table=table)
        else:
            return f'{table}表结构字段无需创建'

    # 关闭连接
    def close(self, time: str = None, table: str = None):
        """
        关闭提供的链接以及游标
        :return: 返回提示信息
        """
        try:
            self.curr.close()
            self.DB.close()
            return '关闭成功'
            # sql = f"SELECT cve FROM {table} WHERE {time} >= '{self.ks_time}';"
            # sql = "SELECT * FROM eol WHERE stime >= '2023-04-11 17:16:10';"
            # self.curr.execute(sql)
            # result = self.curr.fetchall()
        except Exception as e:
            self.curr.close()
            self.DB.close()
            return f'关闭失败,错误信息{e}'

    # 指定表名，添加数据
    def add_data(self, item: dict, table: str):
        """
        添加数据
        :param item: 需要传递字典参数（键需要与数据表字段对应）
        :param table: 数据表表名
        :return: 返回提示信息
        """
        # 将item对象的键值分别取出
        keys = sorted(list(item.keys()), key=len)
        values = [item[key] for key in keys]
        # sql语句
        sql = f"insert into {table}(`{'`,`'.join(keys)}`) values ({'%s,' * ((len(values) - 1))}%s);"

        try:
            # self.DB.start_transaction()
            self.curr.execute(sql, tuple(values))
            self.DB.commit()
        # except IntegrityError:
        #     return "id数据已存在"
        except Exception as e:
            self.DB.rollback()
            return '数据实例化存储失败' + sql % tuple(values) + f"{e}"
        else:
            return '数据实例化存储成功'

    # 删除指定字段数据
    def delete_data(self, table: str, field: str, price: str):
        """
        删除指定字段匹配数据
        :param table: 指定表名
        :param field: 指定字段名
        :param price: 指定需要匹配数据
        :return:
        """
        sql = f"DELETE FROM {table} WHERE `{field}` = {price};"
        try:
            self.curr.execute(sql)
            self.DB.commit()
            return f"{price}数据删除成功"
        except Exception as e:
            self.DB.rollback()
            return "数据删除失败" + f"错误信息{e}"

    # 提供匹配字段与数据匹配数据是否存在
    def price_exists(self, field: str = None, price: str = None, field2: str = None, price2: str = None, table: str = None):
        """
        验证数据是否存在，指定字段，传入字段查询数据
        :param table: 表名
        :param field: 传入指定字段名
        :param price: 传入查询数据
        :param field2: 两个判断条件使用此参数传递第二个判断数据字段名
        :param price2: 传入第二个判断条件的数据
        :return: 返回字典信息，提示信息以及状态码
        """
        if not price:
            err = {
                'error': 103,
                'log': "请传入查询数据"
            }
            return err

        if not field:
            err = {
                'error': 103,
                'log': "请指定查询数据字段名，一般使用url字段查询"
            }
            return err
        if not field2:
            sql = f"SELECT id FROM {table} where {field}=%s;"
            try:
                # 执行查询语句
                self.curr.execute(sql, (price,))
                result = self.curr.fetchall()
            except Exception as e:
                err = {
                    'error': 104,
                    'log': f'{field}字段 数据查询失败{str(e)}'
                }
                return err
            if result:
                err = {
                    'error': 102,
                    'log': f'{price}数据存在',
                    'data': result[0][0]
                }
            else:
                err = {
                    'error': 101,
                    'log': f'无{price}链接数据'
                }
            return err
        else:
            sql = f'SELECT id FROM {table} where `{field}` = "{price}" and `{field2}` = "{price2}";'
            try:
                # 执行查询语句
                self.curr.execute(sql)
                # print(sql)
                result = self.curr.fetchall()
            except Exception as e:
                err = {
                    'error': 104,
                    'log': f'{field}字段 数据查询失败{str(e)}'
                }
                return err
            if result:
                err = {
                    'error': 102,
                    'log': f'{price}数据存在',
                    'data': result[0][0]
                }
            else:
                err = {
                    'error': 101,
                    'log': f'无{price}链接数据'
                }
            return err

    # 获取最新更新时间
    def query_time(self, field: str = None, name: str = None, fields: str = None, table: str = None):
        """
        获取指定匹配字段数据中指定字段最大值
        :param name: 指定字段名称
        :param fields: 对于数据库中抓取多个类型的url时候可以使用
        :param field: 增加判断条件，比如满足字段pro下的值为coles的数据再进行判断页数字段的最大值
        :param table: 表名
        :return:
        """

        if fields:
            sql = f'SELECT MAX({name}) FROM {table} WHERE {fields} = "{field}";'

            try:
                # 执行查询语句
                self.curr.execute(sql)
                result = self.curr.fetchall()
                # result = self.curr.fetchone()
            except Exception as e:
                return 404, e
            else:
                result_list = [row for row in result[0]][0]
                return result_list
        else:
            sql = f"SELECT MAX({name}) FROM {table};"

            try:
                # 执行查询语句
                self.curr.execute(sql)
                # result = self.curr.fetchall()
                result = self.curr.fetchall()
            except:
                return 404
            else:
                result_list = [row for row in result]
                result_list = [row for row in result_list[0]]
                return result_list[0]

    # 获取更新数据量
    def query_data_count(self, table: str, field: str, data_time: str):
        """
        通过指定表名、字段、时间，获取指定时间后的数据量
        :param table:
        :param field:
        :param data_time:
        :return:
        """
        sql = f"SELECT COUNT(*) FROM {table} WHERE {field} >= '{data_time}';"
        try:
            # 执行查询语句
            self.curr.execute(sql)
            result = self.curr.fetchall()

        except Exception as e:

            return [404, e]
        else:
            result_list = [row for row in result]
            return result_list

    # 获取指定时间字段指定时间后的数据
    def query_data(self, table: str, max_time: str, field: str, fields: str):
        """
        获取指定时间字段指定时间后的数据
        :param table: 指定表名
        :param max_time: 指定匹配时间
        :param field: 指定匹配时间字段
        :param fields: 指定返回数据字段 （*号代表全部字段数据）
        :return:
        """
        sql = f"SELECT {fields} FROM {table} WHERE {field} > '{max_time}';"
        try:
            # 执行查询语句
            self.curr.execute(sql)
            result = self.curr.fetchall()
            field_list = self.curr.column_names
            # result = self.curr.fetchone()
        except Exception as e:

            return [404, e]
        else:
            result_list = [row for row in result]
            return [result_list, field_list]

    # 执行sql语句
    def run_sql(self, sql: str):
        """
        执行sql语句
        :param sql: 接受sql语句进行执行
        :return: 返回执行结果
        """
        try:
            self.curr.execute(sql)
            result = self.curr.fetchall()
            self.DB.commit()
        except Exception as e:
            return f"执行sql语句错误，错误信息{e}"
        return result

    def query_cpe(self, table: str = None, cpe_item: dict = None):

        sql = f"SELECT id,cpe_part,cpe_vendor,cpe_product FROM {table} WHERE 0 = 0"
        if cpe_item['cpe']:
            i = cpe_item['cpe'].replace("\\", "\\\\")
            sql += f" AND cpe = '{i}'"

        try:
            # print("查询规则绑定cpe是否存在", sql)
            # 执行查询语句
            self.curr.execute(sql)
            result = self.curr.fetchall()
        except Exception as e:
            err = {
                'error': 104,
                'log': f'cpe字段 数据查询失败{str(e)}'
            }
            return err
        if result:
            err = {
                'error': 102,
                'data': result
            }
        else:
            err = {
                'error': 101,
            }
        return err

    def query_cpe_matches(self, table: str = None, matches_item: dict = None):
        sql = f"SELECT id FROM {table} WHERE 0 = 0"
        if matches_item['cpe']:
            cpe = matches_item['cpe'].replace("\\", "\\\\")
            sql += f" AND cpe = '{cpe}'"
        if matches_item['versionStartExcluding']:
            sql += f" AND versionStartExcluding = '{matches_item['versionStartExcluding']}'"
        if matches_item['versionStartIncluding']:
            sql += f" AND versionStartIncluding = '{matches_item['versionStartIncluding']}'"
        if matches_item['versionEndIncluding']:
            sql += f" AND versionEndIncluding = '{matches_item['versionEndIncluding']}'"
        if matches_item['versionEndExcluding']:
            sql += f" AND versionEndExcluding = '{matches_item['versionEndExcluding']}'"

        try:
            print("查询规则数据是否存在", sql)
            # 执行查询语句
            self.curr.execute(sql)
            result = self.curr.fetchall()
        except Exception as e:
            err = {
                'error': 104,
                'log': f'cpe匹配规则数据查询失败{str(e)}'
            }
            return err
        if result:
            err = {
                'error': 102,
                'data': result
            }
        else:
            err = {
                'error': 101,
            }
        return err

    # 取指定字段满足条件的所有数据
    def query_field(self, table: str = None, field: str = None, price: str = None):
        sql = f'SELECT * FROM {table} WHERE {field} = "{price}";'
        try:
            self.curr.execute(sql)
            result = self.curr.fetchall()
            self.DB.commit()
        except Exception as e:
            return f"执行sql语句错误，错误信息{e}"
        return result

    # 提供指定范围获取表数据
    def batch_get(self, table: str = None, page_size: int = None, offset: int = None):
        """
        添加数据
        :param table: 数据表表名
        :param page_size: 指定取值数量
        :param offset: 指定取值起始位置
        :return: 返回提示信息
        """
        sql = f"SELECT * FROM {table} LIMIT {page_size} OFFSET {offset}"
        try:
            self.curr.execute(sql)
            result = self.curr.fetchall()
            self.DB.commit()
        except Exception as e:
            return f"执行sql语句错误，错误信息{e}"
        return result

    # 获取指定字段数据量
    def count_get(self, table: str = None, field: str = None):
        sql = f"SELECT COUNT({field}) FROM {table}"
        try:
            self.curr.execute(sql)
            result = self.curr.fetchall()[0][0]
            self.DB.commit()
        except Exception as e:
            return f"执行sql语句错误，错误信息{e}"
        return result

    # 获取匹配满足条件指定字段数据
    def query_field_r(self, table: str = None, r_field: str = None, field: str = None, price: str = None):
        """
        获取满足匹配条件指定字段数据
        :param table:
        :param r_field:
        :param field:
        :param price:
        :return:
        """
        sql = f"select {r_field} from {table} where {field} = '{price}';"
        try:
            # print("查询规则绑定cpe是否存在", sql)
            # 执行查询语句
            self.curr.execute(sql)
            result = self.curr.fetchall()
        except Exception as e:
            err = {
                'error': 104,
                'log': f'查询满足条件指定字段数据，查询失败{str(e)}'
            }
            return err
        if result:
            err = {
                'error': 102,
                'data': result
            }
        else:
            err = {
                'error': 101,
            }
        return err

    # 更新指定字段数据
    def update_field(self, table: str = None, condition: str = None, ask: str = None, field: str = None, price: str = None):
        """
        更新指定字段数据
        :param table:
        :param condition:
        :param field:
        :param price:
        :param ask:
        :return:
        """
        sql = f"UPDATE {table} SET {field}='{price}' WHERE {condition}='{ask}';"
        try:
            # 执行查询语句
            self.curr.execute(sql)
            self.DB.commit()
        except Exception as e:
            err = {
                'error': 104,
                'log': f'查询满足条件指定字段数据，查询失败{str(e)}'
            }
            return err
        else:
            err = {
                'error': 102,
                'log': f'更新完成'
            }
        return err


if __name__ == '__main__':
    DB = MysqlData()
    print(DB.connect(host="127.0.0.1", user="root", password="123456", port=3306))
    sql = "use spiders;"
    print(DB.run_sql(sql=sql))
    print(DB.run_sql(sql="SELECT MAX(cve_last_modified_time) FROM nvd;"))
