class UserInput:
    def __init__(self, text=input("Enter a command: ")):
        self.text = text

class ParseInput(UserInput):
    def __init__(self, text):
        self.text = text

    def parse_input(self, text):
        self.text = text
        self.cmd, *self.args = self.text.split()
        self.cmd = self.cmd.strip().lower()
        return self.cmd, *self.args      

user_input = UserInput()
parse = ParseInput(user_input)
command, *args = parse.parse_input(user_input.text)
print(command, *args)
