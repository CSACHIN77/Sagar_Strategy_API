import mysql.connector

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="sagar_strategy"
)

def convert_to_json(result,strategy_id,value):
    portfolios = []
    #print('5')
    print(f'Result {result}')
    mycursor = mydb.cursor()
    #print(result)
    for row in result:
        strategy = {
            "id":strategy_id,
            "name": row["name"],
             "strategies": []            
            }
    
        
    # Fetch data for legs related to the current strategy
        #('6')
        leg_sql = """SELECT id,portfolio_Id, strategy_id, symbol, quantity_multiplier,monday, tuesday, wednesday, thrusday, friday FROM portfoliostrategies WHERE portfolio_Id = %s"""  # Replace 'legs' and 'strategy_id' with your table and column names
        mycursor.execute(leg_sql, (strategy_id,))
        leg_rows = mycursor.fetchall()
        #print(leg_rows)
    # Iterate over leg rows and format data into the desired structure
        for leg_row in leg_rows:
            #print('9')
            #print(leg_row)
            strategies = {
                "portfolio_Id": leg_row[1],
                "strategy_id": leg_row[2],
				"id": leg_row[0],
                "symbol": leg_row[3],
                "quantity_multiplier": leg_row[4],
                "monday": bool(leg_row[5]),
                "tuesday": bool(leg_row[6]),
                "wednesday": bool(leg_row[7]),
                "thrusday": bool(leg_row[8]),
                "friday": bool(leg_row[9])
                }
            #print(leg)
            strategy["strategies"].append(strategies)
                    #print(strategy)
    portfolios.append(strategy)
            #print(strategy)
    #data = {"strategies": strategy}
    # = strategies
    if value==1:       
        return strategy
    else:
        return portfolios

