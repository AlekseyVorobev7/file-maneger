import sys
import os


HELP_TEXT = """
=== File Manager — Available Commands ===

Команда	Описание
ls	Вывести содержимое текущей директории
pwd	Показать текущий путь внутри рабочей директории
cd <путь>	Сменить директорию ('..', '/', или имя папки)
mkdir <имя>	Создать директорию
rmdir <имя>	Удалить директорию (рекурсивно)
touch <имя>	Создать пустой файл
cat <имя>	Вывести содержимое файла
write <имя>	Записать текст в файл (ввод до строки END)
append <имя>	Дописать текст в конец файла (ввод до END)
rm <имя>	Удалить файл
cp <src> <dst>	Скопировать файл
mv <src> <dst>	Переместить файл или директорию
ren <old> <new>	Переименовать файл или директорию
help	Показать справку
exit / quit	Выйти из файлового менеджера

==========================================
"""


def _format_listing(entries: list[tuple[str, str]]) -> str:
    if not entries:
        return "  (empty)"
    lines = []
    for name, kind in entries:
        marker = "[DIR] " if kind == "DIR" else "[FILE]"
        lines.append(f"  {marker} {name}")
    return "\n".join(lines)


def run(navigator, file_ops) -> None:
    print("\n=== File Manager ===")
    print(f"Root: {navigator.base_dir}")
    print("Type 'help' for available commands.\n")

    while True:
        prompt = f"fm:{navigator.pwd()}> "
        try:
            raw = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not raw:
            continue

        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        try:
            if cmd in ("exit", "quit"):
                print("Goodbye!")
                break

            elif cmd == "help":
                print(HELP_TEXT)

            elif cmd == "pwd":
                print(navigator.pwd())

            elif cmd == "ls":
                entries = navigator.list_dir()
                print(_format_listing(entries))

            elif cmd == "cd":
                if not arg:
                    print("Usage: cd <path>")
                else:
                    navigator.change_dir(arg)

            elif cmd == "mkdir":
                if not arg:
                    print("Usage: mkdir <name>")
                else:
                    navigator.make_dir(arg)
                    print(f"Directory '{arg}' created.")

            elif cmd == "rmdir":
                if not arg:
                    print("Usage: rmdir <name>")
                else:
                    navigator.remove_dir(arg)
                    print(f"Directory '{arg}' removed.")

            elif cmd == "touch":
                if not arg:
                    print("Usage: touch <name>")
                else:
                    file_ops.create_file(arg)
                    print(f"File '{arg}' created.")

            elif cmd == "cat":
                if not arg:
                    print("Usage: cat <name>")
                else:
                    content = file_ops.read_file(arg)
                    print(content if content else "(empty file)")

            elif cmd == "write":
                if not arg:
                    print("Usage: write <name>")
                else:
                    print("Enter content (type END on a new line to finish):")
                    lines = []
                    while True:
                        line = input()
                        if line == "END":
                            break
                        lines.append(line)
                    file_ops.write_file(arg, "\n".join(lines))
                    print(f"File '{arg}' written.")

            elif cmd == "append":
                if not arg:
                    print("Usage: append <name>")
                else:
                    print("Enter content to append (type END on a new line to finish):")
                    lines = []
                    while True:
                        line = input()
                        if line == "END":
                            break
                        lines.append(line)
                    file_ops.append_file(arg, "\n" + "\n".join(lines))
                    print(f"Content appended to '{arg}'.")

            elif cmd == "rm":
                if not arg:
                    print("Usage: rm <name>")
                else:
                    file_ops.delete_file(arg)
                    print(f"File '{arg}' deleted.")

            elif cmd == "cp":
                args = arg.split(maxsplit=1)
                if len(args) < 2:
                    print("Usage: cp <source> <destination>")
                else:
                    file_ops.copy_file(args[0], args[1])
                    print(f"Copied '{args[0]}' → '{args[1]}'.")

            elif cmd == "mv":
                args = arg.split(maxsplit=1)
                if len(args) < 2:
                    print("Usage: mv <source> <destination>")
                else:
                    file_ops.move_file(args[0], args[1])
                    print(f"Moved '{args[0]}' → '{args[1]}'.")

            elif cmd == "ren":
                args = arg.split(maxsplit=1)
                if len(args) < 2:
                    print("Usage: ren <old_name> <new_name>")
                else:
                    file_ops.rename_file(args[0], args[1])
                    print(f"Renamed '{args[0]}' → '{args[1]}'.")

            else:
                print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")

        except (PermissionError, FileNotFoundError, FileExistsError,
                NotADirectoryError, IsADirectoryError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
