from determinate import determinate
from undeterminate import undeterminate


def main():
    # path = input("Введите имя файла с грамматикой конечного автомата\n")
    # path_undeterminate = "automats/automat_systems.txt"
    # undeterminate_X = undeterminate()
    # undeterminate_X.init_by_file(path_undeterminate)
    # determinate_X = undeterminate_X.to_determinate()


    # path_determinate = "automats/auto0"

    print("Введите искомую подстроку")
    string = input()

    print("Введите путь к файлоподобному объекту")
    path = input()

    determinate_X = determinate.KMP(string)
    print(determinate_X.find_substring_file(path))

    # determinate_X = determinate.KMP("sxooxss")
    # print(determinate_X.substring("sxooxssxooxssxooxss"))

    # print(determinate_X.sf("5", "01223123445"))



    # determinate_X.init_by_file(path_determinate)
    # mini_auto = determinate_X.minimise()

    # mini_auto.print_loads()

    # undeterminate_X.print_structure()
    # determinate_X.print_structure()
    # undeterminate_X.print_loads()
    # determinate_X.print_loads()
    # print(determinate_X.check_string("1"))



if __name__ == '__main__':
    main()
