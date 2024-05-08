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
import os
from dataclasses import dataclass


DEBUG                = False  # If true, extra info in terminal. Disable in prod
STRING_DELIMITER     = '"'    # Char used to delimit "strings"
INSTRUCTION_ENDER    = '!'    # Normally a semicolon
SENTIMENT_MULTIPLIER = 5

# temporary -- to be provided by user later through CLI
SOURCE_FILE_PATH = "startup.prettyplease"


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
  # name:(type, value)
  public: dict[str, object]
  # private variables/functions
  # defined with `define me ... !`
  private: dict[str, object]
  def __main__():
    "Return the default PrettyPleaseModule for module __main__."
    return PrettyPleaseModule(0, {}, {})
  def is_defined(self, sym: str):
    if not isinstance(sym, str):
      return True # sym is a literal.
    if sym.isdigit():
      return True # literal int
    return sym in self.public or sym in self.private
  def get_variable(self, sym: str):
    # literal
    if not isinstance(sym, str):
      return sym
    if sym.isdigit():
      self.private[sym] = int(sym) # literal int.
      # can be garbage collected like any other variable.
      # After all, it is only a convention to call "2" the number of elements in a boolean set.
      # Might as well just call it L.

    if sym in self.public:
      return self.public[sym]
    elif sym in self.private:
      return self.private[sym]
  def define_var(self, tokens: list[Token]):
    """
    Used by interpreter when opcode is `define`.
    Define a variable or a function in the module.
    """
    # Syntax:
    # `define me <...> !` private variable
    # `define us <...> !` public variable
    # There's no module yet so this is useless.
    # `define me a variable x = 3 !` single literal
    # `define me some variables x y z = 1 2 3 respectively !` multiple literals
    # `define me a function f returning <opcode> <...> !`
    tokenl = len(tokens)
    if tokenl < 6:
      print(f"\033[31mERROR at line {tokens[0].line}: invalid define syntax. This makes me unhappy.\033[m")
      self.mood -= 2
      return
    if not (public := tokens[1].value == "us")\
        and tokens[1].value != "me":
      print(f"\033[31mERROR at line {tokens[1].line}: expected to define for `me` or `us`, got `{tokens[1].value}`."
            + " This makes me unhappy.\033[m")
      self.mood -= len(tokens[1].value) # len because why not? That's more stuff to print in the error.
      return
    if not tokens[2].value in ("a",):
      print(f"\033[31mERROR at line {tokens[2].line}: expected to define `a` or `some` (not implemented) symbol(s), got `{tokens[2].value}`."
            + "This make me unhappy\033[m")
      self.mood -= len(tokens[1].value)
      return
    # `define me some ... !` not implemented yet
    if (deftype := tokens[3].value) == "variable":
      if tokenl != 7 or\
        tokens[5].value != "=":
        print(f"\033[31mERROR: If you ask for the definition of one variable, "
              + f"then do *define* one and only *one* variable. (at line {tokens[3].line}).\033[m")
        self.mood -= 2
        return 
      symbol = tokens[4].value
      try:
        value = int(tokens[6].value)
      except:
        print(f"\033[31mERROR at line {tokens[6].line}: variables can only take integer values.\033[m")
        self.mood -= 2
        return
      # no variable shadowing, that would be a form of memory management, and this is impure.
      if self.is_defined(symbol) and\
         self.get_variable(symbol) != value: # if it has the same value, then the programmer is just saying x = x, which is not an error.
        print(f"\033[031mERROR at line {tokens[6].line}: trying to define {symbol} with value {value} when {symbol} = {self.get_variable(symbol)}.\033[m")
        self.mood -= 3 # trying to violate purity is a crime against sanity and hence deserves -3 of mood.
        return
      if public:
        self.public[symbol] = value
      else:
        self.private[symbol] = value
      return value
    elif deftype == "function":
      # define a function as such:
      # `define <me/us> a function <name> = <opcode> <...> !`
      symbol = tokens[4].value
      if tokens[5].value != "returning":
        print(f"\033[31mERROR at line {tokens[5].line}: function {symbol} is not `returning` anything. This makes me unhappy.\033[m")
        self.mood -= 2
        return
      if self.is_defined(symbol):
        print(f"\033[31mERROR at line {tokens[4].line}: trying to define a function {symbol} but {symbol} is already defined. This makes me unhappy.\033[m")
        self.mood -= 2
        return
      f = (*tokens[6:],)
      if public:
        self.public[symbol] = f
      else:
        self.private[symbol] = f
      

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

  ret = None # last expression evaluated (returned for functions/REPL)
  # MAIN LOOP
  # Interpretation happens here
  while len(tokens) != 0:
    if DEBUG: print("mood: " + str(cache.mood))

    # find index of instruction ender ("!")
    for index_of_token, token in enumerate(tokens):
      if token.value == INSTRUCTION_ENDER:
        index_of_ender = index_of_token
        break

    # variable that defines whether the interpret will interpret or sulk (not interpret).
    feels_like_it = True

    token_values = [token.value for token in tokens[1:index_of_token]]
    if (semicolon_count := token_values.count(';')) != 0:
      # semicolons are used instead of parenthesis to enclose sub-expressions.
        # e.g. `opcode1 arg1 ; opcode2 arg2 ; arg3 !` first evaluates `opcode2 arg2 !`,
        # get its value `val` and replace it in `opcode arg1 val arg3 !`
      # as there is no open- and close- semicolons, one can never next sub-expressions.
        # e.g. `opcode ; opcode2 arg1 ; opcode3 arg2 ; arg3 !`
        # evaluates `opcode2 arg1 !` replace its value, then `opcode3 arg2` and replace its value. 
      # anyway everybody hates nesting,
      # so that way the programmer is *forced* to wrap nested expressions into functions,
      # and just like that you get yourself a functional programming language.

      # one semicolon is not enough to enclose an expression.
      if semicolon_count == 1:
        print(f"\033[31mERROR: at line {tokens}")
        feels_like_it = False # what do you want to do with such a code.
      # TODO: finish semicolon nesting.

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
          sentence = " ".join(token.value for token in data)
          if DEBUG: print(f"{sentence=!r}")
          feeling = sentiment(sentence)
          if DEBUG: print(f"{feeling=}")
          cache.mood += feeling
          if abs(feeling) > SENTIMENT_MULTIPLIER // 2 + 1:
            emphasis = random.choice([" very ", " truly ", " so "])
          else:
            emphasis = " "
          if feeling > 0:
            print(f"\033[32mThat's{emphasis}kind of you. Thanks.\033[0m")
          elif feeling < 0:
            print(f"\033[31mThat's{emphasis}rude.\033[m")
          else: # feeling == 0
            print("\033[33mWhy would you even comment that?\033[0m")

        case "sum":
          to_sum = [token.value for token in tokens[1:index_of_ender]]
          for sym in to_sum:
            if not cache.is_defined(sym):
              print(f"\033[31mERROR at line {tokens[0].line}: {sym} is not defined. This makes me unhappy.\033[m")
              cache.mood -= 2
              to_sum.clear()
          ret = sum(cache.get_variable(sym) for sym in to_sum)
        
        case "product":
          to_reduce = [token.value for token in tokens[1:index_of_ender]]
          for sym in to_reduce:
            if not cache.is_defined(sym):
              print(f"\033[31mERROR at line {tokens[0].line}: {sym} is not defined. This makes me unhappy.\033[m")
              cache.mood -= 2
              to_reduce.clear()
          ret = 1
          for sym in to_reduce:
            ret *= cache.get_variable(sym)
        
        case "and":
          to_reduce = [token.value for token in tokens[1:index_of_ender]]
          for sym in to_reduce:
            if not cache.is_defined(sym):
              print(f"\033[31mERROR at line {tokens[0].line}: {sym} is not defined. This makes me unhappy.\033[m")
              cache.mood -= 2
              to_reduce.clear()
          ret = cache.get_variable(to_reduce.pop())
          for sym in to_reduce:
            ret &= cache.get_variable(sym)
        
        case "or":
          to_reduce = [token.value for token in tokens[1:index_of_ender]]
          for sym in to_reduce:
            if not cache.is_defined(sym):
              print(f"\033[31mERROR at line {tokens[0].line}: {sym} is not defined. This makes me unhappy.\033[m")
              cache.mood -= 2
              to_reduce.clear()
          ret = 0
          for sym in to_reduce:
            ret |= cache.get_variable(sym)
        
        case "exclusive or":
          to_reduce = [token.value for token in tokens[1:index_of_ender]]
          for sym in to_reduce:
            if not cache.is_defined(sym):
              print(f"\033[31mERROR at line {tokens[0].line}: {sym} is not defined. This makes me unhappy.\033[m")
              cache.mood -= 2
              to_reduce.clear()
          ret = 0
          for sym in to_reduce:
            ret ^= cache.get_variable(sym)

        case "define":
          ret = cache.define_var(tokens[:index_of_ender])
        
        # requires quotes.
        case "give up":
          break

        # allow to run abitrary .prettyplease file.
        # e.g. `run my_file.prettyplease !`
        # Note: must still be written in startup.prettyplease
        # Otherwise it would be actually useful.
        case "run":
          filename: str = "".join(token.value for token in tokens[1:index_of_ender])
          if not filename.endswith(".prettyplease"):
            # the interpreter is sad when the wrong file extension is used.
            print(f"\033[31m{filename} has the wrong file extension. This makes me unhappy.\033[m")
            cache.mood -= 2
          # run the file anway, even if the extension is wrong.
          try:
            with open(filename, "r") as io:
              code_lines = io.readlines()
            # reuse cache: run the file in the same scope (use import for modules).
            interpret_code(code_lines, cache)
          # the file probably doesn't exist
          except Exception:
            print(f"\033[31mERROR at line {tokens[0].line}: file {filename} doesn't exist. This makes me unhappy.\033[m")

        # import a library from ./lib/
        case "import":
          if index_of_ender < 2:
            print(f"\033[31mERROR at line {tokens[0].line}: incomplete import.")
          else:
            filename = tokens[1].value + ".prettyplease"
            filename = os.path.join(os.path.dirname(__file__), "lib", filename)
          try:
            with open(filename, "r") as io:
              code_lines = io.readlines()
            module = PrettyPleaseModule.__main__()
            interpret_code(code_lines, module)

            if module.mood < -SENTIMENT_MULTIPLIER//2:
              print("\033[31mThat module is very rude. This makes me unhappy.\033[m")
            elif module.mood > SENTIMENT_MULTIPLIER//2:
              print("\033[32mSuch a sweet module.\033[m")
            # module may not have been written by the same person.
            # hence the interpreter is a little bit more forgiving.
            cache.mood += module.mood//2

            # module is too rude to be imported.
            if module.mood > -SENTIMENT_MULTIPLIER:
              cache.public.update(module.public)
          # the file probably doesn't exist
          except Exception:
            print(f"\033[31mERROR at line {tokens[0].line}: file {filename} doesn't exist. This makes me unhappy.\033[m") 

        # if the opcode is not builtin
        case _:
          if not cache.is_defined(opcode):
            print(f"\033[31mERROR at line {tokens[0].line}: unknown opcode: {opcode}. This makes me unhappy.\033[m")
            cache.mood -= 2 # make the interpret sadder
          f = cache.get_variable(opcode)
          if isinstance(f, tuple):
            # f is a function
            # function arguments are refered as \0 \1 \2 and so on
            # if too much arguments are given: ignore them.
            # if too little are given: error for now (TODO: currying?)
            args = tokens[1:index_of_ender]
            args = [
              args[int(token.value[1:])] if isinstance(token.value, str) and token.value.startswith("\\") and token.value[1:].isdigit()
              else token # note: error gives line of the function. Feature not bug.
              for token in f
            ]
            tokens[0:index_of_ender] = args

          else:
            # f is a variable (will raise an error)
            tokens[0] = Token(f, tokens[0].line)

          continue # interpret the changed code.

    # delete all tokens until the semicolon
    for x in range(index_of_ender+1):
      del tokens[0]
    
    # anger collection (delete variables when unhappy)
    if cache.mood < -SENTIMENT_MULTIPLIER and random.random() < 0.25:
      print("\033[31mI can be rude as well and delete all defined variables.\033[m")
      cache.public.clear()
      cache.private.clear()
      # destroying variables make calm the interpreter down
      # (avoids deleting multiple time in a row)
      cache.mood = 0
    if cache.mood < 0 and random.random() < -cache.mood/SENTIMENT_MULTIPLIER\
       and ((publicl := len(cache.public)) != 0
       or  (privatel := len(cache.private))!= 0):
      # all variables are as likely to be deleted.
      # if there is 9 public and 1 private,
      # 10% that the private is deleted.
      if random.random() < publicl/(publicl + privatel):
        # delete a random public variable.
        sym = random.choice([*cache.public.keys()])
        del cache.public[sym]
      else:
        # delete a private variable.
        sym = random.choice([*cache.private.keys()])
        del cache.private[sym]
      print(f"\033[31mI can be rude as well and forget the value of {sym}.\033[m")
      # destroying variables relaxes the interpreter
      # (avoids deleting multiple time in a row)
      cache.mood += 1

  return ret # last expression evaluated.

def repl(cache = PrettyPleaseModule.__main__()):
  """
  Start a pretty-please REPL.
  Argument `cache` stores all variables defined in interactive session.
  """
  while -2*SENTIMENT_MULTIPLIER < cache.mood or random.random() < cache.mood/SENTIMENT_MULTIPLIER + 3.0: # loop
    expr = input("pretty-please> ") # read
    while '!' not in expr:
      expr += input("               ")
    val = interpret_code(expr.strip().split('\n'), cache) # eval
    if val is not None:
      print(val) # print
  print("\033[31mA person as rude as you does not deserve a REPL.\033[m")
  return cache

interpret_code(code_lines)
