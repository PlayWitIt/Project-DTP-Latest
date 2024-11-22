from openai import OpenAI
import yaml
import glob
config = open("config.yml", "r")
configyaml = yaml.safe_load(config)
client = OpenAI(api_key=configyaml['OPEANI-KEY'])

filedata = []

filename = ""

list_files = []

fixed = []

for i in glob.glob("*.py"):
    list_files.append(i)
    with open(i, "r") as file:
        data = file.readlines()
    filedata.append("File Name: " + str(i) + " Contents of FIle: " + str(data))

def start_work():
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an advanced python programmer. I will give you a file list, with the file content attached. You will say, what file you want to work on first to improve/fix bugs, liek this 'main.py' You WILL ONLY RESPOND WITH THE NAME OF THE FILE, NOTHING ELSE"},
        {"role": "user", "content": str(filedata)},
    ]
    )
    message = response.choices[0].message.content

    print(message)

    with open("history.txt", "a+") as file:
        file.write("Total File Data: " + str(filedata) + "\n\n")
        file.write(message + "\n\n")
    work(message)

def continue_work(file_name):
    with open("history.txt", "r") as file:
        data = file.readlines()
    with open(file_name, "r") as file:
        contents = file.readlines()
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an advanced python programmer. I will give you a file list, with the previous file you fixed already. You will say, what file you want to work on next to improve/fix bugs, liek this 'main.py' You WILL ONLY RESPOND WITH THE NAME OF THE FILE, NOTHING ELSE"},
        {"role": "user", "content": "Chat History: " + str(data) + " Files already fixed: " + str(fixed) + " What file would you like to work on now from this list: " + str(list_files)},
    ]
    )
    message = response.choices[0].message.content
    print(message)
    work(message)

def work(file_name):
    fixed.append(file_name)
    with open("history.txt", "r") as file:
        data = file.readlines()
    with open(file_name, "r") as file:
        contents = file.readlines()
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an advanced python programmer. I will give you the chat history, on the last line is the file you will work on. That file is now open to you, and you will fix bugs, or improve it in some way. YOU WILL RESPOND WITH ONLY THE FULL FIXED CODE, NO EXTRA TEXT, NO COMNMENTARY, JUST THE CODE"},
        {"role": "user", "content": "Chat History: " + str(data) + " Current File Name: " + file_name + " File Contents: " + str(contents)},
    ]
    )
    message = response.choices[0].message.content
    print(message)
    with open(file_name, "w") as file:
        file.write(message)
    continue_work(file_name)

start_work()