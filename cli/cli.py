import sys

def handle_args() -> str:
  """
  handles command line arguments, shows help menu, starts repl
  """
  main_arg = sys.argv[1] # <arg>
  
  if main_arg == "help":
    with open("cli/helpmenu.txt", "r") as help_menu:
      print(help_menu.read())
    sys.exit()

  if main_arg == "repl":
    return "cli/repl.prettyplease" # a script that simply starts the repl

  file_path = main_arg
  return file_path