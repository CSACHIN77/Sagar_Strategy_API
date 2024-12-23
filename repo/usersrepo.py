import json
import mysql.connector
from mysql.connector import Error
import os
import sys


try:
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the current script
    sagar_common_path = os.path.join(current_dir, "../../Sagar_common")  # Go up two levels to "OGCODE"
    if sagar_common_path not in sys.path:
        sys.path.append(sagar_common_path)
    from common_function import fetch_parameter
except ImportError as e:
    print(f"Errorfetching db details: {e}")


def connect_to_users_db() -> mysql.connector.connection.MySQLConnection:
    try:
        env = "dev"  # Environment, e.g., 'dev', 'prod'
        key = "db_sagar_strategy"  # Example key
        db_Value = fetch_parameter(env, key)
        if db_Value is None:
            raise HTTPException(status_code=500, detail="Failed to fetch database configuration.")
        print(f"Fetched db config: {db_Value}")

        conn = mysql.connector.connect(
            host=db_Value['host'],
            database=db_Value['database'],
            user=db_Value['user'],
            password=db_Value['password'],
        )
        if conn.is_connected():
            print("Connected to database.")
            return conn
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

def convert_boolean(value):
    if isinstance(value, bool):
        return int(value)
        
    if isinstance(value, str) and value.lower() == 'true':
        return 1
    elif isinstance(value, str) and value.lower() == 'false':
        return 0
    return value



