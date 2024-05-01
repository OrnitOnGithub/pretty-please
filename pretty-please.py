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

DEBUG = False            # If true, extra info in terminal. Disable in prod
STRING_DELIMITER = '"'  # Char used to delimit "strings"
INSTRUCTION_ENDER = '!' # Normally a semicolon

source_file_path = "test.pp" # temporary -- to be provided by user later


# Load file contents to memory
with open(source_file_path, "r") as source_file:
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

while True:
  # process tokens lol
  for index_of_token, token in enumerate(tokens):
    if token.value == INSTRUCTION_ENDER:
      index_of_ender = index_of_token
      break
  
  # Main loop -- we process tokens here
  # The opcode is the first token in an instruction. It defines the instruction.
  # Example: print variable1 !
  # print is the opcode, variable1 is the first argument
  opcode = tokens[0].value
  # EXAMPLE: arg1 = tokens[1].value
  match opcode:

    case "test":
      print("test to you too")

    
    # If the opcode is not recognised
    case _:
      print(f"ERROR: unknown opcode: {opcode} 💀💀💀")


  # delete all tokens until the semicolon
  for x in range(index_of_ender+1):
    tokens.pop(0)

  # If it's joever, exit the loop
  if len(tokens) == 0:
    break
exit