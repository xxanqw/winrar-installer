from cli import create_argument_parser, run_cli
import platform
import sys
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    if platform.system() != "Windows":
        print("❌ Error: This application is only supported on Windows.")
        sys.exit(1)

    arch, _ = platform.architecture()
    if arch != "64bit":
        print("❌ Error: This application supports only 64-bit Windows.")
        sys.exit(1)

    if not is_admin():
        print("❌ Error: This application requires administrator privileges.")
        print("Please run your Terminal as administrator.")
        sys.exit(1)

    parser = create_argument_parser()
    args = parser.parse_args()

    args.cli = True

    run_cli(args)


if __name__ == "__main__":
    main()