class UsersRepo:
    def __init__(self,data):
        self.data = data

    def registerUser(self,data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        #print(data)
        mycursor = conn.cursor()
        query = """
        INSERT INTO user (
            username, password, email, emailVerificationStatus, first_name, middle_name, last_name,
            mobile, mobileVerificationStatus, address, dateofbirth, risk_profile, last_login, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        print(f"mobileverify {data.get('mobileVerificationStatus')}")

        values = (
            data['username'], data['password'], data['email'], convert_boolean(data.get('emailVerificationStatus', False)),
            data.get('first_name'), data.get('middle_name'), data.get('last_name'),
            data.get('mobile'), convert_boolean(data.get('mobileVerificationStatus', False)), data.get('address'),
            data.get('dateofbirth'), data.get('risk_profile'), data.get('last_login'), convert_boolean(data.get('is_active', True))
        )
        
        try:
            mycursor.execute(query, values)
            conn.commit()
            
            print("Record inserted successfully.")
            user_id = mycursor.lastrowid
            return user_id

        except Error as e:
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message} 
        
        finally:
            if conn.is_connected():
                mycursor.close()
    
    def edituser(self,data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        mycursor = conn.cursor()
        check_query = "SELECT * FROM user WHERE id = %s"
        mycursor.execute(check_query, (data['id'],))
        result = mycursor.fetchone()
        if result:
        # Prepare the update query
            update_query = """
                UPDATE user
                SET 
                    username = %s,
                    password = %s,
                    email = %s,
                    emailVerificationStatus = %s,
                    first_name = %s,
                    middle_name = %s,
                    last_name = %s,
                    mobile = %s,
                    mobileVerificationStatus = %s,
                    address = %s,
                    dateofbirth = %s,
                    risk_profile = %s,
                    last_login = %s,
                    is_active = %s
                WHERE id = %s
            """
            values = (
                data['username'],
                data['password'],
                data['email'],
                convert_boolean(data.get('emailVerificationStatus', False)),
                data['first_name'],
                data['middle_name'],
                data['last_name'],
                data['mobile'],
                convert_boolean(data.get('mobileVerificationStatus', False)),
                data['address'],
                data['dateofbirth'],
                data['risk_profile'],
                data['last_login'],
                convert_boolean(data.get('is_active', True)),
                data['id']
            )
            
            try:
                mycursor.execute(update_query, values)
                conn.commit()  # Commit the changes
                return {'id': data['id'], 'update_status': True}
            except Exception as e:
                conn.rollback()  # Rollback in case of error
                return {'id': data['id'], 'update_status': False, 'error': str(e)}
        else:
            return {'id': data['id'], 'update_status': False, 'error': 'User ID not found.'}

        # Close the cursor
        mycursor.close()

    def addUserBroker(self,data):
        #print(data)
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        mycursor = conn.cursor()
        query = """
        INSERT INTO UserBrokers (
            user_id, broker_id, API_Key, API_Secret,market_api_key,market_api_secret
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data['user_id'], data['broker_id'], data['api_key'], data['api_secret'],data['market_api_key'],data['market_api_secret']
        )
        
        try:
            mycursor.execute(query, values)
            conn.commit()
            
            print("Record inserted successfully.")
            user_id = mycursor.lastrowid
            return user_id

        except Error as e:
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message} 
        
        finally:
            if conn.is_connected():
                mycursor.close()

    def editUserBroker(self,data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        mycursor = conn.cursor()
        check_query = "SELECT * FROM UserBrokers WHERE id = %s AND user_id = %s AND broker_id = %s"
        values = (data['id'],data['user_id'], data['broker_id'])
        mycursor.execute(check_query, values)
        result = mycursor.fetchone()
        if result:
        # Prepare the update query
            update_query = """
                UPDATE UserBrokers
                SET 
                    API_Key = %s,
                    API_Secret = %s,
                    market_api_key = %s,
                    market_api_secret = %s
                WHERE id = %s AND user_id = %s AND broker_id = %s
            """
            values = (
                data['api_key'],
                data['api_secret'],
                data['market_api_key'],
                data['market_api_secret'],
                data['id'],
                data['user_id'],
                data['broker_id']
            )
            
            try:
                mycursor.execute(update_query, values)
                conn.commit()  # Commit the changes
                return {'id': data['id'],'user_id': data['user_id'], 'broker_id': data['broker_id'], 'update_status': True}
            except Exception as e:
                conn.rollback()  # Rollback in case of error
                return {'id': data['id'],'user_id': data['user_id'], 'broker_id': data['broker_id'], 'update_status': False, 'error': str(e)}
        else:
            return {'id': data['id'],'user_id': data['user_id'], 'broker_id': data['broker_id'], 'update_status': False, 'error': 'UserBroker record not found.'}
            # Close the cursor
            mycursor.close()
    
    def deleteUserBroker(self,data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        mycursor = conn.cursor()
        check_query = "SELECT * FROM UserBrokers WHERE id=%s AND user_id = %s AND broker_id = %s"
        values = (data['id'],data['user_id'], data['broker_id'])
        mycursor.execute(check_query, values)
        result = mycursor.fetchone()
        if result:
            delete_query = "DELETE FROM UserBrokers WHERE id=%s AND user_id = %s AND broker_id = %s"
            try:
                mycursor.execute(delete_query, values)
                conn.commit()  # Commit the changes
                return {'id': data['id'],'user_id': data['user_id'], 'broker_id': data['broker_id'], 'delete_status': True}
            except Exception as e:
                conn.rollback()
                return {'id': data['id'],'user_id': data['user_id'], 'broker_id': data['broker_id'], 'delete_status': False, 'error': str(e)}
        else:
            return {'id': data['id'],'user_id': data['user_id'], 'broker_id': data['broker_id'], 'delete_status': False, 'error': 'UserBroker record not found.'}
            # Close the cursor
            mycursor.close()  
    
    def getAllBrokers(self):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        mycursor = conn.cursor()
        query = """SELECT id, name FROM Broker"""
        
        try:
            mycursor.execute(query)  # Execute the query without needing 'values'
            
            # Fetch all rows from the result set
            result = mycursor.fetchall()
            
            # Format the result as a list of dictionaries
            modules = [{"id": str(row[0]), "name": row[1]} for row in result]
            
            return modules  # Return the formatted result
        
        except Error as e:
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message}
        
        finally:
            if conn.is_connected():
                mycursor.close()

    def addBroker(self,data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        #print(data)
        mycursor = conn.cursor()
        query = """
        INSERT INTO broker (
            name
        ) VALUES (%s)
        """
        values = (
            data['name'],
        )
        
        try:
            mycursor.execute(query, values)
            conn.commit()
            
            # Fetch the inserted broker's ID (assuming it is auto-incremented)
            user_id = mycursor.lastrowid  # This will get the last inserted row's ID
            
            print(f"Record inserted successfully with ID: {user_id}")
            return {"id": user_id}  # Return the ID in a dictionary

        except Error as e:
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message} 
        
        finally:
            if conn.is_connected():
                mycursor.close()

    def editBroker(self,data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        mycursor = conn.cursor()
        check_query = "SELECT * FROM broker WHERE id = %s"
        values = (data['id'],)
        mycursor.execute(check_query, values)
        result = mycursor.fetchone()
        if result:
        # Prepare the update query
            update_query = """
                UPDATE broker
                SET 
                    name = %s
                WHERE id = %s
            """
            values = (
                data['name'],
                data['id']
            )
            
            try:
                mycursor.execute(update_query, values)
                conn.commit()  # Commit the changes
                return {'id': data['id'], 'update_status': True}
            except Exception as e:
                conn.rollback()  # Rollback in case of error
                return {'id': data['id'], 'update_status': False, 'error': str(e)}
        else:
            return {'id': data['id'], 'update_status': False, 'error': 'UserBroker record not found.'}
            # Close the cursor
            mycursor.close()
    
    def deleteBroker(self,data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        mycursor = conn.cursor()
        check_query = "SELECT * FROM broker WHERE id = %s"
        values = (data['id'],)
        mycursor.execute(check_query, values)
        result = mycursor.fetchone()
        if result:
            delete_query = "DELETE FROM broker WHERE id = %s"
            try:
                mycursor.execute(delete_query, values)
                conn.commit()  # Commit the changes
                return {'id': data['id'],'delete_status': True}
            except Exception as e:
                conn.rollback()
                return {'id': data['id'],'delete_status': False, 'error': str(e)}
        else:
            return {'id': data['id'],'delete_status': False, 'error': 'UserBroker record not found.'}
            # Close the cursor
            mycursor.close()  

    def addBilling(self, data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
    # Create cursor to execute SQL queries
        mycursor = conn.cursor()

        # Initialize the list of columns and values to be inserted
        columns = ["user_id", "billing_type"]
        values = [data['user_id'], data['billing_type']]

        # Add profit_sharing_type only if not already in the list (based on billing_type)
        if data['billing_type'] == 'profit sharing':
            columns.append("profit_sharing_type")
            values.append(data['profit_sharing_type'])

        # Add one_time_fee based on billing_type condition
        if data['billing_type'] == 'one time':
            columns.append("one_time_fee")
            values.append(data.get('one_time_fee', 0))  # Default to 0 if not provided
        else:
            # Set one_time_fee to 0 if not 'one time'
            columns.append("one_time_fee")
            values.append(0)

        # If the billing_type is 'subscription', include subscription_type and subscription_fee
        if data['billing_type'] == 'subscription':
            columns.extend(["subscription_type", "subscription_fee"])
            values.extend([data.get('subscription_type'), data.get('subscription_fee') or None])  # Default to None if empty
        else:
            # Set subscription_type and subscription_fee to None for other billing types
            columns.extend(["subscription_type", "subscription_fee"])
            values.extend([None, None])

        # If the profit_sharing_type is 'flat', include profit_sharing_flat_profit_percent and profit_sharing_flat_less_percent
        if data.get('profit_sharing_type') == 'flat' and data.get('billing_type') == 'profit sharing':
            columns.extend(["profit_sharing_flat_profit_percent", "profit_sharing_flat_less_percent"])
            values.extend([data.get('profit_sharing_flat_profit_percent') or None, 
                        data.get('profit_sharing_flat_less_percent') or None])
        else:
            # Set profit sharing flat percentages to None if profit_sharing_type is not 'flat'
            columns.extend(["profit_sharing_flat_profit_percent", "profit_sharing_flat_less_percent"])
            values.extend([None, None])

        # Construct the SQL query dynamically based on columns and values
        query = f"""
        INSERT INTO billing ({', '.join(columns)})
        VALUES ({', '.join(['%s'] * len(values))})
        """

        try:
            # Execute the query with the provided values
            mycursor.execute(query, values)

            # Commit the transaction to save the data
            conn.commit()

            # Get the ID of the last inserted row
            billing_id = mycursor.lastrowid
            print(f"Record inserted successfully with ID: {billing_id}")

            # If the profit_sharing_type is 'slab', insert into ProfitSharingSlabs
            if data.get('profit_sharing_type') == 'slab' and data.get('billing_type') == 'profit sharing':
                for slab in data['profit_sharing_slabs']:
                    slab_query = """
                        INSERT INTO ProfitSharingSlabs (billing_id, `from`, `to`, profit_percent, less_percent)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    slab_values = (
                        billing_id,
                        slab['from'],
                        slab['to'],
                        slab['profit_percent'],
                        slab['less_percent']
                    )
                    mycursor.execute(slab_query, slab_values)

                # Commit the transaction to save the slabs data
                conn.commit()

            return billing_id

        except Error as e:
            # Handle any errors during execution
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message}

        finally:
            # Ensure the cursor is closed after execution
            if conn.is_connected():
                mycursor.close()

    def getAllModules(self):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        mycursor = conn.cursor()
        query = """SELECT id, name FROM Modules"""
        
        try:
            mycursor.execute(query)  # Execute the query without needing 'values'
            
            # Fetch all rows from the result set
            result = mycursor.fetchall()
            
            # Format the result as a list of dictionaries
            modules = [{"id": str(row[0]), "name": row[1]} for row in result]
            
            return modules  # Return the formatted result
        
        except Error as e:
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message}
        
        finally:
            if conn.is_connected():
                mycursor.close()

    def addModules(self,data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        #print(data)
        mycursor = conn.cursor()
        query = """
        INSERT INTO Modules (
            name
        ) VALUES (%s)
        """
        values = (
            data['name'],
        )
        
        try:
            mycursor.execute(query, values)
            conn.commit()
            
            # Fetch the inserted broker's ID (assuming it is auto-incremented)
            user_id = mycursor.lastrowid  # This will get the last inserted row's ID
            
            print(f"Record inserted successfully with ID: {user_id}")
            return {"id": user_id}  # Return the ID in a dictionary

        except Error as e:
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message} 
        
        finally:
            if conn.is_connected():
                mycursor.close()

    def addUserAccessModules(self, data):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        mycursor = conn.cursor()
        
        query = """
        INSERT INTO UserAccessModules (
            user_id, module_id, enabled
        ) VALUES (%s, %s, %s)
        """
        
        inserted_data = []  # This will hold the results to return
        
        try:
            for entry in data:
                # Insert data
                values = (entry['user_id'], entry['module_id'], entry['enabled'])
                mycursor.execute(query, values)
                
                # After executing the insert, fetch the generated ID for the current row
                inserted_id = mycursor.lastrowid
                
                # Append the inserted record with the generated ID
                inserted_data.append({
                    'id': inserted_id,
                    'user_id': entry['user_id'],
                    'module_id': entry['module_id'],
                    'enabled': entry['enabled']
                })
            
            # Commit the transaction after all inserts
            conn.commit()
            
            print("Records inserted successfully.")
            
            return inserted_data  # Return the data with the new IDs
            
        except Error as e:
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message}
        
        finally:
            if conn.is_connected():
                mycursor.close()
    
    def getAllUsers(self):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        mycursor = conn.cursor()
        query = """SELECT id, username, password, email, emailVerificationStatus, 
                          first_name, middle_name, last_name, mobile, mobileVerificationStatus, 
                          address, dateofbirth, risk_profile, last_login, is_active 
                   FROM User"""
        
        try:
            mycursor.execute(query)  # Execute the query without needing 'values'
            
            # Fetch all rows from the result set
            result = mycursor.fetchall()
            
            # Format the result as a list of dictionaries
            users = [{
                "id": str(row[0]), 
                "username": row[1], 
                "password": row[2], 
                "email": row[3], 
                "emailVerificationStatus": row[4],
                "first_name": row[5], 
                "middle_name": row[6], 
                "last_name": row[7], 
                "mobile": row[8], 
                "mobileVerificationStatus": row[9], 
                "address": row[10], 
                "dateofbirth": row[11], 
                "risk_profile": row[12], 
                "last_login": row[13], 
                "is_active": row[14]
            } for row in result]
            
            return users  # This return should be inside the method
        
        except Error as e:
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message}
        
        finally:
            if conn.is_connected():
                mycursor.close()
                conn.close()

    def getAllUserBroker(self):
        conn = connect_to_users_db()

        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")
        mycursor = conn.cursor()
        query = """SELECT id,user_id, broker_id, API_Key, API_Secret, market_api_key, 
                          market_api_secret
                   FROM UserBrokers"""
        
        try:
            mycursor.execute(query)  # Execute the query without needing 'values'
            
            # Fetch all rows from the result set
            result = mycursor.fetchall()
            
            # Format the result as a list of dictionaries
            users = [{
                "id": str(row[0]), 
                "user_id": row[1], 
                "broker_id": row[2], 
                "API_Key": row[3], 
                "API_Secret": row[4],
                "market_api_key": row[5], 
                "market_api_secret": row[6]
            } for row in result]
            
            return users  # This return should be inside the method
        
        except Error as e:
            error_message = f"Error: {e}"
            print(error_message)
            return {"error": error_message}
        
        finally:
            if conn.is_connected():
                mycursor.close()
                conn.close()