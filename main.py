from determinate import determinate
from undeterminate import undeterminate


def main():
    # path = input("Введите имя файла с грамматикой конечного автомата\n")
    # path_undeterminate = "automats/automat_systems.txt"
    # undeterminate_X = undeterminate()
    # undeterminate_X.init_by_file(path_undeterminate)
    # determinate_X = undeterminate_X.to_determinate()


    path_determinate = "automats/auto0"

    determinate_X = determinate()
    determinate_X.init_by_file(path_determinate)
    mini_auto = determinate_X.minimise()

    mini_auto.print_loads()

    # undeterminate_X.print_structure()
    # determinate_X.print_structure()
    # undeterminate_X.print_loads()
    # determinate_X.print_loads()
    # print(determinate_X.check_string("1"))



if __name__ == '__main__':
    main()
