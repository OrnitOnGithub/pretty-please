# DONE - Read input file
# TODO   - command line interface
# TODO     - read and handle parameters
# TODO     - show help menu
# DONE - Tokenize (split by token, special chars, etc, unify strings.)
# DONE   - A single Token should contain enough information for error handling
# DONE     - Its value (str)
# DONE     - Line (int)
# DONE - Iterate over tokens
# TODO   - Do the funny shit
# DONE   - Delete everything before the first semicolon
# DONE   - Iterate again, but over the new mutated list this time
# DONE - ERRORS:
# DONE   - Handle errors ONLY during the runtime!!!
# TODO   - Translate the neat error messages from Kathleen
# DONE     - Or not lol. keep it ugly.


import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
import random
from dataclasses import dataclass


DEBUG                = False  # If true, extra info in terminal. Disable in prod
STRING_DELIMITER     = '"'    # Char used to delimit "strings"
INSTRUCTION_ENDER    = '!'    # Normally a semicolon
SENTIMENT_MULTIPLIER = 5

# temporary -- to be provided by user later through CLI
SOURCE_FILE_PATH = "test.prettyplease"


def sentiment(text: str) -> int:
  """
  does semtiment analysis. \n
  takes a piece of text (str) as parameter and returns a value
  - positive if positive sentiment (0 to 5)
  - negative if negative sentiment (0 to -5)
  """
  scores = analyzer.polarity_scores(text)
  sentiment = scores['compound']
  return round(sentiment * SENTIMENT_MULTIPLIER)


# Load file contents to memory
with open(SOURCE_FILE_PATH, "r") as source_file:
  # get list of str, each str being a line
  code_lines = source_file.readlines();

# class that holds information about each token
class Token:
  """
  used to hold information about tokens.
  - token value (str) (the token itself, like "print" or "test idk)
  - token line (int) (the line the token is at. starts at 1, like in most code editors)
  """
  def __init__(self, value, line):
    self.value = value
    self.line = line   # this will mostly be used for errors i think.
  def __str__(self):
    # Neatly display our object becuase python can't do it by itself...
    return f"Token:\n  value : \"{self.value}\"\n  line  : {self.line}"

@dataclass
class PrettyPleaseModule:
  """
  Class used to store informatin about the module currently interpreted.
  """
  # variable that keeps track of how the interpret is "feeling"
  # positive: feeling great
  # negative: angy
  mood: int
  # public variables/functions
  # defined with `define us ... !`
  public: dict[str, object]
  # private variables/functions
  # defined with `define me ... !`
  private: dict[str, object]
  def __main__():
    "Return the default PrettyPleaseModule for module __main__."
    return PrettyPleaseModule(0, {}, {})

def tokenise(code_lines: list[str]):
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

  # now we create a linear stream of tokens using the Token class
  tokens = [Token(token, index_of_line+1)
            for index_of_line, line in enumerate(tokenised_code_lines)
            for token in line]

  if DEBUG:
    for token in tokens: print(token)
  
  return tokens

def interpret_code(code_lines: list[str], cache: PrettyPleaseModule = PrettyPleaseModule.__main__()):
  """
  Interpret a code written in pretty-please.
  Should return the value of the last interpreted expression.
  """

  # tokenise the text
  tokens = tokenise(code_lines)

  # MAIN LOOP
  # Interpretation happens here
  while True:
    if DEBUG: print("mood: " + str(cache.mood))

    # find index of instruction ender ("!")
    for index_of_token, token in enumerate(tokens):
      if token.value == INSTRUCTION_ENDER:
        index_of_ender = index_of_token
        break

    # variable that defines whether the interpret will interpret or sulk (not interpret).
    feels_like_it = True

    # sometimes, the compiler may feel like there is too much work to do.
    # so, 1/10 chance to reduce the interpret's mood
    if random.randint(0,10) == 1:
      print("\033[31mSo much work...\033[m")
      cache.mood -= 2

    # If the interpret is grumpy, 50% chance it won't do as told
    if cache.mood < 0:
      if random.randint(0, 1) == 1:
        feels_like_it = False
    
    # if the opcode is /, this is a comment. Always read comments.
    if tokens[0].value == '/':
      # always read comments. so that you get to redeem yourself
      feels_like_it = True

    if feels_like_it:
      # Main match-case -- we process tokens here
      # The opcode is the first token in an instruction. It defines the instruction.
      # Example: print variable1 !
      # print is the opcode, variable1 is the first argument
      opcode = tokens[0].value
      # EXAMPLE: arg1 = tokens[1].value
      match opcode:
        case "test":
          # the interpret needs to be relatively cheerful to test
          if cache.mood < 2:
            print("I don't feel like testing right now. Maybe if you asked kindly.")
          else:
            print("TEST: test to you too!")

        # integrated hello world
        case "helloworld":
          # if the interpret is really sad
          if cache.mood < -2:
            # it may want to kill itself
            print("Goodbye, world...")
            break # break out of interpretation loop (commit suicide)
          else:
            print("Hello, World!")

        case "repl":
          # give `cache` as argument
          # the interpreter remembers all code which happened before `repl !`
          repl(cache)

        case "mkint":
          # create an integer
          # We will hold all integers in a dict
          # there will be no memory managment.
          # Actually, if the compiler is anrgy it might delete an int.
          pass

        # if opcode is "/" this is a comment
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
          cache.mood += feeling
          if feeling > 0:
            print("\033[32mThat's kind of you. Thanks\033[0m")
          else:
            print("\033[31mThat's rude.\033[m")

        # If the opcode is not recognised
        case _:
          print(f"\033[31mERROR at line {tokens[0].line}: unknown opcode: {opcode}. This makes me unhappy.\033[m")
          cache.mood -= 2 # make the interpret sadder

    # delete all tokens until the semicolon
    for x in range(index_of_ender+1):
      tokens.pop(0)

    # If it's joever, exit the loop
    if len(tokens) == 0:
      break

def repl(cache = PrettyPleaseModule.__main__()):
  """
  Start a pretty-please REPL.
  Argument `cache` stores all variables defined in interactive session.
  """
  while -5 < cache.mood or random.random() < 0.1: # loop
    expr = input("pretty-please> ") # read
    while '!' not in expr:
      expr += input("               ")
    val = interpret_code(expr.strip().split('\n'), cache) # eval
    if val is not None:
      print(val) # print
  print("\033[31mA person as rude as you does not deserve a REPL.\033[m")
  return cache

interpret_code(code_lines)
