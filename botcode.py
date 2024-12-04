#Import libraries
import os, random, discord 
from dotenv import load_dotenv
from discord.ext import commands
from ec2_metadata import ec2_metadata

###########

#Import token file
load_dotenv("token.env")

#Initializing environment variable token
token = os.getenv('TOKEN')

#Initialize intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required for commands and message content handling

#Recieving EC2 metadata
region = None
availability_zone = None
ip_address = None
life_cycle = None
error_msg="no ec2 metadata :("

#exception handler to detect if we're running in ec2 or not
try:
    ip_address = ec2_metadata.public_ipv4 or ec2_metadata.private_ipv4
    region = ec2_metadata.region
    availability_zone = ec2_metadata.availability_zone
    life_cycle = ec2_metadata.instance_life_cycle
except Exception as e:
    ip_address = error_msg
    region = error_msg
    availability_zone = error_msg
    life_cycle = error_msg

#Initialize Dicord Client
jhizzler = discord.Client(intents=intents)
jhizzler = commands.Bot(command_prefix="!", intents=intents)


#This runs once everytime we start up the robot
@jhizzler.event 
async def on_ready(): 
	print("Logged in as a bot {0.user}".format(jhizzler))
	print(f'Your EC2 Data are as follows: IP Address: {ip_address}, Region: {region}, Availability Zone: {availability_zone}')

#this runs everytime a message is sent
@jhizzler.event
async def on_message(message):
    if message.author == jhizzler.user:
        return

    #Obtain details from the message
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content).lower()

    print(f'Message "{user_message}" by {username} on {channel}')

    #message handling
    if channel in ["random", "test"]:
        if user_message in ["hello", "hi"]:
            await message.channel.send(f'Hello {username}')
            return

        elif user_message == "bye":
            await message.channel.send(f'Bye {username}')
            return

        elif user_message == "tell me a joke":
            jokes = [
                "Why was 10 scared of 11. Because it was inbetween 9 and 11",
                "What does MR.Monte like to do on his free time? Be awesome.",
                "why couldn't the asian man play baseball? Because he ate the bat",
            ]
            await message.channel.send(random.choice(jokes))
            return

        elif user_message == "ip":
            await message.channel.send(f'Your public IP is {ip_address}')
            return

       
        elif user_message == "life":
            await message.channel.send(f"Master P's server has been up for {life_cycle}")
            return
        
        elif user_message == "zone":
            await message.channel.send(f'Your availability zone is {availability_zone}')
            return

        elif user_message == "tell me about my server":
            await message.channel.send(
                f'Your EC2 region is {region}, Your public IP is {ip_address}, '
                f'Your availability zone is {availability_zone}'
            )
            return

#Define command to respond to "ping"
@jhizzler.command() 
async def ping(ctx): 
    await ctx.send('Pong!') 

#hurtin
jhizzler.run(token)