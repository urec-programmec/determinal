from os.path import exists

class getter:
    def get_automat_by_file(self, path):
        try:
            auto = open(path, 'r')
            try:
                automat = [line.strip() for line in auto]
                return self.get_automat_by_params_str(automat[0], automat[1], automat[2], automat[3], "\n".join(automat[4:]))
            except:
                raise Exception("Проверьте корректность входного файла")
        except:
            raise Exception("Путь к файлу некорректен или файла не существует")
        finally:
            auto.close()

    def get_automat_by_string(self, string):
        try:
            automat = [line.strip() for line in string.split("\n")]
            return self.get_automat_by_params_str(automat[0], automat[1], automat[2], automat[3], "\n".join(automat[4:]))
        except:
            raise Exception("Проверьте корректность входной строки")

    def get_automat_by_iterable_collections(self, iterable):
        try:
            automat = [i for i in iterable]
            return self.get_automat_by_params_collections(automat[0], automat[1], automat[2], automat[3], "\n".join(automat[4:]))
        except:
            raise Exception("Проверьте корректность входного объекта")

    def get_automat_by_iterable_str(self, iterable):
        try:
            automat = [str(i) for i in iterable]
            return self.get_automat_by_params_str(automat[0], automat[1], automat[2], automat[3], "\n".join(automat[4:]))
        except:
            raise Exception("Проверьте корректность входного объекта")

    def get_automat_by_params_collections(self, alphabet : set, states : set, startstate : str, finalstates : set, transitions : list):
        try:
            return [
                list(alphabet),
                list(states),
                str(startstate),
                list(finalstates),
                transitions if type(transitions[0]) == list else [i.split() for i in transitions]
            ]
        except:
            raise Exception("Неизвестная ошибка, проверьте корректность параметров")

    def get_automat_by_params_str(self, alphabet: str, states: str, startstate: str, finalstates: str, transitions: str):
        try:
            return [
                alphabet.split(),
                states.split(),
                str(startstate),
                finalstates.split(),
                [i.split() for i in transitions.split("\n")]
            ]
        except:
            raise Exception("Неизвестная ошибка, проверьте корректность параметров")

    def put_automat_into_file(self, automat_in_str, last_filename=""):
        i = 1
        middle = "determinate"
        pattern = last_filename if last_filename != "" else ""
        end = ".txt"
        path = self.make_filename(pattern, i, middle, end)

        while exists(path):
            i += 1
            path = self.make_filename(pattern, i, middle, end)

        try:
            with open(path, "w") as file:
                file.write(automat_in_str)
        except:
            raise Exception("Неизвестная ошибка при попытке записи автомата в файл")

        print("ok")

    def make_filename(self, pattern, num, middle, end):
        index = pattern.rfind(".")
        if index != -1 and (pattern[index:] == ".txt" or pattern[index:] == ".log"):
            return pattern[:index] + "_" + middle + "_" + str(num) + pattern[index:]
        else:
            return pattern + "_" + middle + "_" + str(num) + end
