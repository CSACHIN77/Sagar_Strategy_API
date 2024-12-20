from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Any, Optional,Dict, Union
from fastapi.middleware.cors import CORSMiddleware
import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
import json
import pandas as pd
import logging
#from constants import DB_CONFIG

def connect_to_db() -> mysql.connector.connection.MySQLConnection:  # Fixed function name
    try:
        conn = mysql.connector.connect(
            host='localhost',
<<<<<<< HEAD
            #database='sagar_strategy',
=======
            #database='sagar_users',
>>>>>>> bd9a5ce74d9afe7d838e6a6083b7d54ec743e10a
            user='root',
            password='root'
        )
        if conn.is_connected():
            print("Connected to database.")
            return conn
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

def create_database():
    try:
        conn = ""
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS sagar_strategy;")
<<<<<<< HEAD
        print(f"Database sagar_strategy created successfully.")
=======
        print(f"Database sagar_users created successfully.")
>>>>>>> bd9a5ce74d9afe7d838e6a6083b7d54ec743e10a
        cursor.execute("USE sagar_strategy;")

        #create user table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS User (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            emailVerificationStatus BOOLEAN DEFAULT FALSE,
            first_name VARCHAR(100),
            middle_name VARCHAR(100),
            last_name VARCHAR(100),
            mobile VARCHAR(15) unique,
            mobileVerificationStatus BOOLEAN DEFAULT FALSE,
            address VARCHAR(200),
            dateofbirth DATE,
            risk_profile INT CHECK (risk_profile BETWEEN 1 AND 5),
            last_login DATETIME,
            is_active BOOLEAN DEFAULT TRUE
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Table 'User' created successfully (if it did not exist).")
    

        # Create the Billing table with composite primary key
        create_billing_table_query = """
        CREATE TABLE IF NOT EXISTS Billing (
            id INT AUTO_INCREMENT,
            user_id INT NOT NULL,
            billing_type VARCHAR(50) NOT NULL,
            one_time_fee DECIMAL(10, 2) DEFAULT 0,
            subscription_type VARCHAR(50) DEFAULT NULL,
            subscription_fee DECIMAL(10, 2) DEFAULT 0,
            profit_sharing_type VARCHAR(50) DEFAULT NULL,
            profit_sharing_flat_profit_percent DECIMAL(10, 2),
            profit_sharing_flat_less_percent DECIMAL(10, 2),
            PRIMARY KEY (id, user_id),
            UNIQUE(id),
            FOREIGN KEY (user_id) REFERENCES User(id)
        );
        """
        cursor.execute(create_billing_table_query)
        conn.commit()
        print("Table 'Billing' created successfully (if it did not exist).")

        
 
        # Create the ProfitSharingSlabs table with composite primary key
        create_profit_sharing_slabs_table_query = """
        CREATE TABLE IF NOT EXISTS ProfitSharingSlabs (
            id INT AUTO_INCREMENT UNIQUE,
            billing_id INT NOT NULL UNIQUE,
            `from` DECIMAL(10, 2) ,
            `to` DECIMAL(10, 2) ,
            profit_percent DECIMAL(10, 2) ,
            less_percent DECIMAL(10, 2) ,
            FOREIGN KEY (billing_id) REFERENCES Billing(Id),
            PRIMARY KEY (id, billing_id)
        );
        """
        cursor.execute(create_profit_sharing_slabs_table_query)
        conn.commit()
        print("Table 'ProfitSharingSlabs' created successfully (if it did not exist).")

        create_modules_table_query = """
        CREATE TABLE IF NOT EXISTS Modules (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100)
        );
        """
        cursor.execute(create_modules_table_query)
        print("Table 'Modules' created successfully (if it did not exist).")

        create_user_access_modules_table_query = """
        CREATE TABLE IF NOT EXISTS UserAccessModules (
            id INT AUTO_INCREMENT,
            user_id INT,
            module_id INT,
            enabled BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (id,user_id, module_id),
            FOREIGN KEY (user_id) REFERENCES User(id),
            FOREIGN KEY (module_id) REFERENCES Modules(id)
        );
        """
        cursor.execute(create_user_access_modules_table_query)
        print("Table 'UserAccessModules' created successfully (if it did not exist).")

        # Create the Broker table
        create_broker_table_query = """
        CREATE TABLE IF NOT EXISTS Broker (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
        """
        cursor.execute(create_broker_table_query)
        print("Table 'Broker' created successfully (if it did not exist).")

        # Create the UserBrokers table with composite primary key
        create_user_brokers_table_query = """
        CREATE TABLE IF NOT EXISTS UserBrokers (
            id INT AUTO_INCREMENT,
            user_id INT,
            broker_id INT,
            API_Key VARCHAR(255),
            API_Secret VARCHAR(255),
            market_api_key VARCHAR(255),
            market_api_secret VARCHAR(255),
            PRIMARY KEY (id, user_id, broker_id),
            FOREIGN KEY (user_id) REFERENCES User(id),
            FOREIGN KEY (broker_id) REFERENCES Broker(id)
        );
        """
        cursor.execute(create_user_brokers_table_query)
        print("Table 'UserBrokers' created successfully (if it did not exist).")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()
