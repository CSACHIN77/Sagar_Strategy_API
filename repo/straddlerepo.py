# straddlerepo.py
import mysql.connector

class StraddleRepo:
    def __init__(self, host='localhost', user='root', password='root', database='sagar_strategy'):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def insert_data(self, data):
        query = '''
            INSERT INTO strategy (
                entry_time, exit_time, implied_futures_expiry, increase_in_profit,
                last_entry_time, lock_profit, name, overall_sl, overall_target,
                profit_reaches, square_off, strategy_type, trail_profit, trailing_options,
                underlying
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (
            data['entry_time'], data['exit_time'], data['implied_futures_expiry'],
            data['increase_in_profit'], data['last_entry_time'], data['lock_profit'],
            data['name'], data['overall_sl'], data['overall_target'],
            data['profit_reaches'], data['square_off'], data['strategy_type'],
            data['trail_profit'], data['trailing_options'], data['underlying']
        )
        self.cursor.execute(query, values)
        self.conn.commit()

