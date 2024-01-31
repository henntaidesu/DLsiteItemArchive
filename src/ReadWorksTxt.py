
def ReadWorksTxt():

    with open('works.txt', 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file]
    return lines


