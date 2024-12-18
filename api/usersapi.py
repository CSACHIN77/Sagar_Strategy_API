from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Any, Optional,Dict, Union
from fastapi.middleware.cors import CORSMiddleware
import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import List
import os
import json
import sys
import pandas as pd
import logging

try:
    current_directory = os.path.dirname('usersapi.py')
    # Construct the path to the parent directory
    parent_directory = os.path.abspath(os.path.join(current_directory, '..'))
    # Add the parent directory to the system path
    sys.path.append(parent_directory)
    from repo.usersdetails import UserService
except ImportError as e:
    print(f"Error importing Portfolioservice: {e}")


try:
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the current script
    sagar_common_path = os.path.join(current_dir, "../../Sagar_common")  # Go up two levels to "OGCODE"
    if sagar_common_path not in sys.path:
        sys.path.append(sagar_common_path)
    from common_function import fetch_parameter
except ImportError as e:
    print(f"Errorfetching db details: {e}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


#------------------------------------------------------------------------------------------------------
# USERS APIS
#------------------------------------------------------------------------------------------------------

def connect_to_users_db() -> mysql.connector.connection.MySQLConnection:

    try:
        env = "dev"  # Environment, e.g., 'dev', 'prod'
        key = "db_sagar_users"  # Example key
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

#User Registration
@app.post("/registeruser", response_model=dict)
async def registeruser(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        user_service = UserService(data)
        user_id = user_service.registerUser(conn,data)
        data["id"] = user_id
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Edit User Details
@app.post("/edituser", response_model=dict)
async def edituser(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        user_service = UserService(data)
        user_id = user_service.editUser(conn,data)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Add UserBroker
@app.post("/addUserBroker", response_model=dict)
async def addUserBroker(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        user_service = UserService(data)
        value = user_service.addUserBroker(conn,data)
        data = {"id": value} | data
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Edit User Broker
@app.post("/editUserBroker", response_model=dict)
async def editUserBroker(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        user_service = UserService(data)
        user_id = user_service.editUserBroker(conn,data)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Delete User Broker
@app.post("/deleteUserBroker", response_model=dict)
async def deleteUserBroker(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        user_service = UserService(data)
        user_id = user_service.deleteUserBroker(conn,data)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Add Broker
@app.post("/addBroker", response_model=dict)
async def addBroker(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        print(data)
        user_service = UserService(data)
        user_id = user_service.addBroker(conn,data)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Edit Broker
@app.post("/editBroker", response_model=dict)
async def editBroker(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        user_service = UserService(data)
        user_id = user_service.editBroker(conn,data)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Delete Broker
@app.post("/deleteBroker", response_model=dict)
async def deleteBroker(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        user_service = UserService(data)
        user_id = user_service.deleteBroker(conn,data)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#GET ALL Brokers
@app.get("/getAllBrokers", response_model=list)
async def getAllBrokers():
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        data = []
        user_service = UserService(data)
        value = user_service.getAllBrokers(conn)
        return value

    except Exception as e:
        # Handle unexpected exceptions and provide error response
        raise HTTPException(status_code=500, detail=str(e))


#Add Billing
@app.post("/addBilling", response_model=dict)
async def addBilling(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        print(data)
        user_service = UserService(data)
        user_id = user_service.addBilling(conn,data)
        data = {"id": user_id} | data
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Add Modules
@app.post("/addModules", response_model=dict)
async def addModules(data: dict):
    
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))
        print(data)
        user_service = UserService(data)
        user_id = user_service.addModules(conn,data)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#GET ALL MODULES
@app.get("/getAllModules", response_model=list)
async def getAllModules():
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        data = []
        user_service = UserService(data)
        value = user_service.getAllModules(conn)
        return value

    except Exception as e:
        # Handle unexpected exceptions and provide error response
        raise HTTPException(status_code=500, detail=str(e))



#Add UserAccessModules
@app.post("/addUserAccessModules", response_model=list)
async def addUserAccessModules(data: List[dict]):  
    conn = connect_to_users_db()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        print(type(data))  # This will show that data is a List of dicts
        user_service = UserService(data)
        value = user_service.addUserAccessModules(conn, data)  # Pass data as a list

        # Check if the value returned is True (successful operation)
        return value

    except Exception as e:
        # Handle unexpected exceptions and provide error response
        raise HTTPException(status_code=500, detail=str(e))

# Main for running the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
