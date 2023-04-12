from .data import *
from .driver import *
database_uri = "sqlite:///example.db"
# TODO: this file needs rewriting
import json
import aiosqlite

class Database():
    def __init__(self):
        self.pool = None
        self.applications = Driver("Applications","id TEXT PRIMARY KEY, type JSON, notifications JSON")
        self.users = Driver("Users", "id TEXT PRIMARY KEY, applications JSON")
        


    async def get_all_applications(self):
        applications = []
        async with aiosqlite.connect("database.db") as conn:
            async with conn.execute("SELECT * FROM applications") as cursor:
                async for row in cursor:
                    applications.append(Application(row[0], row[1], row[2]))
            return applications
    
    async def application_is_in_database(self, id:int):
        if await self.applications.select("*", f"id = {id}") is not None:
            return True
        return False
    
    async def get_application(self, id:int):
        if await self.application_is_in_database(id):
            return Application(id, await self.applications.select("type",f"id = {id}"),self.applications.select("notifications",f"id = {id}"))
        else:
            raise Exception("Application not in database")
    
    async def add_application_to_database(self, id: int, type: json, notifications: json):
        if not await self.application_is_in_database(id):
            await self.applications.insert("id,type,notifications",f"{id},{type},{notifications}")
            return True
        else:
            raise Exception("Application already in database")

    async def remove_application_from_database(self, id: int):
        if await self.application_is_in_database(id):
            await self.applications.delete(f"id = {id}")
            return True
        else:
            raise Exception("Application not in database")

    async def add_application_notification(self, id: int, notification: json):
        if await self.application_is_in_database(id):
            notifications = await self.applications.select("notifications", f"id = {id}")
            notifications = json.loads(notifications)
            notifications.append(notification)
            await self.applications.update(f"id = {id}", ["notifications"], [json.dumps(notifications)])
            return True
        else:
            raise Exception


    async def remove_application_notification(self, id: int, notification: json):
        
        if await self.__application_is_in_database(id):
            notifications = await self.applications.select("notifications", f"id = {id}")
        
            # need to properly update the json object
        
            await self.applications.update(f"id = {id}", ["notifications"], [notifications])
            return True
        else:
            raise Exception("Application not in database")

    async def get_notifications(self, id: int):
        async with aiosqlite.connect("database.db") as conn:
            async with conn.execute("SELECT * FROM users WHERE id = ?", (id,)) as cursor:
                row = await cursor.fetchone()
                if row is not None:
                    return User(id, row[1])
                else:
                    raise Exception("User not in database")
    
    async def add_notification(self, id: int, notification: json):
        async with aiosqlite.connect("database.db") as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM users WHERE id = ?", (id,))
                user = await cur.fetchone()
                if user is not None:
                    notifications = json.loads(user[2])
                    notifications[notification["application"]].append(notification)
                    await cur.execute("UPDATE users SET applications = ? WHERE id = ?", (json.dumps(notifications), id))
                    await self.add_application_notification(notification["application"], notification)
                    return True
                else:
                    raise Exception("User not in database")

    
    async def add_notification(self, id: int, notification: dict):
        async with aiosqlite.connect("database.db") as conn:
            async with conn.cursor() as cur:
                # Check if user exists
                await cur.execute("SELECT * FROM users WHERE id = ?", (id,))
                user = await cur.fetchone()
                if user is not None:
                    # Retrieve current notifications for user
                    await cur.execute("SELECT applications FROM users WHERE id = ?", (id,))
                    notifications = json.loads(await cur.fetchone()[0])

                    # Update notifications and write to database
                    notifications.append(notification)
                    await cur.execute("UPDATE users SET applications = ? WHERE id = ?", (json.dumps(notifications), id))
                    await conn.commit()

                    # Update application notifications
                    await self.add_application_notification(notification["application"], notification)
                    return True
                else:
                    raise Exception("User not in database")

    async def remove_notification(self, id: int, notification: dict):
        async with aiosqlite.connect("database.db") as conn:
            async with conn.cursor() as cur:
                # Check if user exists
                await cur.execute("SELECT * FROM users WHERE id = ?", (id,))
                user = await cur.fetchone()
                if user is not None:
                    # Retrieve current notifications for user
                    await cur.execute("SELECT applications FROM users WHERE id = ?", (id,))
                    notifications = json.loads(await cur.fetchone()[0])

                    # Update notifications and write to database
                    notifications.remove(notification)
                    await cur.execute("UPDATE users SET applications = ? WHERE id = ?", (json.dumps(notifications), id))
                    await conn.commit()

                    # Remove application notifications
                    await self.remove_application_notification(notification["application"], notification)
                    return True
                else:
                    raise Exception("User not in database")

    async def update_notification(self, id: int, notification: dict):
        async with aiosqlite.connect("database.db") as conn:
            async with conn.cursor() as cur:
                # Check if user exists
                await cur.execute("SELECT * FROM users WHERE id = ?", (id,))
                user = await cur.fetchone()
                if user is not None:
                    # Retrieve current notifications for user
                    await cur.execute("SELECT applications FROM users WHERE id = ?", (id,))
                    notifications = json.loads(await cur.fetchone()[0])

                    # Find and update the notification
                    for i, n in enumerate(notifications):
                        if n["id"] == notification["id"]:
                            notifications[i] = notification
                            break

                    # Update notifications and write to database
                    await cur.execute("UPDATE users SET applications = ? WHERE id = ?", (json.dumps(notifications), id))
                    await conn.commit()
                    return True
                else:
                    raise Exception("User not in database")

    
    async def add_website(self,url:str,user:int,notifications:json):

        
        pass

    async def add_minecraft(self, url:str, user:int, notifications:json):
       
        
        pass

    async def add_bot(self, id:int, user:int, notifications:json):
        
        pass
    
    async def __nuke(self):
        """
        Nukes the database, let's hope you know what you're doing.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        await self.applications.execute("DELETE FROM applications WHERE id != 69420123")
        await self.users.execute("DELETE FROM users WHERE id != 'admin'")
        
        # USERS
    
    async def add_subscription_to_user(self, id:int=None, name:str=None, Application:Application=None, Notification:Notification=None):
        """
        Adds the subscription to the user

        Parameters
        ----------
        id : int, optional
            The id of the user
        name : str, optional
            The name of the user
        Application : Application
            The application to add
        Notification : Notification
            The notification to add

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if Application is None or Notification is None:
            return ValueError("subscription cannot be None")

        async with self.conn.execute("SELECT * FROM users WHERE id = ? OR name = ?", (id, name)) as cursor:
            user = await cursor.fetchone()
        
        if user is None:
            raise Exception("User not in database")

        subscriptions = json.loads(user[2])
        subscriptions[Application.name].append(Notification.message)
        
        await self.conn.execute("UPDATE users SET subscriptions = ? WHERE id = ?", (json.dumps(subscriptions), user[0]))
        await self.conn.commit()

    async def remove_subscription_from_user(self, id:int=None, name:str=None, Application:Application=None, Notification:Notification=None):
        """
        Removes the subscription from the user

        Parameters
        ----------
        id : int, optional
            The id of the user
        name : str, optional
            The name of the user
        Application : Application
            The application to remove
        Notification : Notification
            The notification to remove

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if Application is None:
            return ValueError("subscription cannot be None")

        async with self.conn.execute("SELECT * FROM users WHERE id = ? OR name = ?", (id, name)) as cursor:
            user = await cursor.fetchone()
        
        if user is None:
            raise Exception("User not in database")

        subscriptions = json.loads(user[2])
        subscriptions[Application.name].remove(Notification.message)
        
        await self.conn.execute("UPDATE users SET subscriptions = ? WHERE id = ?", (json.dumps(subscriptions), user[0]))
        await self.conn.commit()

    async def update_subscription_in_user(self, id:int=None, name:str=None, Application:Application=None, Notification:Notification=None):
        """
        Updates the subscription in the user

        Parameters
        ----------
        id : int, optional
            The id of the user
        name : str, optional
            The name of the user
        Application : Application
            The application to update
        Notification : Notification
            The notification to update

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the id and name are both None
        """
        if Application is None or Notification is None:
            return ValueError("subscription cannot be None")

        async with self.conn.execute("SELECT * FROM users WHERE id = ? OR name = ?", (id, name)) as cursor:
            user = await cursor.fetchone()
        
        if user is None:
            raise Exception("User not in database")

        subscriptions = json.loads(user[2])
        subscriptions[Application.name].remove(Notification.old_message)
        subscriptions[Application.name].append(Notification.new_message)
        
        await self.conn.execute("UPDATE users SET subscriptions = ? WHERE id = ?", (json.dumps(subscriptions), user[0]))
        await self.conn.commit()

    async def get_user_subscriptions(self):
        """
        Gets the user subscriptions

        Parameters
        ----------
        None

        Returns
        -------
        list
            The list of subscriptions

        Raises
        ------
        None
        """
        subscriptions = []
        async with self.db.cursor() as cursor:
            await cursor.execute("SELECT * FROM users")
            rows = await cursor.fetchall()
            for row in rows:
                for application in row[2]:
                    for notification in application[1]:
                        subscriptions.append(Application(row[0], application[0], notification[0]))
        return subscriptions
