import mysql.connector

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="sagar_strategy"
)

def convert_to_json(result,strategy_id):
    strategies = []
    mycursor = mydb.cursor()
    for row in result:
        strategy = {
            "id": row["id"],
            "name": row["name"],
             "underlying":row["underlying"],
             "strategy_type": row["strategy_type"],
             "implied_futures_expiry": row["implied_futures_expiry"],
             "entry_time": row["entry_time"],
             "last_entry_time": row["last_entry_time"],
             "exit_time": row["exit_time"],
             "square_off": row["square_off"],
             "overall_sl": row["overall_sl"],
             "overall_target": row["overall_target"],
              "trailing_options": row["trailing_options"],
              "profit_reaches": row["profit_reaches"],
              "lock_profit": row["lock_profit"],
              "increase_in_profit": row["increase_in_profit"],
              "trail_profit": row["trail_profit"],
             "legs": []
            
            }
    
    # Fetch data for legs related to the current strategy
        leg_sql = "SELECT * FROM leg WHERE strategy_id = %s"  # Replace 'legs' and 'strategy_id' with your table and column names
        mycursor.execute(leg_sql, (strategy_id,))
        leg_rows = mycursor.fetchall()
    
    # Iterate over leg rows and format data into the desired structure
        for leg_row in leg_rows:
            leg = {
                "atm_straddle_premium": row["atm_straddle_premium"],
                "closest_premium": row["closest_premium"],
                "expiry": row["expiry"],
                "id": row["id"],
                "leg_no": row["leg_no"],
                "lots": row["lots"],
                "no_of_reentry": row["no_of_reentry"],
                "option_type": row["option_type"],
                "percent_of_atm_strike_sign": row["percent_of_atm_strike_sign"],
                "percent_of_atm_strike_value": row["percent_of_atm_strike_value"],
                "position": row["position"],
                "range_breakout": row["range_breakout"],
                "roll_strike": row["roll_strike"],
                "roll_strike_increase_in_profit": row["roll_strike_increase_in_profit"],
                "roll_strike_lock_profit": row["roll_strike_lock_profit"],
                "roll_strike_lock_profit_sign": row["roll_strike_lock_profit_sign"],
                "roll_strike_profit_reaches": row["roll_strike_profit_reaches"],
                "roll_strike_stop_loss": row["roll_strike_stop_loss"],
                "roll_strike_stop_loss_sign": row["roll_strike_stop_loss_sign"],
                "roll_strike_strike_type": row["roll_strike_strike_type"],
                "roll_strike_trail_profit": row["roll_strike_trail_profit"],
                "roll_strike_trail_profit_sign": row["roll_strike_trail_profit_sign"],
                "roll_strike_trailing_options": row["roll_strike_trailing_options"],
                "simple_momentum": row["simple_momentum"],
                "simple_momentum_direction": row["simple_momentum_direction"],
                "simple_momentum_range_breakout": row["simple_momentum_range_breakout"],
                "simple_momentum_sign": row["simple_momentum_sign"],
                "straddle_width_sign": row["straddle_width_sign"],
                "straddle_width_value": row["straddle_width_value"],
                "strategy_id": row["strategy_id"],
                "strike_selection_criteria": row["strike_selection_criteria"],
                "strike_selection_criteria_increase_in_profit": row["strike_selection_criteria_increase_in_profit"],
                "strike_selection_criteria_lock_profit": row["strike_selection_criteria_lock_profit"],
                "strike_selection_criteria_lock_profit_sign": row["strike_selection_criteria_lock_profit_sign"],
                "strike_selection_criteria_profit_reaches": row["strike_selection_criteria_profit_reaches"],
                "strike_selection_criteria_stop_loss": row["strike_selection_criteria_stop_loss"],
                "strike_selection_criteria_stop_loss_sign": row["strike_selection_criteria_stop_loss_sign"],
                "strike_selection_criteria_trail_profit": row["strike_selection_criteria_trail_profit"],
                "strike_selection_criteria_trail_profit_sign": row["strike_selection_criteria_trail_profit_sign"],
                "strike_selection_criteria_trailing_options": row["strike_selection_criteria_trailing_options"],
                "strike_type": row["strike_type"]
            }
            strategy["legs"].append(leg)
            #print(strategy)
    strategies.append(strategy)
    print(strategy)
    data = {"strategies": strategies}
    return data

