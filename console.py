#!/usr/bin/python3
""" User this module for instance shell simulator objects
    (HBNB console)

    Classes
    -------
    HBNBCommand
"""
import cmd
import os
import pwd
import ast  # For to use literal_eval method to convert from string to dict
import re
from models import storage
from models import cls_dict


class HBNBCommand(cmd.Cmd):
    """ Allow instances of objects that inherit from Cmd
        in the cmd module and run a shell
    """
    intro = ("\033[38;2;245;97;166m*" * 25) +\
        "\n* Welcome {}\n".format(pwd.getpwuid(os.getuid()).pw_name) +\
        ("*" * 25)
    prompt = "\033[38;2;255;56;92m(hbnb)\033[0m "

    def do_create(self, line):
        """\033[38;2;132;255;161m
        Creates a new instance of BaseModel and storage in JSON file
        Usage:
        (hbnb) create <classname> // stdout: id of the instance
        """
        if line == "":
            print("** class name missing **")
        elif line not in cls_dict.keys():
            print("** class doesn't exist **")
        else:
            obj = cls_dict[line]()
            storage.save()
            print(obj.id)

    def do_show(self, line):
        """\033[38;2;132;255;161m
        Prints the string representation of an instance
        based on the class name and id
        Usage:
        (hbnb) show <classname> <id>
        """
        parts = line.split()
        cls_name = parts[0] if len(parts) > 0 else None
        id = parts[1] if len(parts) > 1 else None
        if cls_name is None:
            print("** class name missing **")
        elif cls_name not in cls_dict.keys():
            print("** class doesn't exist **")
        elif id is None:
            print("** instance id missing ** ")
        elif (cls_name + "." + id) not in list(storage.all().keys()):
            print("** no instance found **")
        else:
            print(storage.all()[cls_name + "." + id])

    def do_destroy(self, line):
        """\033[38;2;132;255;161m
        Deletes an instance based on the class name and id
        Usage:
        (hbnb) destroy <classname> <id>
        """
        parts = line.split()
        cls_name = parts[0] if len(parts) > 0 else None
        id = parts[1] if len(parts) > 1 else None
        if cls_name is None:
            print("** class name missing **")
        elif cls_name not in cls_dict.keys():
            print("** class doesn't exist **")
        elif id is None:
            print("** instance id missing ** ")
        elif (cls_name + "." + id) not in list(storage.all().keys()):
            print("** no instance found **")
        else:
            del storage.all()[cls_name + "." + id]

    def do_update(self, line):  # Refactor
        """\033[38;2;132;255;161m
        Updates an instance based on the class name and id by adding
        or updating attribute
        Usage:
        (hbnb) update <classname> <id> <attribute name> "<attribute value>"
        """
        parts = line.split()
        cls_name = parts[0] if len(parts) > 0 else None
        id = parts[1] if len(parts) > 1 else None
        attribute = parts[2] if len(parts) > 2 else None
        value = parts[3] if len(parts) > 3 else None

        if cls_name is None:
            print("** class name missing **")
        elif cls_name not in cls_dict.keys():
            print("** class doesn't exist **")
        elif id is None:
            print("** instance id missing ** ")
        elif (cls_name + "." + id) not in list(storage.all().keys()):
            print("** no instance found **")
        elif attribute is None:
            print("** attribute name missing **")
        elif value is None:
            print("** value missing **")
        else:
            setattr(storage.all()[cls_name + "." + id], attribute, value)
            storage.save()

    def do_all(self, line):
        """\033[38;2;132;255;161m
        Prints all string representation of all instances
        based or not on the class name
        Usage:
        (hbnb) all
        (hbnb) all <classname>
        """
        parts = line.split()
        cls_name = parts[0] if len(parts) > 0 else None
        if cls_name is not None and cls_name not in cls_dict.keys():
            print("** class doesn't exist **")
        else:
            if cls_name is None:
                print([str(elm) for elm in storage.all().values()])
            else:
                print([
                    str(elm) for elm in storage.all().values()
                    if elm.__class__.__name__ == cls_name
                ])

    def precmd(self, line):
        """ Format user input before executing the command, to direct them
            to already existing commands
            Parameter
            ---------
            line : str
                Input of the user from the console
        """
        if re.search('^[A-Z].*\\..*\\(.*\\)$', line):
            parts = (re.split("[.()]", line))[:-1]
            params = parts[2]
            if parts[1] == "update":
                if re.search("[\\{\\}]", params):
                    parts[1] = "d" + parts[1]
                    params = re.split(", ", params, 1)
                else:
                    params = re.split(", ", params, 2)
                if (parts[1] != "dupdate"):
                    params = list(map(lambda e: e.replace("\"", ""), params))
                params = " ".join(params)
            elif parts[1] != "all" and parts[1] != "count":
                params = params.replace("\"", "")
            line = "{} {} {}".format(parts[1], parts[0], params)
        return line

    def do_dupdate(self, line):  # Refactor
        """ pass
        """
        parts = line.split(" ", 2)
        cls_name = parts[0] if len(parts) > 0 else None
        id = parts[1].replace("\"", "") if len(parts) > 1 else None
        my_dict = ast.literal_eval(parts[2]) if len(parts) > 2 else None

        if cls_name is None:
            print("** class name missing **")
        elif cls_name not in cls_dict.keys():
            print("** class doesn't exist **")
        elif id is None:
            print("** instance id missing ** ")
        elif (cls_name + "." + id) not in list(storage.all().keys()):
            print("** no instance found **")
        elif my_dict is None:
            print("** attribute name missing **")
        else:
            for key, value in my_dict.items():
                setattr(storage.all()[cls_name + "." + id], key, value)
            storage.save()

    def do_count(self, line):
        """\033[38;2;132;255;161m
        Shows the number of instances por class
        Usage:
        (hbnb) <classname>.count()
        (hbnb) count <classname>
        """
        parts = line.split()
        if (len(parts) != 1):
            cmd.Cmd.do_help(self, "count")
        else:
            count = 0
            cls_name = parts[0]
            for value in storage.all().values():
                if value.__class__.__name__ == cls_name:
                    count += 1
            print(count)

    def do_EOF(self, line):
        """\033[38;2;132;255;161m
        Terminates the running program
        Usage:
        (hbnb) 'ctrl + D'
        """
        print()
        return True

    def do_quit(self, line):
        """\033[38;2;132;255;161m
        Quit command to exit the program
        Usage:
        (hbnb)$ quit
        """
        return True

    def do_help(self, arg):
        """\033[38;2;132;255;161m
        Help for commands
        Usage:
        (hbnb) help // List available commands
        (hbnb) help <command> // Detailed help on the command(cmd)
        """
        cmd.Cmd.do_help(self, arg)

    def emptyline(self):
        """
        Ignore empty lines
        """
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
