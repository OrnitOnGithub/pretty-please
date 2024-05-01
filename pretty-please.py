# - Read input file
#   - command line interface
#     - read and handle parameters
#     - show help menu
# - Tokenize (split by token, special chars, etc, unify strings.)
#   - A single Token should contain enough information for error handling
#     - Its value (str)
#     - Line (int)
# - Split into instructions (everything in-between semicolons)
# - Iterate over instructions
#   - Do the funny shit
# - ERRORS:
#   - Handle errors ONLY during the runtime!!!
#   - Translate the neat error messages from Kathleen
#     - Or not lol. keep it ugly.

# for sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
def sentiment(text):
    scores = analyzer.polarity_scores(text)
    sentiment = scores['compound']
    return round(sentiment * SENTIMENT_MULTIPLIER)

from colorama import Fore, Style
import random

DEBUG                = False  # If true, extra info in terminal. Disable in prod
STRING_DELIMITER     = '"'    # Char used to delimit "strings"
INSTRUCTION_ENDER    = '!'    # Normally a semicolon
SENTIMENT_MULTIPLIER = 5

SOURCE_FILE_PATH = "test.prettyplease" # temporary -- to be provided by user later


# Load file contents to memory
with open(SOURCE_FILE_PATH, "r") as source_file:
  # get list of str, each str being a line
  code_lines = source_file.readlines();

# tokenise the text
tokenised_code_lines = []
# I will not document this algorithm because it is a copy of Kathleen's implementation in Rust
# https://github.com/OrnitOnGithub/kathleen/blob/master/src/tokenizer.rs
# For more information refer to that.
for line in code_lines:
  tokens = []
  token = ""
  is_string = False
  special_chars = [              
    '(', ')',
    '{', '}',
    '[', ']',
    '<', '>',
    '!', '|', '&',
    ',', '.', ':', ';',
    '+', '*', '/', '-', '=', '^',
  ]
  for ch in line:
    if ch == STRING_DELIMITER:
      is_string = not is_string
    else:
      if not is_string:
        if ch == ' ' or ch == '\n':
          if token != "":
            tokens.append(token)
          token = ""
        elif ch in special_chars:
          if token != "":
            tokens.append(token)
          token = ""
          tokens.append(ch)
        else:
          token += ch
      else:
        token += ch
  tokenised_code_lines.append(tokens)

if DEBUG: print(tokenised_code_lines)

# Create a linear stream of Tokens
tokens = []

# class that holds information about each token
class Token:
  def __init__(self, value, line):
    self.value = value
    self.line = line   # this will mostly be used for errors i think.
  def __str__(self):
    # Neatly display our object becuase python can't do it by itself
    return f"Token:\n  value : \"{self.value}\"\n  line  : {self.line}"  

for index_of_line, line in enumerate(tokenised_code_lines):
  for token in line:
    tokens.append(
      Token(
        token,
        index_of_line+1
      )
    )

if DEBUG:
  for token in tokens: print(token)

# positive: feeling great
# nefative: angy
interpret_mood = 0

while True:
  if DEBUG: print("mood: " + str(interpret_mood))
  # process tokens lol
  for index_of_token, token in enumerate(tokens):
    if token.value == INSTRUCTION_ENDER:
      index_of_ender = index_of_token
      break

  feels_like_it = True

  # sometimes, the compiler may feel like there is too much work to do.
  if random.randint(0,10) == 1:
    print(Fore.RED + "So much work..." + Style.RESET_ALL)
    interpret_mood -= 2

  # If the interpret is grumpy, 50% chance it won't do as told
  if interpret_mood < 0:
    if random.randint(0, 1) == 1:
      feels_like_it = False
  if tokens[0].value == '/':
    # however always read comments. so that you get to redeem yourself
    feels_like_it = True

  if feels_like_it:
    # Main loop -- we process tokens here
    # The opcode is the first token in an instruction. It defines the instruction.
    # Example: print variable1 !
    # print is the opcode, variable1 is the first argument
    opcode = tokens[0].value
    # EXAMPLE: arg1 = tokens[1].value
    match opcode:

      case "test":
        if interpret_mood < 2:
          print("I don't feel like testing right now. Maybe if you asked kindly.")
        else:
          print("TEST: test to you too!")

      case "helloworld":
        if interpret_mood < -2:
          print("Goodbye, world...")
          break
        else:
          print("Hello, World!")

      case "mkint":
        # create an integer
        # We will hold all integers in a dict
        # there will be no memory managment.
        # Actually, if the compiler is anrgy it might delete an int.
        pass

      case "/":
        # Do the funny sentiment analysis
        if DEBUG: print("encountered comment")
        data = [tokens[token] for token in range(1, index_of_ender)]
        sentence = ""
        for token in data:
          sentence += token.value + " "
        if DEBUG: print(sentence)
        feeling = sentiment(sentence)
        if DEBUG: print(feeling)
        interpret_mood += feeling
        if feeling > 0:
          print(Fore.GREEN + "That's kind of you. Thanks" + Style.RESET_ALL)
        else:
          print(Fore.RED + "That's rude." + Style.RESET_ALL)

      # If the opcode is not recognised
      case _:
        print(Fore.RED + f"ERROR at line {tokens[0].line}: unknown opcode: {opcode}. This makes me unhappy." + Style.RESET_ALL)
        interpret_mood -= 2 # make the interpret sadder

  # delete all tokens until the semicolon
  for x in range(index_of_ender+1):
    tokens.pop(0)

  # If it's joever, exit the loop
  if len(tokens) == 0:
    break
exit