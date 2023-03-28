import random
from flask import Flask, render_template, request

app = Flask(__name__)

# List of words for the game
words = ['python', 'java', 'ruby', 'javascript', 'html', 'css', 'react', 'angular', 'vue', 'django']

# Function to choose a random word from the list of words
def choose_word():
    return random.choice(words)

# Function to initialize the game state
def initialize_game():
    word = choose_word()
    hidden_word = ['_' for _ in word]
    guesses = []
    wrong_guesses = 0
    correct_guesses = 0
    max_wrong_guesses = 6
    return word, hidden_word, guesses, wrong_guesses, correct_guesses, max_wrong_guesses

# Function to process a guess
def process_guess(guess, word, hidden_word, guesses, wrong_guesses, correct_guesses, max_wrong_guesses):
    if guess in guesses:
        return False, hidden_word, guesses, wrong_guesses, correct_guesses
    guesses.append(guess)
    if guess in word:
        for i in range(len(word)):
            if word[i] == guess:
                hidden_word[i] = guess
        correct_guesses += 1
        return True, hidden_word, guesses, wrong_guesses, correct_guesses
    else:
        wrong_guesses += 1
        return False, hidden_word, guesses, wrong_guesses, correct_guesses


# Function to process a guess
def process_guess(guess, word, hidden_word, guesses, wrong_guesses, max_wrong_guesses):
    if guess in guesses:
        return False, hidden_word, guesses, wrong_guesses
    guesses.append(guess)
    if guess in word:
        for i in range(len(word)):
            if word[i] == guess:
                hidden_word[i] = guess
        return True, hidden_word, guesses, wrong_guesses
    else:
        wrong_guesses += 1
        return False, hidden_word, guesses, wrong_guesses

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for starting a new game
@app.route('/new_game')
def new_game():
    word, hidden_word, guesses, wrong_guesses, correct_guesses, max_wrong_guesses = initialize_game()
    return render_template('game.html', hidden_word=' '.join(hidden_word), guesses=', '.join(guesses), wrong_guesses=wrong_guesses, correct_guesses=correct_guesses, max_wrong_guesses=max_wrong_guesses, word=word)

    

# Route for processing a guess
@app.route('/guess', methods=['POST'])
def guess():                   
    guess = request.form['guess']
    word = request.form['word']
    hidden_word = request.form['hidden_word'].split()
    guesses = request.form['guesses'].split(',')
    wrong_guesses = int(request.form['wrong_guesses'])
    max_wrong_guesses = int(request.form['max_wrong_guesses'])
    result, hidden_word, guesses, wrong_guesses = process_guess(guess, word, hidden_word, guesses, wrong_guesses, max_wrong_guesses)
    if '_' not in hidden_word:
        return render_template('win.html', word=word)
    elif wrong_guesses == max_wrong_guesses:
        return render_template('lose.html', word=word)
    else:
        return render_template('game.html', hidden_word=' '.join(hidden_word), guesses=', '.join(guesses), wrong_guesses=wrong_guesses, max_wrong_guesses=max_wrong_guesses, word=word)

if __name__ == '__main__':
    app.run(debug=True)