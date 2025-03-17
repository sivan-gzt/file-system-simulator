from file_system.filesystem import FileSystem

def main():
    fs = FileSystem()
    print("Welcome!")
    print("Type 'exit' to quit.")


    while True:
        command = input(f"{fs.current.name}> ").strip()
        if command.lower() == "exit":
            print("Goodbye!")
            break

        parts = command.split()
        if not parts:
            continue
        
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "ls":
            items = fs.ls()

            if items:
                print("  ".join(items))
            
        elif cmd == "mkdir":
            if arg:
                print(fs.mkdir(arg))
            else:
                print("usage: mkdir <directory_name>")
        elif cmd == "cd":
            if arg:
                print(fs.cd(arg))
            else:
                print("usage: cd <directory_name or '..'>")

        else:
            print(f"unknown command {cmd}")

if __name__ == "__main__":
    main()
