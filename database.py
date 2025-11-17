"""
Database module for Finanzverwaltungstool
Handles connection and operations with MariaDB
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

# Load environment variables
load_dotenv()


class Database:
    """Database connection and operations handler"""
    
    def __init__(self):
        """Initialize database connection parameters"""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.user = os.getenv('DB_USER', 'finaz_user')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'finaz_db')
        self.connection = None
    
    def connect(self) -> bool:
        """
        Establish connection to MariaDB database
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Fehler bei der Datenbankverbindung: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
        """
        Execute a query that modifies data (INSERT, UPDATE, DELETE)
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Fehler bei der Query-Ausführung: {e}")
            return False
    
    def fetch_query(self, query: str, params: tuple = None) -> Optional[List[tuple]]:
        """
        Execute a SELECT query and fetch results
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of tuples with results or None if error
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return None
    
    def fetch_one(self, query: str, params: tuple = None) -> Optional[tuple]:
        """
        Execute a SELECT query and fetch one result
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Tuple with result or None if error/no result
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return None
    
    def get_last_insert_id(self) -> Optional[int]:
        """
        Get the last inserted ID
        
        Returns:
            Last insert ID or None
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except Error as e:
            print(f"Fehler beim Abrufen der Insert-ID: {e}")
            return None
