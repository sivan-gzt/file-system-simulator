PATH_DELIMITER = '/'
INDENT_STR = lambda n: u"\u2800" * (n)

# not all terminals can display these
# COLOR_RED = "\033[91m"
# COLOR_RESET = "\033[0m"
# PREFIX_DIRECTORY = '📁'
# PREFIX_FILE = '📄'
COLOR_RED = ""
COLOR_RESET = ""
PREFIX_DIRECTORY = ''
PREFIX_FILE = ''
MAX_LENGTH_NAME = 255
ROOT = '~'
TREE_BRANCH   = "├── " 
TREE_LAST     = "└── " 
TREE_VERTICAL = "│" + u"\u2800" * 2
TREE_SPACE    = u"\u2800" * 2