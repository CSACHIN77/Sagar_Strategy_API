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
    mycursor = mydb.cursor()
    #print(result)
    for row in result:
        strategy = {
            "id": row["id"],
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
    
    def insert_data(self,strategy_data,legs_data):
       
        print(strategy_data.id)


# Option 2: Round and convert to integer
        value_as_int = int(round(float(strategy_data.id)))
        print(value_as_int)
        
        name_value = []
        name_value.append(strategy_data.name)
        mycursor = mydb.cursor()
        query = """
        INSERT INTO portfolio (
                name) VALUES (%s)
        """
        values = (name_value)
        print(query) 
        mycursor.execute(query, values)
        mydb.commit()
        print("Data inserted successfully in strategy table.")
        inserted_id = mycursor.lastrowid
        print("Inserted ID:", inserted_id)
    
            #print(leg_value.strategy_id)
        query= """INSERT INTO portfoliostrategies (portfolio_id,strategy_id,symbol,quantity_multiplier,monday,tuesday,wednesday,thrusday,friday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        inserted_id = mycursor.lastrowid
        for leg_value in legs_data:
            values = (inserted_id,leg_value.strategy_id,leg_value.symbol,leg_value.quantity_multiplier,leg_value.monday,leg_value.tuesday,leg_value.wednesday,leg_value.thrusday,leg_value.friday)
            #print(query)
            #print(values)
            try:
                mycursor.execute(query, values)
                mydb.commit()
                print("Insertion successful!")
            except Exception as e:
                print("Error:", e)
                
    def update_data(self, strategy_data, legs_data, strategyId):
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
            
            for strategy in legs_data:
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
            update_portfolio_values = (strategy_data.name, strategyId)
            mycursor = mydb.cursor()
            mycursor.execute(update_portfolio_query, update_portfolio_values)
            mydb.commit()
            print(f"Updated portfolio name for portfolio with ID: {strategyId}")
    
        except Exception as e:
            print(f"Error updating data: {str(e)}")
            mydb.rollback()  # Rollback in case of error
    
    def getAllPortfolio(self):
        try:
            mycursor = mydb.cursor(dictionary=True)
            value=2
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
                
                # Convert to JSON format
                strategy_details = convert_to_json(result, strategy_id,value)
                # Append strategy details to all_strategies list
                #return strategy_details
                
                all_portfolios.extend(strategy_details)
                #all_strategies.append(result)
            
            # Return all strategies as JSON data
            transformed_data = {"portfolio": all_portfolios}
            # Outputting the transformed data
            #print(json.dumps(transformed_data, indent=2))
            return all_portfolios
        
        except Exception as e:
            print(f"Error retrieving strategy details: {e}")
            return {"error": str(e)}

    def getPortfolioDetails(self, strategy_id):
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
    