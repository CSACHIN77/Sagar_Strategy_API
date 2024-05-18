import mysql.connector

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="sagar_strategy"
)

class StraddleRepo:
        
    def insert_data(self,strategy_data,legs_data):
        #print("Rupendra")
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
    
        
            #print(leg_value.id)
            
        mycursor = mydb.cursor()
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
            
            
            

        
