import aiosqlite

class Driver():
    """
    Internal Driver file for use in the database file

    Parameters
    ----------
    table_name : str
        The name of the table to be created
    columns : str
        The columns to be created in the table

    Methods
    -------
    __init__(table_name:str,columns:str) -> None
        Constructor for the Driver class
    create_table(table_name:str,columns:str) -> None
        Creates a table in the database
    insert(columns:str,values:str) -> None
        Inserts a row into the table
    select(columns:str,where:str) -> None
        Selects a row from the table
    update(where:str,columns:list,values:list) -> None
        Updates a row in the table
    delete(where:str) -> None
        Deletes a row from the table
    close() -> None
        Closes the connection to the database

    Returns
    -------
    Driver
        The driver object
    """
    def __init__(self,table_name,columns=""):
        self.table_name = table_name
        """
        Generates a database object

        Parameters
        ----------
        table_name : str
            The name of the table to be created
        columns : str
            The columns to be created in the table
        """

            
        async def cog_load(self):
            self.create_table(f"{table_name}",f"{columns}")
    
    async def create_table(self,table_name,columns):
        """
        Creates a table in the database

        Parameters
        ----------
        table_name : str
            The name of the table to be created
        columns : str
            The columns to be created in the table
        """

 
        async with aiosqlite.connect('database.db') as db:
            await db.execute(f'CREATE TABLE IF NOT EXISTS {table_name}({columns})')
            await db.commit()

    async def insert(self,columns,values):
        """
        Inserts a row into the table

        Parameters
        ----------
        columns : str
            The columns to be inserted into
        values : str
            The values to be inserted into the columns
        """
        async with aiosqlite.connect('database.db') as db:
            await db.execute(f"INSERT INTO {self.table_name}({columns}) VALUES({values})")
            await db.commit()

    async def select(self,columns,where=None):
        """
        Selects a row from the table

        Parameters
        ----------
        columns : str
            The columns to be selected from
        Where : str, optional
            The where statement to be used, defualts to None
        """
        if where:
             async with aiosqlite.connect('database.db') as db:
                async with db.execute(f'SELECT {columns} FROM {self.table_name}  WHERE {where}') as cursor:
                    rows = await cursor.fetchall()
                    return rows

        else:
            async with aiosqlite.connect('database.db') as db:
                async with db.execute(f'SELECT {columns} FROM {self.table_name}') as cursor:
                    rows = await cursor.fetchall()
                    return rows


    async def update(self,where,columns=[],values=[]):
        """
        Updates a row in the table

        Parameters
        ----------
        where : str
            The where statement to be used
        columns : list, optional
            The columns to be updated, defualts to []
        values : list, optional
            The values to be updated, defualts to []
        """
        if len(columns) != len(values):
            raise Exception("columns and values must be the same length")
        else:
            statement = ""
            for c in columns:
                statement = statement + (f"{c} = {values[columns.index(c)]}")
                if columns.index(c) != len(columns) - 1:
                    statement = statement + ", "
            print(f"UPDATE {self.table_name} SET {statement} WHERE {where}")
        async with aiosqlite.connect('database.db') as db:
            await db.execute(f"UPDATE {self.table_name} SET {statement} WHERE {where}")
            await db.commit()
    
    async def delete(self,where):
        """
        Deletes a row from the table

        Parameters
        ----------
        where : str
            The where statement to be used
        """
        async with aiosqlite.connect('database.db') as db:
            await db.execute(f"DELETE FROM {self.table_name} WHERE {where}")
            await db.commit()
    
