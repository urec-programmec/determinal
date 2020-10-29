from determinate import determinate
from undeterminate import undeterminate


def main():
    # path = input("Введите имя файла с грамматикой конечного автомата\n")
    path_undeterminate = "automats/auto11"
    path_determinate = "automats/auto4"

    undeterminate_X = undeterminate()
    undeterminate_X.init_by_file(path_undeterminate)

    determinate_X = undeterminate_X.to_determinate()

    # undeterminate_X.print_structure()
    # determinate_X.print_structure()

    undeterminate_X.print_loads()
    determinate_X.print_loads()

if __name__ == '__main__':
    main()