class StraddleRepo:
        
    def insert_data(self,strategy_data,legs_data):
       
        print(strategy_data.id)
       
        mycursor = mydb.cursor()
        query = """
        INSERT INTO strategy (
                name, underlying, strategy_type, implied_futures_expiry, entry_time,
                last_entry_time, exit_time, square_off, overall_sl, overall_target,
                trailing_options, profit_reaches, lock_profit, increase_in_profit, trail_profit
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (strategy_data.name,strategy_data.underlying,strategy_data.strategy_type,strategy_data.implied_futures_expiry,strategy_data.entry_time,strategy_data.last_entry_time
                                 ,strategy_data.exit_time,strategy_data.square_off,strategy_data.overall_sl,strategy_data.overall_target,strategy_data.trailing_options,strategy_data.profit_reaches
                                 ,strategy_data.lock_profit,strategy_data.increase_in_profit,strategy_data.trail_profit
        )
        print(query) 
        mycursor.execute(query, values)
        mydb.commit()
        print("Data inserted successfully in strategy table.")
        inserted_id = mycursor.lastrowid
        print("Inserted ID:", inserted_id)
    
            #print(leg_value.strategy_id)
        query= """INSERT INTO leg (strategy_id,leg_no,lots,position,option_type,expiry,no_of_reentry,strike_selection_criteria,closest_premium,strike_type,straddle_width_value,straddle_width_sign,percent_of_atm_strike_value,percent_of_atm_strike_sign,atm_straddle_premium,strike_selection_criteria_stop_loss,strike_selection_criteria_stop_loss_sign,strike_selection_criteria_trailing_options,strike_selection_criteria_profit_reaches,strike_selection_criteria_lock_profit,strike_selection_criteria_lock_profit_sign,strike_selection_criteria_increase_in_profit,strike_selection_criteria_trail_profit,strike_selection_criteria_trail_profit_sign,roll_strike,roll_strike_strike_type,roll_strike_stop_loss,roll_strike_stop_loss_sign,roll_strike_trailing_options,roll_strike_profit_reaches,roll_strike_lock_profit,roll_strike_lock_profit_sign,roll_strike_increase_in_profit,roll_strike_trail_profit,roll_strike_trail_profit_sign,simple_momentum_range_breakout,simple_momentum,simple_momentum_sign,simple_momentum_direction,range_breakout) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        for leg_value in legs_data:
            values = (inserted_id,leg_value.leg_no,leg_value.lots,leg_value.position,leg_value.option_type,leg_value.expiry,leg_value.no_of_reentry,leg_value.strike_selection_criteria,leg_value.closest_premium,leg_value.strike_type,leg_value.straddle_width_value,leg_value.straddle_width_sign,leg_value.percent_of_atm_strike_value,leg_value.percent_of_atm_strike_sign,leg_value.atm_straddle_premium,leg_value.strike_selection_criteria_stop_loss,leg_value.strike_selection_criteria_stop_loss_sign,leg_value.strike_selection_criteria_trailing_options,leg_value.strike_selection_criteria_profit_reaches,leg_value.strike_selection_criteria_lock_profit,leg_value.strike_selection_criteria_lock_profit_sign,leg_value.strike_selection_criteria_increase_in_profit,leg_value.strike_selection_criteria_trail_profit,leg_value.strike_selection_criteria_trail_profit_sign,leg_value.roll_strike,leg_value.roll_strike_strike_type,leg_value.roll_strike_stop_loss,leg_value.roll_strike_stop_loss_sign,leg_value.roll_strike_trailing_options,leg_value.roll_strike_profit_reaches,leg_value.roll_strike_lock_profit,leg_value.roll_strike_lock_profit_sign,leg_value.roll_strike_increase_in_profit,leg_value.roll_strike_trail_profit,leg_value.roll_strike_trail_profit_sign,leg_value.simple_momentum_range_breakout,leg_value.simple_momentum,leg_value.simple_momentum_sign,leg_value.simple_momentum_direction,leg_value.range_breakout,)
            #print(query)
            #print(values)
            try:
                mycursor.execute(query, values)
                mydb.commit()
                print("Insertion successful!")
            except Exception as e:
                print("Error:", e)
            
    
    def update_data(self,strategy_data,legs_data,strategyId):
       
        print(strategy_data.id)
       
        mycursor = mydb.cursor()
        query = """
        UPDATE strategy
    SET
        name = %s,underlying = %s,strategy_type = %s,implied_futures_expiry = %s,entry_time = %s,
        last_entry_time = %s,exit_time = %s,square_off = %s,overall_sl = %s,overall_target = %s,
        trailing_options = %s,profit_reaches = %s,lock_profit = %s,increase_in_profit = %s,trail_profit = %s
    WHERE
        id = %s
        """
        values = (strategy_data.name,strategy_data.underlying,strategy_data.strategy_type,strategy_data.implied_futures_expiry,strategy_data.entry_time,strategy_data.last_entry_time
                                 ,strategy_data.exit_time,strategy_data.square_off,strategy_data.overall_sl,strategy_data.overall_target,strategy_data.trailing_options,strategy_data.profit_reaches
                                 ,strategy_data.lock_profit,strategy_data.increase_in_profit,strategy_data.trail_profit,strategyId
        )
        print(query) 
        mycursor.execute(query, values)
        mydb.commit()
        print("Data inserted successfully in strategy table.")
        inserted_id = mycursor.lastrowid
        print("Inserted ID:", inserted_id)
            #print(leg_value.strategy_id)
        query= """INSERT INTO leg (strategy_id,leg_no,lots,position,option_type,expiry,no_of_reentry,strike_selection_criteria,closest_premium,strike_type,straddle_width_value,straddle_width_sign,percent_of_atm_strike_value,percent_of_atm_strike_sign,atm_straddle_premium,strike_selection_criteria_stop_loss,strike_selection_criteria_stop_loss_sign,strike_selection_criteria_trailing_options,strike_selection_criteria_profit_reaches,strike_selection_criteria_lock_profit,strike_selection_criteria_lock_profit_sign,strike_selection_criteria_increase_in_profit,strike_selection_criteria_trail_profit,strike_selection_criteria_trail_profit_sign,roll_strike,roll_strike_strike_type,roll_strike_stop_loss,roll_strike_stop_loss_sign,roll_strike_trailing_options,roll_strike_profit_reaches,roll_strike_lock_profit,roll_strike_lock_profit_sign,roll_strike_increase_in_profit,roll_strike_trail_profit,roll_strike_trail_profit_sign,simple_momentum_range_breakout,simple_momentum,simple_momentum_sign,simple_momentum_direction,range_breakout) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        for leg_value in legs_data:
            values = (inserted_id,leg_value.leg_no,leg_value.lots,leg_value.position,leg_value.option_type,leg_value.expiry,leg_value.no_of_reentry,leg_value.strike_selection_criteria,leg_value.closest_premium,leg_value.strike_type,leg_value.straddle_width_value,leg_value.straddle_width_sign,leg_value.percent_of_atm_strike_value,leg_value.percent_of_atm_strike_sign,leg_value.atm_straddle_premium,leg_value.strike_selection_criteria_stop_loss,leg_value.strike_selection_criteria_stop_loss_sign,leg_value.strike_selection_criteria_trailing_options,leg_value.strike_selection_criteria_profit_reaches,leg_value.strike_selection_criteria_lock_profit,leg_value.strike_selection_criteria_lock_profit_sign,leg_value.strike_selection_criteria_increase_in_profit,leg_value.strike_selection_criteria_trail_profit,leg_value.strike_selection_criteria_trail_profit_sign,leg_value.roll_strike,leg_value.roll_strike_strike_type,leg_value.roll_strike_stop_loss,leg_value.roll_strike_stop_loss_sign,leg_value.roll_strike_trailing_options,leg_value.roll_strike_profit_reaches,leg_value.roll_strike_lock_profit,leg_value.roll_strike_lock_profit_sign,leg_value.roll_strike_increase_in_profit,leg_value.roll_strike_trail_profit,leg_value.roll_strike_trail_profit_sign,leg_value.simple_momentum_range_breakout,leg_value.simple_momentum,leg_value.simple_momentum_sign,leg_value.simple_momentum_direction,leg_value.range_breakout,)
            #print(query)
            #print(values)
            try:
                mycursor.execute(query, values)
                mydb.commit()
                print("Insertion successful!")
            except Exception as e:
                print("Error:", e)
                
    def getStrategyName(self):
        strategy_names = []
        mycursor = mydb.cursor()
        query = "SELECT DISTINCT name FROM strategy"
        mycursor.execute(query)
        result = mycursor.fetchall()
        for row in result:
            strategy_names.append(row[0])
        return strategy_names

    def getStrategyDetails(self, strategy_id):
        mycursor = mydb.cursor(dictionary=True)
        query = """
        SELECT strategy.*, leg.*
        FROM strategy
        INNER JOIN leg ON strategy.id = leg.strategy_id
        WHERE strategy.id = %s
        """
        mycursor.execute(query, (strategy_id,))
        result = mycursor.fetchall()
        stategy_details = convert_to_json(result,strategy_id)
        #for row in result:
         #   strategy_details.append(row)
        return stategy_details
        
        
            
    
    