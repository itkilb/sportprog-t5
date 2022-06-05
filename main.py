import discord
from discord.ext import commands
from config import settings
import requests

bot = commands.Bot(command_prefix = settings['prefix']) # Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.


@bot.command() # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def codeforce(ctx, *, arg): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.

    input = list(map(str, arg.split(',')))
    input = list(map(lambda x : x.replace(' ', ''), input))

    # get users info
    allTask = []
    usersInfo = []
    for user in input:
        response = requests.get("https://codeforces.com/api/user.status?handle=" +  user  + "&from=1")
        data = response.json()
        if (data['status'] == 'OK'):
            usersInfo.append(data['result'])
    
    # all task
    response = requests.get("https://codeforces.com/api/problemset.problems")
    allTask = response.json()['result']['problems']

    newTask = False
    for task in allTask:
        contestId = task['contestId']
        index = task['index']
        for users in usersInfo:
            if (newTask):
                newTask = False
                break
            for user in users:
                try:
                    if user['problem']['contestId'] == contestId and user['problem']['index'] == index:
                        newTask = True
                        break
                    
                except KeyError:
                    continue
                    
    await ctx.send(f'Link, {"https://codeforces.com/gym/" + str(contestId)  + "/problem/" + index}!') # Выводим сообщение с упоминанием автора, обращаясь к переменной author.

bot.run(settings['token'])


    
