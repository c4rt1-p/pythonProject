import discord
from discord.ext import commands
import random
import requests
from credits import bot_token, api_key


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name="cat_fact")
async def cat_fact(ctx):
    api_url = "https://cat-fact.herokuapp.com/facts/random"
    response_cat_fact = requests.get(api_url)

    if response_cat_fact.status_code == 200:
        cat_fact = response_cat_fact.json()['text']
        await ctx.send(cat_fact)
    else:
        await ctx.send("не удалось получить факт о котах")


@bot.command()
async def generate_cat(ctx):
    url = f"https://cataas.com/cat"
    response = requests.get(url)

    if response.status_code == 200:
        with open("image.png", "wb") as file:
            file.write(response.content)

        message = f"Изображение успешно загружено"
        await ctx.send(message, file=discord.File("image.png"))
    else:
        pass
        await ctx.send(message)


@bot.command(name="dog_picture")
async def dog_picture(ctx):
    api_url = "https://random.dog/woof.json"
    response_dog = requests.get(api_url)

    if response_dog.status_code == 200:
        data = response_dog.json()
        image_url = data['url']

        await ctx.send(image_url)
    else:
        await ctx.send("Не удалось получить изображение собаки.")


@bot.command(name="animal_info")
async def animal_info(ctx, animal_name):
    api_url = f'https://api.api-ninjas.com/v1/animals?name={animal_name}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})

    if response.status_code == requests.codes.ok:
        animal_data = response.json()
        if animal_data:
            animal = animal_data[0]
            name = animal.get('name')
            locations = animal.get('locations')
            weight = animal.get('characteristics', {}).get('weight', 'Неизвестный вес')

            await ctx.send(f"Имя животного: {name}, Местоположение животного: {locations}, Вес животного: {weight}")
        else:
            await ctx.send("Информация о животном не найдена.")
    else:
        await ctx.send(f"Произошла ошибка при получении информации о животном.")


@bot.command(name="help_command")
async def help_command(ctx):
    commands_list = [f"!generate_cat - Показывает фото кота",
                     "!dog_picture - Показывает фото собаки",
                     "!animal_info <animal_name> - Показывает информацию о животном по его имени"]
    help_message = "\n".join(commands_list)

    await ctx.send(f"Список доступных команд:\n{help_message}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!'):

        await bot.process_commands(message)
    else:
        response_message = ("Я получил твое сообщение, но не понимаю его."
                            "Если хочешь могу выслать тебе либо фотку животного (кота или собаки), "
                            "а также факты обо всех животных. "
                            "Для этого напиши команду. Если ты ее не знаешь, обратись к !help_command")

        await message.channel.send(response_message)


bot.run(bot_token)