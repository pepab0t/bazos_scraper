import re

PATH_PATTERN = re.compile("\\s*url: https://reality\\.bazos\\.cz(.+)\n")


def main():
    with open("output.txt", "r") as file, open("visited_backup.txt", "w") as visit_file:
        for line in file:
            m = PATH_PATTERN.match(line)
            if m is None:
                continue
            visit_file.write(m.group(1) + "\n")


if __name__ == "__main__":
    main()