class PortfolioRepo:
    def __init__(self):
        pass
    
    def insert_data(self,portfolio,strategies,strategyvariables,legs):
       
      
        mycursor = mydb.cursor()
    
        # Insert into portfolio table
        name_value = [portfolio.name]
        query = "INSERT INTO portfolio (name) VALUES (%s)"
        try:
            mycursor.execute(query, name_value)
            mydb.commit()
            print("Data inserted successfully in portfolio table.")
            portfolio_id = mycursor.lastrowid
            print("Inserted Portfolio ID:", portfolio_id)
        except Exception as e:
            print("Error inserting into portfolio table:", e)
            return
    
        # Insert into portfoliostrategies table
        for strategy in strategies:
            query = """
                INSERT INTO portfoliostrategies (portfolio_id, strategy_id, symbol, quantity_multiplier, monday, tuesday, wednesday, thrusday, friday)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                portfolio_id,
                strategy.strategy_id,
                strategy.symbol,
                strategy.quantity_multiplier,
                strategy.monday,
                strategy.tuesday,
                strategy.wednesday,
                strategy.thrusday,  # corrected spelling of 'thursday'
                strategy.friday
            )
            try:
                mycursor.execute(query, values)
                mydb.commit()
                print("Insertion successful into portfoliostrategies table!")
                strategy_id = mycursor.lastrowid  # Get the inserted strategy_id
            except Exception as e:
                print("Error inserting into portfoliostrategies table:", e)
                return
    
        # Insert into portfoliostrategyvariables table
        for variable in strategyvariables:
            query = """
                INSERT INTO portfoliostrategyvariables (
                    portfolio_strategy_id, underlying, strategy_type, quantity_multiplier, implied_futures_expiry,
                    entry_time, last_entry_time, exit_time, square_off, overall_sl, overall_target, trailing_options,
                    profit_reaches, lock_profit, increase_in_profit, trail_profit
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                strategy_id,  # Use the strategy_id as portfolio_strategy_id
                variable.underlying,
                variable.strategy_type,
                variable.quantity_multiplier,
                variable.implied_futures_expiry,
                variable.entry_time,
                variable.last_entry_time,
                variable.exit_time,
                variable.square_off,
                variable.overall_sl,
                variable.overall_target,
                variable.trailing_options,
                variable.profit_reaches,
                variable.lock_profit,
                variable.increase_in_profit,
                variable.trail_profit
            )
            try:
                mycursor.execute(query, values)
                mydb.commit()
                print("Insertion successful into portfoliostrategyvariables table!")
                portfolio_strategy_id = mycursor.lastrowid  # Get the inserted portfolio_strategy_id
            except Exception as e:
                print("Error inserting into portfoliostrategyvariables table:", e)
                return
    
        # Insert into leg table
        for leg_value in legs:
            query = """
                INSERT INTO portfoliostrategyvariableslegs (
                    portfolio_strategy_variables_id, lots, position, option_type, expiry, no_of_reentry,
                    strike_selection_criteria, closest_premium, strike_type, straddle_width_value, straddle_width_sign,
                    percent_of_atm_strike_value, percent_of_atm_strike_sign, atm_straddle_premium,
                    strike_selection_criteria_stop_loss, strike_selection_criteria_stop_loss_sign,
                    strike_selection_criteria_trailing_options, strike_selection_criteria_profit_reaches,
                    strike_selection_criteria_lock_profit, strike_selection_criteria_lock_profit_sign,
                    strike_selection_criteria_increase_in_profit, strike_selection_criteria_trail_profit,
                    strike_selection_criteria_trail_profit_sign, roll_strike, roll_strike_strike_type,
                    roll_strike_stop_loss, roll_strike_stop_loss_sign, roll_strike_trailing_options,
                    roll_strike_profit_reaches, roll_strike_lock_profit, roll_strike_lock_profit_sign,
                    roll_strike_increase_in_profit, roll_strike_trail_profit, roll_strike_trail_profit_sign,
                    simple_momentum_range_breakout, simple_momentum, simple_momentum_sign, simple_momentum_direction,
                    range_breakout
                ) VALUES ((SELECT id FROM portfoliostrategyvariables WHERE portfolio_strategy_id = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                portfolio_strategy_id,
                leg_value.lots,
                leg_value.position,
                leg_value.option_type,
                leg_value.expiry,
                leg_value.no_of_reentry,
                leg_value.strike_selection_criteria,
                leg_value.closest_premium,
                leg_value.strike_type,
                leg_value.straddle_width_value,
                leg_value.straddle_width_sign,
                leg_value.percent_of_atm_strike_value,
                leg_value.percent_of_atm_strike_sign,
                leg_value.atm_straddle_premium,
                leg_value.strike_selection_criteria_stop_loss,
                leg_value.strike_selection_criteria_stop_loss_sign,
                leg_value.strike_selection_criteria_trailing_options,
                leg_value.strike_selection_criteria_profit_reaches,
                leg_value.strike_selection_criteria_lock_profit,
                leg_value.strike_selection_criteria_lock_profit_sign,
                leg_value.strike_selection_criteria_increase_in_profit,
                leg_value.strike_selection_criteria_trail_profit,
                leg_value.strike_selection_criteria_trail_profit_sign,
                leg_value.roll_strike,
                leg_value.roll_strike_strike_type,
                leg_value.roll_strike_stop_loss,
                leg_value.roll_strike_stop_loss_sign,
                leg_value.roll_strike_trailing_options,
                leg_value.roll_strike_profit_reaches,
                leg_value.roll_strike_lock_profit,
                leg_value.roll_strike_lock_profit_sign,
                leg_value.roll_strike_increase_in_profit,
                leg_value.roll_strike_trail_profit,
                leg_value.roll_strike_trail_profit_sign,
                leg_value.simple_momentum_range_breakout,
                leg_value.simple_momentum,
                leg_value.simple_momentum_sign,
                leg_value.simple_momentum_direction,
                leg_value.range_breakout
            )
            try:
                mycursor.execute(query, values)
                mydb.commit()
                print("Insertion successful into leg table!")
            except Exception as e:
                print("Error inserting into leg table:", e)
                return
    
        mycursor.close()
            
    def update_data(self, portfolio_data, strategy_data, strategyId):
        try:
            # Connect to MySQL
            mycursor = mydb.cursor()
    
            # Delete existing records for the given portfolio_Id
            delete_query = "DELETE FROM portfoliostrategies WHERE portfolio_Id = %s"
            delete_values = (strategyId,)
            mycursor.execute(delete_query, delete_values)
            print(f"Deleted existing portfolio strategies for portfolio with ID: {strategyId}")
    
            # Insert new values
            insert_query = """
                INSERT INTO portfoliostrategies (portfolio_Id, strategy_id, symbol, quantity_multiplier,
                                                monday, tuesday, wednesday, thrusday, friday)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            for strategy in strategy_data:
                strategy_id = strategy.strategy_id
                symbol = strategy.symbol
                quantity_multiplier = strategy.quantity_multiplier
                monday = strategy.monday
                tuesday = strategy.tuesday
                wednesday = strategy.wednesday
                thrusday = strategy.thrusday  # Corrected typo 'thrusday' to 'thrusday'
                friday = strategy.friday
                
                insert_values = (
                    strategyId, strategy_id, symbol, quantity_multiplier,
                    monday, tuesday, wednesday, thrusday, friday
                )
                mycursor.execute(insert_query, insert_values)
                print(f"Inserted new portfolio strategy for strategy_id: {strategy_id}")
    
            # Commit changes and close cursor
            mydb.commit()
            mycursor.close()
    
            # Optionally, update portfolio name (as per your original code)
            update_portfolio_query = "UPDATE portfolio SET name = %s WHERE id = %s"
            update_portfolio_values = (portfolio_data.name, strategyId)
            mycursor = mydb.cursor()
            mycursor.execute(update_portfolio_query, update_portfolio_values)
            mydb.commit()
            print(f"Updated portfolio name for portfolio with ID: {strategyId}")
    
        except Exception as e:
            print(f"Error updating data: {str(e)}")
            mydb.rollback()  # Rollback in case of error
    
    def getAllPortfolio(self):
        
        mydb = None
        mycursor = None
        
            
        try:
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="sagar_strategy"
            )
            
            mycursor = mydb.cursor(dictionary=True)
            value = 2

            # Step 1: Fetch all unique strategy IDs
            mycursor.execute("SELECT DISTINCT id FROM portfolio")
            strategy_ids = [row['id'] for row in mycursor.fetchall()]
            
            # List to store all strategy details
            all_portfolios = []
            
            # Step 2: Iterate over each strategy_id and fetch details
            for strategy_id in strategy_ids:
                # Fetch strategy details
                query = """
                SELECT *
                FROM portfolio
                WHERE id = %s
                """
                
                mycursor.execute(query, (strategy_id,))
                result = mycursor.fetchall()

                #if result:
                    # Convert to JSON format
                    #strategy_details = convert_to_json(result, strategy_id, value)
                    # Append strategy details to all_portfolios list
                    #all_portfolios.extend(strategy_details)
            
            # Return all portfolios as JSON data
                    #transformed_data = {"portfolio": all_portfolios}
            
            # Outputting the transformed data
            #print(json.dumps(transformed_data, indent=2))
            return result
        
        except mysql.connector.Error as err:
            print(f"Error retrieving strategy details: {err}")
            return {"error": str(err)}
        finally:
            # Close cursor and connection
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()

    def getPortfolioDetails(self, strategy_id):
        print(f'Rupendra getPortfolioDetails')
        #print('3')
        value=1
        mycursor = mydb.cursor(dictionary=True)
        stategy_details = ""
        query =  """
        SELECT *
        FROM portfolio
        WHERE id = %s
        """
        mycursor.execute(query, (strategy_id,))
        result = mycursor.fetchall()
        #print('4')
        stategy_details = convert_to_json(result,strategy_id,value)
        #for row in result:
            #   strategy_details.append(row)
            

        return stategy_details

