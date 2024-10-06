import discord
from discord import app_commands
from pymongo import MongoClient
import os
from mcstatus import JavaServer, BedrockServer
import socket

# database connection
cluster = MongoClient(os.environ.get("mongo"))
db = cluster["discord"]
collection = db["status"]

class Minecraft(app_commands.Group):
    """All commands related to Minecraft servers"""

    @app_commands.command(description="Check the status of a Minecraft server")
    @app_commands.describe(ip = "The IP of the server to check on")
    async def status(self, interaction: discord.Interaction,ip:str):
        """Check the status of a Minecraft server"""
        try:
            server = JavaServer.lookup(ip)
            status = server.status()
        except ConnectionRefusedError:
            await interaction.response.send_message(f"Could not connect to the server at {ip}. The connection was refused.")
            return
        except socket.timeout:
            await interaction.response.send_message(f"Connection to {ip} timed out.")
            return
        except Exception as e:
            # Log the error for debugging
            print(f"Java server error: {e}")
            try:
                server = BedrockServer.lookup(ip)
                status = server.status()
            except ConnectionRefusedError:
                await interaction.response.send_message(f"Could not connect to the server at {ip}. The connection was refused.")
                return
            except socket.timeout:
                await interaction.response.send_message(f"Connection to {ip} timed out.")
                return
            except Exception as e:
                # Log the error for debugging
                print(f"Bedrock server error: {e}")
                await interaction.response.send_message(f"The server at {ip} could not be found or is unreachable.")
                return
        await interaction.response.send_message(f"The server has {status.players.online} players and replied in {status.latency} ms")

    @app_commands.command(description="Check the latency of a Minecraft server")
    @app_commands.describe(ip="The IP of the server to check on")
    async def latency(self, interaction: discord.Interaction, ip: str):
        """Check the latency of a Minecraft server"""
        try:
            server = JavaServer.lookup(ip)
            status = server.status()
        except ConnectionRefusedError:
            await interaction.response.send_message(f"Could not connect to the server at {ip}. The connection was refused.")
            return
        except socket.timeout:
            await interaction.response.send_message(f"Connection to {ip} timed out.")
            return
        except Exception as e:
            # Log the error for debugging
            print(f"Java server error: {e}")
            try:
                server = BedrockServer.lookup(ip)
                status = server.status()
            except ConnectionRefusedError:
                await interaction.response.send_message(f"Could not connect to the server at {ip}. The connection was refused.")
                return
            except socket.timeout:
                await interaction.response.send_message(f"Connection to {ip} timed out.")
                return
            except Exception as e:
                # Log the error for debugging
                print(f"Bedrock server error: {e}")
                await interaction.response.send_message(f"The server at {ip} could not be found or is unreachable.")
                return

        await interaction.response.send_message(f"The server replied in {status.latency} ms.")