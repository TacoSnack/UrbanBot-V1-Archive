import discord
from discord import app_commands
import sqlite3
import math

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

con = sqlite3.connect('cities.db')
cur = con.cursor()

support_server = discord.Object(id=1039591871258820618)

@client.event
async def on_ready():
    cur.execute('CREATE TABLE IF NOT EXISTS cities (id INT PRIMARY KEY, name TEXT, happiness INT, population INT, balance INT, resources INT, crowdedness INT, traffic INT, pollution INT, res_level INT, com_level INT, ind_level INT, road_level INT, bus_level INT, park_level INT, plazas INT, bus_stations INT)')

    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='your cities grow! | /invite'))

    print(f'Logged in as {client.user}!')
    con.commit()

@tree.command(name='found', description='Found your city!')
async def found(intr: discord.Interaction, city_name: str):
    city_already_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_already_exists != None:
        await intr.response.send_message('You\'ve already created a city!')
    else:
        cur.execute('INSERT INTO cities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (intr.user.id, city_name, 1, 100, 500, 500, 0, 5, 0, 1, 1, 1, 1, 0, 0, 0, 0, ))
        await intr.response.send_message('You just created your city! Use `/city`to view it.')

        con.commit()

@tree.command(name='city', description='View your city.')
async def city(intr: discord.Interaction):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        res = cur.execute('SELECT name, happiness, population, balance, resources, crowdedness, traffic, pollution FROM cities WHERE id=?', (intr.user.id, )).fetchone()

        city_info_embed = discord.Embed(title=res[0], description='View your city\'s stats here.', color=0x73a0d0)
        city_info_embed.add_field(name='😄 Happiness:', value=res[1], inline=False)
        city_info_embed.add_field(name='🧍 Population:', value=res[2], inline=False)
        city_info_embed.add_field(name='💵 Balance:', value=res[3], inline=False)
        city_info_embed.add_field(name='🪨 Resources:', value=res[4], inline=False)
        city_info_embed.add_field(name='👨‍👩‍👧‍👦 Crowdedness:', value=res[5], inline=False)
        city_info_embed.add_field(name='🚗 Traffic:', value=res[6], inline=False)
        city_info_embed.add_field(name='🛢️ Pollution:', value=res[7], inline=False)

        await intr.response.send_message(embed=city_info_embed)
    else:
        await intr.response.send_message('You haven\'t created a city yet! Use `/found` to create one!')

@tree.command(name='support', description='Get an invite to the support server.')
async def support(intr: discord.Interaction):
    await intr.response.send_message('Join the UrbanBot support server here: https://discord.gg/XuZNNJbf4U')

@tree.command(name='invite', description='Invite the bot to your server!!!')
async def invite(intr: discord.Interaction):
    await intr.response.send_message('Invite the bot to your server here: https://discord.com/oauth2/authorize?client_id=1025198176547909693&scope=bot&permissions=274877959168 ')

@tree.command(name='help', description='Learn the basic commands and info.')
async def help(intr: discord.Interaction):
    help_embed = discord.Embed(title='Help and info', description='Join the [support server](https://discord.gg/gFGAyN5DPn) for extra help.', color=0x73a0d0)
    help_embed.add_field(name='/found [city name]', value='Found your city!', inline=False)
    help_embed.add_field(name='/city', value='View your city.', inline=False)
    help_embed.add_field(name='/collect', value='collect your daily taxes.', inline=False)
    help_embed.add_field(name='/zones, /services, /buildings, /policies', value='View your zones, services, buildings, and policies.', inline=False)
    help_embed.add_field(name='/upgrade [zone/service], /build [building], /add [policy]', value='Upgrade/build/add zones, services, buildings, and polcies.', inline=False)
    help_embed.add_field(name='/lb', value='View the top 10 cities on the leaderboard!', inline=False)

    await intr.response.send_message(embed=help_embed)

@tree.command(name='balance', description='View your balance and resources')
async def balance(intr: discord.Interaction):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        res = cur.execute('SELECT balance, resources FROM cities WHERE id=?', (intr.user.id, )).fetchone()

        await intr.response.send_message(f'You have ${res[0]} dollars and {res[1]} resources.')
    else:
        await intr.response.send_message('You haven\'t created a city yet! Use `/found` to create one!')

@tree.command(name='zones', description='View the levels of your zones.')
async def zones(intr: discord.Interaction):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        res = cur.execute('SELECT res_level, com_level, ind_level FROM cities WHERE id=?', (intr.user.id, )).fetchone()
        next_res_cost = (res[0] + 1) * 800
        next_res_resources = (res[0] + 1) * 800
        next_com_cost = (res[1] + 1) * 1000
        next_com_resources = (res[1] + 1) * 800
        next_ind_cost = (res[2] + 1) * 1000
        next_ind_resources = (res[2] + 1) * 1500

        zones_embed = discord.Embed(title='Zones', description='Every zone affects different metrics, use `/upgrade [zone]` to upgrade.', color=0x73a0d0)
        zones_embed.add_field(name=f'🏠 Residential zones (`res`): level {res[0]}', value=f'Costs ${next_res_cost} and {next_res_resources} resources.', inline=False)
        zones_embed.add_field(name=f'🏢 Commercial zones (`com`): level {res[1]}', value=f'Costs ${next_com_cost} and {next_com_resources} resources.', inline=False)
        zones_embed.add_field(name=f'🏭 Industrial zones (`ind`): level {res[2]}', value=f'Costs ${next_ind_cost} and {next_ind_resources} resources.', inline=False)

        await intr.response.send_message(embed=zones_embed)
    else:
        await intr.response.send_message('You haven\'t created a city yet! Use `/found` to create one!')

@tree.command(name='services', description='View your city services.')
async def services(intr: discord.Interaction):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        res = cur.execute('SELECT road_level, bus_level, park_level FROM cities WHERE id=?', (intr.user.id, )).fetchone()
        next_road_cost = (res[0] + 1) * 1000
        next_road_resources = (res[0] + 1) * 500
        next_bus_cost = (res[1] + 1) * 2000
        next_bus_resources = (res[1] + 1) * 1000
        next_park_cost = (res[2] + 1) * 1000
        next_park_resources = (res[2] + 1) * 800

        services_embed = discord.Embed(title='Services', description='Better services increase happiness, use `/upgrade [service]` to upgrade.', color=0x73a0d0)
        services_embed.add_field(name=f'🛣️ Road network (`roads`): level {res[0]}', value=f'Costs ${next_road_cost} and {next_road_resources} resources.', inline=False)
        services_embed.add_field(name=f'🚌 Bus network (`buses`): level {res[1]}', value=f'Costs ${next_bus_cost} and {next_bus_resources} resources.', inline=False)
        services_embed.add_field(name=f'🏞️ Parks (`parks`): level {res[2]}', value=f'Costs ${next_park_cost} and {next_park_resources} resources.', inline=False)

        await intr.response.send_message(embed=services_embed)
    else:
        await intr.response.send_message('You haven\'t created a city yet! use `/found` to create one!')

@tree.command(name='buildings', description='View buildings you can build.')
async def buildings(intr: discord.Interaction):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        res = cur.execute('SELECT plazas, bus_stations FROM cities WHERE id=?', (intr.user.id, )).fetchone()

        buildings_embed = discord.Embed(title='Buildings', description='More buildings increase happiness, use `/build [building]` to build one.', color=0x73a0d0)
        buildings_embed.add_field(name=f'⛲ Pubic plazas (`plaza`): {res[0]} built', value='Costs $2000 and 500 resources.', inline=False)
        buildings_embed.add_field(name=f'🚏 Bus stations (`station`): {res[1]} built', value='Costs $3000 and 500 resources.', inline=False)

        await intr.response.send_message(embed=buildings_embed)
    else:
        await intr.response.send_message('You haven\'t created a city yet! Use `/found` to create one!')

@tree.command(name='policies', description='View available policies for your city.')
async def policies(intr: discord.Interaction):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        await intr.response.send_message('No policies are available yet in this version.')
    else:
        await intr.response.send_message('You haven\'t created a city! Use `/found` to create one!')

@tree.command(name='upgrade', description='Upgrade a zone or service.')
async def upgrade(intr: discord.Interaction, zone_or_service: str):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        res = cur.execute('SELECT balance, resources, res_level, com_level, ind_level, road_level, bus_level, park_level FROM cities WHERE id=?', (intr.user.id, )).fetchone()

        if zone_or_service == 'res':
            if res[0] >= (res[2] + 1) * 800 and res[1] >= (res[2] + 1) * 800:
                cur.execute('UPDATE cities SET res_level=? WHERE id=?', (res[2] + 1, intr.user.id, ))
                cur.execute('UPDATE cities SET balance=?, resources=? WHERE id=?', (res[0] - ((res[2] + 1) * 800), res[1] - ((res[2] + 1) * 800), intr.user.id, ))
                await intr.response.send_message('Zone has been upgraded!')
            else:
                await intr.response.send_message('You don\'t have enough money/resources!')
        elif zone_or_service == 'com':
            if res[0] >= (res[3] + 1) * 1000 and res[1] >= (res[3] + 1) * 800:
                cur.execute('UPDATE cities SET com_level=? WHERE id=?', (res[3] + 1, intr.user.id, ))
                cur.execute('UPDATE cities SET balance=?, resources=? WHERE id=?', (res[0] - ((res[3] + 1) * 1000), res[1] - ((res[3] + 1) * 800), intr.user.id, ))
                await intr.response.send_message('Zone has been upgraded!')
            else:
                await intr.response.send_message('You don\'t have enough money/resources!')
        elif zone_or_service == 'ind':
            if res[0] >= (res[4] + 1) * 1000 and res[1] >= (res[4] + 1) * 1500:
                cur.execute('UPDATE cities SET ind_level=? WHERE id=?', (res[4]  + 1, intr.user.id, ))
                cur.execute('UPDATE cities SET balance=?, resources=? WHERE id=?', (res[0] - ((res[4] + 1) * 1000), res[1] - ((res[4] + 1) * 1500), intr.user.id, ))
                await intr.response.send_message('Zone has been upgraded!')
            else:
                await intr.response.send_message('You don\'t have enough money/resources!')
        elif zone_or_service == 'roads':
            if res[0] >= (res[5] + 1) * 1000 and res[1] >= (res[5] + 1) * 500:
                cur.execute('UPDATE cities SET road_level=? WHERE id=?', (res[5] + 1, intr.user.id, ))
                cur.execute('UPDATE cities SET balance=?, resources=? WHERE id=?', (res[0] - ((res[5] + 1) * 1000), res[1] - ((res[5] + 1) * 500), intr.user.id, ))
                await intr.response.send_message('Service has been upgraded!')
            else:
                await intr.response.send_message('You don\'t have enough money/resources!')
        elif zone_or_service == 'buses':
            if res[0] >= (res[6] + 1) * 2000 and res[1] >= (res[6] + 1) * 1000:
                cur.execute('UPDATE cities SET bus_level=? WHERE id=?', (res[6] + 1, intr.user.id, ))
                cur.execute('UPDATE cities SET balance=?, resources=? WHERE id=?', (res[0] - ((res[6] + 1) * 2000), res[1] - ((res[6] + 1) * 1000), intr.user.id, ))
                await intr.response.send_message('Service has been upgraded!')
            else:
                await intr.response.send_message('You don\'t have enough money/resources!')
        elif zone_or_service == 'parks':
            if res[0] >= (res[7] + 1) * 1000 and res[1] >= (res[7] + 1) * 800:
                cur.execute('UPDATE cities SET park_level=? WHERE id=?', (res[7] + 1, intr.user.id, ))
                cur.execute('UPDATE cities SET balance=?, resources=? WHERE id=?', (res[0] - ((res[7] + 1) * 1000), res[1] - ((res[7] + 1) * 800), intr.user.id, ))
                await intr.response.send_message('Service has been upgraded!')
            else:
                await intr.response.send_message('You don\'t have enough money/resources!')
        else:
            await intr.response.send_message('Please enter a valid zone or service to upgrade.')
        
        con.commit()
    else:
        await intr.response.send_message('You haven\'t created a city yet! Use `/found` to create one!')

@tree.command(name='build', description='Build a building.')
async def build(intr: discord.Interaction, building: str):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        res = cur.execute('SELECT balance, resources, plazas, bus_stations FROM cities WHERE id=?', (intr.user.id, )).fetchone()

        if building == 'plaza':
            if res[0] >= 2000 and res[1] >= 500:
                cur.execute('UPDATE cities SET plazas=? WHERE id=?', (res[2] + 1, intr.user.id, ))
                cur.execute('UPDATE cities SET balance=?, resources=? WHERE id=?', (res[0] - 2000, res[1] - 500, intr.user.id, ))
                await intr.response.send_message('Building has been built!')
            else:
                await intr.response.send_message('You don\'t have enough money/resources!')
        elif building == 'station':
            if res[0] >= 3000 and res[1] >= 500:
                cur.execute('UPDATE cities SET bus_stations=? WHERE id=?', (res[3] + 1, intr.user.id, ))
                cur.execute('UPDATE cities SET balance=?, resources=? WHERE id=?', (res[0] - 3000, res[1] - 500, intr.user.id, ))
                await intr.response.send_message('Building has been built!')
            else:
                intr.response.send_message('You don\'t have enough money/resources!')
        else:
            await intr.response.send_message('Please enter a valid building name.')
        
        con.commit()
    else:
        await intr.response.send_message('You haven\'t created a city yet! Use `/found` to create one!')

@tree.command(name='add', description='Add a policy in your city.')
async def add(intr: discord.Interaction):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        await intr.response.send_message('No policies are available yet in this version.')
    else:
        await intr.response.send_message('You haven\'t created a city yet! Use `/found` to create one!')

@tree.command(name='collect', description='Collect your daily taxes and refresh your city stats!')
@app_commands.checks.cooldown(1, 1800.0)
async def collect(intr: discord.Interaction):
    city_exists = cur.execute('SELECT name FROM cities WHERE id=?', (intr.user.id, )).fetchone()

    if city_exists != None:
        primary_res = cur.execute('SELECT happiness, population, balance, resources, crowdedness, traffic, pollution FROM cities WHERE id=?', (intr.user.id, )).fetchone()
        secondary_res = cur.execute('SELECT res_level, com_level, ind_level, road_level, bus_level, park_level, plazas, bus_stations FROM cities WHERE id=?', (intr.user.id, )).fetchone()
        
        new_population = math.floor(primary_res[1] + secondary_res[0] * 1000)
        new_balance = math.floor(primary_res[2] + secondary_res[1] * 150)
        new_resources = math.floor(primary_res[3] + secondary_res[2] * 150)
        new_crowdedness = math.floor((primary_res[0] * 95 - (secondary_res[5] * 20 + secondary_res[6] * 15)) / 100)
        new_traffic = math.floor((primary_res[1] * 90 - (secondary_res[3] * 6 + secondary_res[4] * 12 + secondary_res[7] * 6)) / 10000)
        new_pollution = math.floor((primary_res[2] * 110 - (secondary_res[4] * 15 + secondary_res[5] * 20)) / 1000)
        new_total_happiness = math.floor((new_population + new_balance + new_resources - new_crowdedness + new_traffic + new_pollution) / 100)

        new_city_embed = discord.Embed(title='Daily taxes collected!', description='Your city\'s stats have been updated!', color=0x73a0d0)
        new_city_embed.add_field(name='😄 Happiness:', value=new_total_happiness, inline=False)
        new_city_embed.add_field(name='🧍 Population:', value=new_population, inline=False)
        new_city_embed.add_field(name='💵 Balance:', value=new_balance, inline=False)
        new_city_embed.add_field(name='🪨 Resources:', value=new_resources, inline=False)
        new_city_embed.add_field(name='👨‍👩‍👧‍👦 Crowdedness:', value=new_crowdedness, inline=False)
        new_city_embed.add_field(name='🚗 Traffic:', value=new_traffic, inline=False)
        new_city_embed.add_field(name='🛢️ Pollution:', value=new_pollution, inline=False)

        cur.execute('UPDATE cities SET happiness=?, population=?, balance=?, resources=?, crowdedness=?, traffic=?, pollution=? WHERE id=?', (new_total_happiness, new_population, new_balance, new_resources, new_crowdedness, new_traffic, new_pollution, intr.user.id, ))
        await intr.response.send_message(embed=new_city_embed)
        con.commit()
    else:
        await intr.response.send_message('You haven\'t created a city yet! Use `/found` to create one!')

@tree.command(name='give', description='Developer use only.', guild=support_server)
async def give(intr: discord.Interaction, user: discord.Member, money_amount: int, resources_amount: int):
    res = cur.execute('SELECT balance, resources FROM cities WHERE id=?', (user.id, )).fetchone()
    new_balance = res[0] + money_amount
    new_resources = res[1] + resources_amount

    cur.execute('UPDATE cities SET balance=?, resources=? WHERE id=?', (new_balance, new_resources, user.id, ))
    await intr.response.send_message('Money/resources given to user.')
    con.commit()

@tree.command(name='lb', description='See the top 10 cities!')
async def lb(intr: discord.Interaction):
    res = cur.execute('SELECT name, happiness FROM cities ORDER BY happiness DESC').fetchmany(10)

    lb_embed = discord.Embed(title='Leaderboard', description='The leaderboard is ranked by happiness.', color=0x73a0d0)
    lb_embed.add_field(name=f'1st: {res[0][0]}', value=f'Happiness: {res[0][1]}', inline=False)
    lb_embed.add_field(name=f'2nd: {res[1][0]}', value=f'Happiness: {res[1][1]}', inline=False)
    lb_embed.add_field(name=f'3rd: {res[2][0]}', value=f'Happiness: {res[2][1]}', inline=False)
    lb_embed.add_field(name=f'4th: {res[3][0]}', value=f'Happiness: {res[3][1]}', inline=False)
    lb_embed.add_field(name=f'5th: {res[4][0]}', value=f'Happiness: {res[4][1]}', inline=False)
    lb_embed.add_field(name=f'6th: {res[5][0]}', value=f'Happiness: {res[5][1]}', inline=False)
    lb_embed.add_field(name=f'7th: {res[6][0]}', value=f'Happiness: {res[6][1]}', inline=False)
    lb_embed.add_field(name=f'8th: {res[7][0]}', value=f'Happiness: {res[7][1]}', inline=False)
    lb_embed.add_field(name=f'9th: {res[8][0]}', value=f'Happiness: {res[8][1]}', inline=False)
    lb_embed.add_field(name=f'10th: {res[9][0]}', value=f'Happiness: {res[9][1]}', inline=False)

    await intr.response.send_message(embed=lb_embed)

@tree.command(name='stats', description='View the bot\'s server and city count.')
async def stats(intr: discord.Interaction):
    city_count = cur.execute('SELECT COUNT (*) FROM cities').fetchone()

    await intr.response.send_message(f'UrbanBot is on {len(client.guilds)} servers and {city_count[0]} cities have been created!')

@tree.command(name='modname', description='Moderator use only.', guild=support_server)
async def modname(intr: discord.Interaction, city_name: str):
    cur.execute('UPDATE cities SET name=? WHERE name=?', ('Moderated Name', city_name, ))
    await intr.response.send_message('Moderated user\'s city name.')
    con.commit()

@tree.command(name='setname', description='Moderator use only.', guild=support_server)
async def setname(intr: discord.Interaction, user: discord.Member, new_city_name: str):
    cur.execute('UPDATE cities SET name=? WHERE id=?', (new_city_name, user.id, ))
    await intr.response.send_message('User\'s city name has been updated.')
    con.commit()

@tree.command(name='print_db', description='Developer use only.', guild=support_server)
async def print_db(intr: discord.Interaction):
    res = cur.execute('SELECT * FROM cities').fetchall()
    print(res)
    await intr.response.send_message('The database has been printed to the host console.')

@tree.error
async def on_app_command_error(intr: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await intr.response.send_message('You can only collect taxes once every 30 minutes!')
    else:
        await intr.response.send_message('An unknown error occured. Support server: https://discord.gg/XuZNNJbf4U', ephemeral=True)
        raise error

client.run('MTA0MTg0MjI2MDQzNTc5NjA0MA.GmlGFn.p0dG4kri8SEz-jfiwC97LhvK611AYGc4ZxLL3A')
