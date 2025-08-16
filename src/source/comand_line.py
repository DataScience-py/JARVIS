def parser(string: str):
    
    return string.split()

while (comand := input("Jarvis>")) != "exit":
    print(parser(comand))

