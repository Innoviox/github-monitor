import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import requests
from bs4 import BeautifulSoup


client = Bot(description="A bot by rassarian#4378", command_prefix="!", pm_help=True)

commit_check_list = []
commit_memo_list = {}

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' + str(
        len(client.servers)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('Created by rassarian#4378')

    print("Loading links...")

    with open("links.txt") as f:
        for line in f.readlines():
            commit_check_list.append(line)
            commit_memo_list[line] = extract_commits(line)

    print("Loaded")

@client.command()
async def ping(*args):
    await client.say(":ping_pong: Pong!")

@client.command()
async def linkrepo(*args):
    print(args)
    _, user, repo, *__ = args[0].split("github")[1].split("/")
    if len(args) >= 2:
        branch = args[1]
    else:
        repo, *branch = repo.split("@")
        if branch == []:
            branch = "master"
    print(user, repo, branch)
    url = f"https://github.com/{user}/{repo}/commits/{branch}"
    with open("links.txt", "w") as f:
        f.write(url + "\n")
    commit_check_list.append(url) #(user, branch, repo))
    commit_memo_list[url] = extract_commits(url) #user, branch, repo)
    print(commit_memo_list[url])

async def check_commits():
    await client.wait_until_ready()
    counter = 0
    channel = discord.utils.get(client.get_all_channels(), name='github')
    while not client.is_closed:
        counter += 1
        for url in commit_check_list:
            previous = commit_memo_list[url] #[u+b+r]
            new = extract_commits(url) #(u, b, r)
            output = filter(lambda i: i not in previous, new)
            commit_memo_list[url] = new
            for commit in output:
                await client.send_message(channel, commit)
        await asyncio.sleep(10) # task runs every 60 seconds

def extract_commits(url):
    commits = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for li in soup.find_all("li", class_="commits-list-item"):
        p = li.find_all("p")[0]
        output = ' '.join(map(lambda i: i.text, p.find_all("a")))
        user = li.find_all("a", class_="commit-author")[0]
        time = user.nextSibling.nextSibling
        commits.append(output + " by " + user.text)
    return commits


client.loop.create_task(check_commits())
client.run("NDQ2NDkwMzQ3NTQ0MTE3MjQ4.Dd5yLw.uWYZ3AxpRF0nkBXuZEzsewIOvC8")