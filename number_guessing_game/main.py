import random

class CLI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.chances = self.set_chances(difficulty)
        self.number = self.randomNumber() 
        self.attempt = 0
        print(f'Great! You have selected the {["Easy", "Medium", "Hard"][difficulty - 1]} difficulty level.\nLet\'s start the game!')

    def set_chances(self, difficulty):
        if difficulty == 3:
            return 3
        elif difficulty == 2:
            return 5
        else:
            return 10

    def randomNumber(self):
        return random.choice(range(1, 100 + 1))

    def guess(self, answer):
        if answer == self.number:
            return Result(True, f'Congratulations! You guessed the correct number in {self.attempt + 1} attempts.')
        else:
            self.attempt += 1
            if self.attempt < self.chances:
                return Result(False, f'Incorrect! The number is {"greater" if self.number > answer else "smaller"} than {answer}.')
            else:
                return Result(None, f'You couldn\'t guess the number. The answer was {self.number}.')

class Result:
    def __init__(self, correct, message):
        self.correct = correct
        self.message = message

def main():
    print('Welcome to the Number Guessing Game! \nI\'m thinking of a number between 1 and 100. \n')
    print('Enter STOP to stop the game')
    
    while True:
        print("Please select the difficulty level:")
        print("1. Easy (10 chances)\n2. Medium (5 chances)\n3. Hard (3 chances)")
        choice = input('Enter your choice:')
        
        if choice.lower() == 'stop':
            return
        
        try:
            choice = int(choice)
            if choice not in [1, 2, 3]:
                print("Invalid choice. Please select a valid difficulty level.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number or 'stop' to exit.")
            continue

        game = CLI(choice)
        while True:
            guess = input('Enter your guess:')
            if guess.lower() == 'stop':
                return
            
            try:
                guess = int(guess)  # Convert guess to an integer
                result = game.guess(guess)
                print(result.message)
                
                if result.correct is True or result.correct is None:
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")

        print("Game over! Would you like to play again?")

if __name__ == '__main__':
    main()