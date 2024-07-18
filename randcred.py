#!/usr/bin/env python3


import argparse
import secrets
import string
from typing import Optional, TypeAlias


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
    def red(msg: str) -> str:
        return Color.color(msg, "red")

    @staticmethod
    def green(msg: str) -> str:
        return Color.color(msg, "green")

    @staticmethod
    def blue(msg: str) -> str:
        return Color.color(msg, "blue")

    @staticmethod
    def yellow(msg: str) -> str:
        return Color.color(msg, "yellow")

    @staticmethod
    def gray(msg: str) -> str:
        return Color.color(msg, "gray")

    @staticmethod
    def light_gray(msg: str) -> str:
        return Color.color(msg, "light_gray")

    @staticmethod
    def pink(msg: str) -> str:
        return Color.color(msg, "pink")

    @staticmethod
    def cyan(msg: str) -> str:
        return Color.color(msg, "cyan")

    @staticmethod
    def color(text: str, attrs: str) -> str:
        colors = Color.colors
        msg = [colors[attr] for attr in attrs.split() if attr in colors]
        msg.append(str(text))
        msg.append(colors["normal"])
        return "".join(msg)


def get_username(len: int = 10) -> str:
    charset = string.ascii_letters
    return "".join(secrets.choice(charset) for _ in range(len))


def get_password(len: int = 25, punctuation: bool = True) -> str:
    charset = string.ascii_letters + string.digits
    if punctuation:
        charset += string.punctuation
    return "".join(secrets.choice(charset) for _ in range(len))


def write_to_file(
        uname: str,
        passwd: str,
        label: Optional[str] = None,
        fname: Optional[str] = None,
) -> int:
    bytes_written = 0
    if fname is not None:
        out_file = fname
    else:
        out_file = "".join(secrets.choice(string.hexdigits) for _ in range(10))
    with open(out_file, "a+") as fout:
        if label is not None:
            bytes_written += fout.write(f"{label}:\n")
        bytes_written += fout.write(f"==> username: {uname}\n")
        bytes_written += fout.write(f"==> password: {passwd}\n")
        return bytes_written


AP_Namespace: TypeAlias = argparse.Namespace


def make_args() -> AP_Namespace:
    parser = argparse.ArgumentParser(prog="randcred")
    parser.add_argument(
        "-u", "--unamelen",
        help="username length to use",
        type=int,
        default=10,
        required=False,
        dest="uflag",
        metavar="<len>")
    parser.add_argument(
        "-p", "--passwdlen",
        help="password length to use (shouldn't be less than 10)",
        type=int,
        default=25,
        required=False,
        dest="pflag",
        metavar="<len>")
    parser.add_argument(
        "-w",
        "--without-punctuation",
        help="exclude the special characters from the password charset",
        action="store_false",
        required=False,
        dest="wflag")
    parser.add_argument(
        "-W", "--write",
        help="write the result to a file instead of displaying it",
        type=str,
        required=False,
        dest="Wflag",
        metavar="<file name>")
    parser.add_argument(
        "-n", "--pool",
        help="create <n> credentials",
        type=int,
        default=1,
        required=False,
        dest="nflag",
        metavar="<n>")
    parser.add_argument(
        "-l", "--label",
        help="an account name or some label (doesn't work if -n/--pool is specified)",
        type=str,
        required=False,
        dest="lflag",
        metavar="<label>")
    return parser.parse_args()


def main() -> None:
    args = make_args()
    if args.pflag < 13:
        print("password length shouldn't be less than 13")
        exit(1)
    # why would we?
    elif args.pflag > 1_000_000:
        args.pflag = 25
    try:
        if args.Wflag:
            bytes_written = 0
            for i in range(args.nflag):
                username = get_username(args.uflag)
                password = get_password(args.pflag, args.wflag)
                bytes_written += write_to_file(
                    username,
                    password,
                    ("" if args.nflag > 1 else args.lflag),
                    args.Wflag)
            print(f"==> results have been written to {Color.blue(args.Wflag)} ({bytes_written} bytes)")
        else:
            for i in range(args.nflag):
                username = get_username(args.uflag)
                password = get_password(args.pflag, args.wflag)
                if args.nflag == 1 and args.lflag:
                    print(f"{Color.pink(args.lflag)}:")
                print(f"==> {Color.cyan('username')}: {Color.yellow(username)}")
                print(f"==> {Color.cyan('password')}: {Color.yellow(password)}")
                if args.nflag > 1 and i != args.nflag-1:
                    print("")
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()
