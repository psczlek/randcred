#!/usr/bin/env python3


import argparse
import secrets
import string


class Color:
    colors: dict[str, str] = {
        "normal": "\x1b[0m",
        "gray": "\x1b[1;38;5;240m",
        "light_gray": "\x1b[0;37m",
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
        "pink": "\x1b[35m",
        "cyan": "\x1b[36m",
        "bold": "\x1b[1m",
    }

    @staticmethod
    def redify(msg: str) -> str:
        return Color.colorify(msg, "red")

    @staticmethod
    def greenify(msg: str) -> str:
        return Color.colorify(msg, "green")

    @staticmethod
    def blueify(msg: str) -> str:
        return Color.colorify(msg, "blue")

    @staticmethod
    def yellowify(msg: str) -> str:
        return Color.colorify(msg, "yellow")

    @staticmethod
    def grayify(msg: str) -> str:
        return Color.colorify(msg, "gray")

    @staticmethod
    def light_grayify(msg: str) -> str:
        return Color.colorify(msg, "light_gray")

    @staticmethod
    def pinkify(msg: str) -> str:
        return Color.colorify(msg, "pink")

    @staticmethod
    def cyanify(msg: str) -> str:
        return Color.colorify(msg, "cyan")

    @staticmethod
    def colorify(text: str, attrs: str) -> str:
        colors = Color.colors
        msg = [colors[attr] for attr in attrs.split() if attr in colors]
        msg.append(str(text))
        msg.append(colors["normal"])
        return "".join(msg)


class Randcred:
    def __init__(self) -> None:
        pass

    @staticmethod
    def help() -> None:
        helpmsg: list[str] = [
            "Usage:",
            "  randcred [-u <len>] [-p <len>] [-w] [-W <file>] [-n <n>]\n",
            "Options:",
            "  -h, --help                   This help message\n",
            "  -u, --unamelen <len>         Username length to use, shouldn't be less than 10",
            "  -p, --passwdlen <len>        Password length to use, shouldn't be less than 10",
            "  -w, --without-punctuation    Exclude the special characters from the password charset",
            "  -W, --write <file>           Write the result to a file instead of displaying it",
            "  -n, --pool <n>               Create <n> credentials",
            "  -l, --label <label>          An account name or some label (that doesn't work if -n/--pool is specified)"
        ]
        for line in helpmsg:
            print(line)

    def username(self, len: int) -> str:
        charset: str = string.ascii_letters
        return "".join(secrets.choice(charset) for _ in range(len))

    def password(self, len: int, punctuation: bool) -> str:
        charset: str = string.ascii_letters + string.digits if punctuation else string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(charset) for _ in range(len))

    def write_to_file(self, uname: str, passwd: str, label: str, fname: str) -> int:
        bytes_written: int = 0
        out_file: str = fname if fname else "".join(secrets.choice(string.hexdigits) for _ in range(10))
        with open(out_file, "a+") as fout:
            bytes_written += fout.write(f"{label}:\n")
            bytes_written += fout.write(f"  -- Username: {uname}\n")
            bytes_written += fout.write(f"  -- Password: {passwd}\n")
        return bytes_written


def main() -> None:
    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="randcred",
        usage=None,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    arg_parser.add_argument("-h", "--help", action="store_true", required=False)
    arg_parser.add_argument("-u", "--unamelen", type=int, default=10, required=False)
    arg_parser.add_argument("-p", "--passwdlen", type=int, default=25, required=False)
    arg_parser.add_argument("-w", "--without-punctuation", action="store_true", required=False)
    arg_parser.add_argument("-W", "--write", type=str, required=False)
    arg_parser.add_argument("-n", "--pool", type=int, default=1, required=False)
    arg_parser.add_argument("-l", "--label", type=str, required=False)
    args: argparse.Namespace = arg_parser.parse_args()
    if args.help:
        Randcred.help()
        exit(0)
    if args.unamelen < 10 or args.passwdlen < 10:
        print("Username/password length shouldn't be less than 10")
        exit(1)
    generator: Randcred = Randcred()
    try:
        if args.write:
            bytes_written: int = 0
            for i in range(args.pool):
                username: str = generator.username(args.unamelen)
                password: str = generator.password(args.passwdlen, args.without_punctuation)
                bytes_written += generator.write_to_file(username, password, ("" if args.pool > 1 else args.label), args.write)
            print(f"  + Results have been written to {Color.blueify(args.write)} ({bytes_written} bytes)")
        else:
            for i in range(args.pool):
                username: str = generator.username(args.unamelen)
                password: str = generator.password(args.passwdlen, args.without_punctuation)
                if args.pool == 1 and args.label:
                    print(f"{Color.pinkify(args.label)}:")
                print(f"  -- {Color.cyanify('Username')}: {Color.greenify(username)}")
                print(f"  -- {Color.cyanify('Password')}: {Color.colorify(password, 'green' if len(password) >= 25 else 'yellow')}")
                if args.pool > 1 and i != args.pool-1:
                    print("")
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()