'''            
    def update_data(self, strategy_data, legs_data, strategyId):
        try:
            # Update portfolio Name
            print(strategy_data.id)
            
            name_value = []
            name_value.append(strategy_data.name)
            mycursor = mydb.cursor()
            #print(strategy_data.id)
           # Update portfolio Name
            query = """UPDATE portfolio SET Name = %s WHERE Id = %s"""
            values = (strategy_data.name, strategyId)
            mycursor.execute(query, values)
            result = mycursor.fetchone()

            print(f"Update successful for portfolio record with ID: {strategyId}")
            #print(legs_data)
            for strategy in legs_data:
                strategy_id = strategy.strategy_id
                symbol = strategy.symbol
                quantity_multiplier = strategy.quantity_multiplier
                monday = strategy.monday
                tuesday = strategy.tuesday
                wednesday = strategy.wednesday
                thrusday = strategy.thrusday # Note: Corrected typo 'thrusday' to 'thrusday'
                friday = strategy.friday
    
                # Check if the strategy record exists
                check_strategy_query = "SELECT Id FROM portfoliostrategies WHERE portfolio_Id = %s AND strategy_id = %s"
                check_strategy_values = (strategyId, strategy_id)
                mycursor.execute(check_strategy_query, check_strategy_values)
                #result = mycursor.fetchone()
                mycursor.fetchall()
                mydb.commit()
                 
                if mycursor.rowcount > 0:
                    # Update the existing record
                    update_strategy_query = """
                        UPDATE portfoliostrategies
                        SET symbol = %s, quantity_multiplier = %s, monday = %s, tuesday = %s,
                            wednesday = %s, thrusday = %s, friday = %s
                        WHERE portfolio_Id = %s AND strategy_id = %s
                    """
                    update_strategy_values = (
                        symbol, quantity_multiplier, monday, tuesday, wednesday,
                        thrusday, friday, strategyId, strategy_id
                    )
                    mycursor.execute(update_strategy_query, update_strategy_values)
                    mydb.commit()
                    print(f"Updated portfolio strategy for strategy_id: {strategy_id}")
        # Close cursor
            mycursor.close()

        except Exception as e:
            print(f"Error updating portfolio data: {str(e)}")
            mydb.rollback() 
'''
    