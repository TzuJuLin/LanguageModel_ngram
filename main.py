from logging import exception
from lm import LanguageModel


class LanguageModel_bot:

    

    def __init__(self):
        self.file_path = ""
        self.n = 0
        self.train_data = []
        self.model = None
        self.greeting()
    
    def write_new_file(self):
        pass
    

    def generate_text(self, num = 1, write = False):

        if write == False:
            print(self.model.generate())
            
        else:
            new_file_path = input("Please provide a file name: ")
                
            with open(new_file_path, "w") as f:

                for i in range(num):
                    new_text = self.model.generate()
                    f.write(new_text)
                    f.write('\n')
                print("Well done! Check out {}".format(new_file_path))



    def train_lm(self, n):
        print("Wait a bit...I'm working hard...")
        self.model = LanguageModel(int(n))
        self.model.train(self.train_data)

    
    def lm_functions(self):
        func_of_choice = input("I'm ready! What do you want to do now? 1)Generate a Random Text 2)Generate a certain number of texts and write it in a file ")

        if func_of_choice not in ["1", "2"]:
            print("Seems that your choice is invalid. Let's try once more!" )
            return self.lm_functions()
        elif func_of_choice == "1":
            return self.generate_text()
        elif func_of_choice == "2":
            num_of_text = input("How many texts would you like to create? ") 
            while True:
                try:
                    if int(num_of_text) > 0:
                        return self.generate_text(int(num_of_text), True)
                except ValueError:
                    print("Should input a positive integer. Try again!")
                    return self.lm_functions()

    
    def ask_for_n(self):

        n = input("What will be your 'n'? Please give me an integer: ")
        while True:
            try: 
                if int(n) < 1:
                    print("n has to be a positive integer. Try again!")
                    return self.ask_for_n()
                else:
                    self.n = n
                    self.train_lm(self.n)
                    return self.lm_functions()
            except ValueError:
                print("Should input an interger. Try again!")
                return self.ask_for_n()
        

    def read_txt(self, file_path):
        train_data = []
        while True:
            try:
                f = open(file_path, "r")
                for line in f:
                    line = line.rstrip("\n")
                    train_data.append([line]) 
                self.train_data += train_data
                return self.ask_for_n()
            except FileNotFoundError:
                print("The path cannot be found. Make sure you're providing a valid path!")
                return self.ask_for_file_path()

        
    def ask_for_file_path(self):
        ask_for_file = input("Please insert the file path of the traing text: ")
        self.file_path = ask_for_file
        return self.read_txt(ask_for_file)

        

    def greeting(self):
        
        #greet and explain the purpose 
        greet = "Hi there! I'm a n-gram language model. You can train me with a text file along with a specified 'n' by your choice. I will then be able to generate random texts base on the files you feed me! Let's get started!!"
        print(greet)
        return self.ask_for_file_path()

        
        




lm = LanguageModel_bot()





    

    