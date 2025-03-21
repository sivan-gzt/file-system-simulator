from argparse import ArgumentError, ArgumentParser
from shlex import split as shlex_split
from src.file_system.filesystem import FileSystem
from src.file_system.exceptions import FileSystemError
from src.file_system.constants import COLOR_RED, COLOR_RESET

def parse_arguments(command: str = None):
    """
    Parses CLI arguments using argparse.

    Args:
        command (str, optional): The command string to parse. If None, uses sys.argv.

    Returns:
        Namespace: Parsed arguments.
    """
    parser = ArgumentParser(description="File System CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # ls command
    parser_ls = subparsers.add_parser('ls', help='List directory contents')
    parser_ls.add_argument('-R', '--recurse', action='store_true', help='Recursively list subdirectories')

    # pwd command
    parser_pwd = subparsers.add_parser('pwd', help='Print present working directory')
    parser_pwd.add_argument('-R', '--recurse', action='store_true', help='Print full path from root')

    # cd command
    parser_cd = subparsers.add_parser('cd', help='Change directory')
    parser_cd.add_argument('directory', type=str, help='Target directory')

    # del command
    parser_del = subparsers.add_parser('del', help='Delete file or directory')
    parser_del.add_argument('name', type=str, help='Name of the file or directory to delete')
    parser_del.add_argument('-R', '--recurse', action='store_true', help='Recursively delete subdirectories')

    # read command
    parser_read = subparsers.add_parser('read', help='Read file content')
    parser_read.add_argument('filename', type=str, help='Name of the file to read')

    # mkdir command
    parser_mkdir = subparsers.add_parser('mkdir', help='Create one or more directories')
    parser_mkdir.add_argument('directories', type=str, nargs='+', help='Names of the directories to create')

    # touch command
    parser_touch = subparsers.add_parser('touch', help='Create or overwrite files')
    parser_touch.add_argument(
        'files', 
        type=str, 
        nargs='+', 
        help='Names of the files to create or overwrite (must be in an existing directory)'
    )
    parser_touch.add_argument(
        '--content', 
        type=str, 
        default='',
        help='Content to write to the file (only for a single file)'
    )
    parser_touch.set_defaults(func=validate_touch_args)

    # write command
    parser_write = subparsers.add_parser('write', help='Write to an existing file')
    parser_write.add_argument(
        'file', 
        type=str, 
        help='Name of the file to write to (must already exist)'
    )
    parser_write.add_argument(
        '--content', 
        type=str, 
        required=True, 
        help='Content to write to the file'
    )
    parser_write.add_argument(
        '--overwrite', 
        action='store_true', 
        help='Overwrite the file content instead of appending'
    )

    # size command
    parser_size = subparsers.add_parser('size', help='Get the size of a file or directory')
    parser_size.add_argument(
        'name',
        type=str,
        help='Name of the file or directory to get the size of'
    )

    if command is not None:
        args = parser.parse_args(shlex_split(command))  # Use shlex.split for consistent parsing
    else:
        args = parser.parse_args()  # Use sys.argv for default behavior

    return args

def validate_touch_args(args):
    """
    Validates the arguments for the 'touch' command.

    Args:
        args: The parsed arguments.

    Raises:
        ArgumentError: If the arguments are invalid.
    """
    if len(args.files) > 1 and args.content:
        raise ArgumentError(None, "The --content option can only be used with a single file.")

def execute_command(fs: FileSystem, args):
    try:
        if args.command == 'ls':
            print(fs.ls(recurse=args.recurse))

        elif args.command == 'pwd':
            print(fs.pwd(recurse=args.recurse))

        elif args.command == 'cd':
            fs.cd(args.directory)  # No output, just execute the command

        elif args.command == 'read':
            content, _ = fs.read(args.filename)
            return content

        elif args.command == 'mkdir':
            for directory in args.directories:
                fs.mkdir(directory)  # No output, just execute the command

        elif args.command == 'touch':
            if len(args.files) > 1 and args.content:
                fs.root.raise_error(FileSystemError("The --content option can only be used with a single file."))
            for file in args.files:
                fs.touch(file, content=args.content)

        elif args.command == 'write':
            fs.write(args.file, content=args.content, overwrite=args.overwrite)

        elif args.command == 'del':
            fs.del_(args.name, recurse=args.recurse)

        elif args.command == 'size':
            print(fs.size(args.name))
            
        else:
            return False # Unknown command
    except FileSystemError as e:
        print(e) # Print the exception message
    except Exception as e:
        fs.root.raise_error(FileSystemError(f"Unknown error: {e}")) # Raise the error to the root directory
    finally:
        return True
        

def interactive_mode(fs: FileSystem, parser: ArgumentParser):
    print("Welcome to the interactive file system CLI!")
    print("Type 'exit' to quit.")

    while True:
        command = input(f"{fs.current.name}> ").strip()
        if command.lower() == "exit":
            print("Goodbye!")
            break

        if not command:
            continue

        try:
            args = parse_arguments(command)  # Use the same parsing logic as non-interactive mode
            if not execute_command(fs, args):
                print(f"Unknown or incomplete command '{command}'")
        except SystemExit:
            # argparse throws a SystemExit exception if parsing fails
            print(f"Invalid command syntax: '{command}'")
        except Exception as e:
            print(f"Error: {e}")


def main():
    fs = FileSystem()
    args = parse_arguments()

    FileSystemError.__str__ = lambda self: f"{COLOR_RED}[{self.__class__.__name__}] {self.reason}{COLOR_RESET}"

    if args.command:
        execute_command(fs, args)
    else:
        interactive_mode(fs, parse_arguments)

if __name__ == "__main__":
    main()
