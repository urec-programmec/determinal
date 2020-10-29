import math

from getter import getter
from state import state
from determinate import determinate

class undeterminate:

    def __init__(self):
        self.alphabet = []
        self.states = []
        self.startstate = ""
        self.finalstates = []
        self.vertexs = []
        self.transitions = []

        self.filename = ""
        self.loads = ""

        self.now = []

        self.self_state_unloaded = "UNLOADED"
        self.self_state_in_progress = "IN PROGRESS"
        self.self_state_ready = "READY"

        self.ready = self.self_state_unloaded

    #region init
    def init_by_file(self, path):
        self.filename = path
        self.ready = self.self_state_in_progress
        try:
            self.translate_getting_result(getter().get_automat_by_file(path))
        except:
            self.clear()
            raise Exception("Произошла неожиданная ошибка в процессе обработки входных данных")

    def init_by_string(self, string):
        self.ready = self.self_state_in_progress
        try:
            self.translate_getting_result(getter().get_automat_by_string(string))
        except:
            self.clear()
            raise Exception("Произошла неожиданная ошибка в процессе обработки входных данных")

    def init_by_iterable_str(self, iterable):
        self.ready = self.self_state_in_progress
        try:
            self.translate_getting_result(getter().get_automat_by_iterable_str(iterable))
        except:
            self.clear()
            raise Exception("Произошла неожиданная ошибка в процессе обработки входных данных")

    def init_by_iterable_collections(self, iterable):
        self.ready = self.self_state_in_progress
        try:
            self.translate_getting_result(getter().get_automat_by_iterable_collections(iterable))
        except:
            self.clear()
            raise Exception("Произошла неожиданная ошибка в процессе обработки входных данных")

    def init_by_params_collections(self, alphabet : set, states : set, startstate : str, finalstates : set, transitions : list):
        self.ready = self.self_state_in_progress
        try:
            self.translate_getting_result(
                getter().get_automat_by_params_collections(alphabet=alphabet, states=states, startstate=startstate,
                                                         finalstates=finalstates, transitions=transitions))
        except:
            self.clear()
            raise Exception("Произошла неожиданная ошибка в процессе обработки входных данных")

    def init_by_params_str(self, alphabet: str, states: str, startstate: str, finalstates: str, transitions: str):
        self.ready = self.self_state_in_progress
        try:
            self.translate_getting_result(
                getter().get_automat_by_params_str(alphabet=alphabet, states=states, startstate=startstate,
                                                         finalstates=finalstates, transitions=transitions))
        except:
            self.clear()
            raise Exception("Произошла неожиданная ошибка в процессе обработки входных данных")
    #endregion

    def translate_getting_result(self, automat):
        if(self.ready != self.self_state_in_progress):
            raise Exception("Неверный источник данных, воспользуйтесь init методами")

        self.alphabet = automat[0]
        self.states = automat[1]
        self.startstate = automat[2]
        self.finalstates = automat[3]
        self.transitions = automat[4]

        self.check_all_parametrs()
        self.translate_transitions()

        self.now = [self.startstate].extend(self.e_childs_vertex(self.startstate))
        self.states.pop(self.states.index(self.startstate.liter))
        a = [self.startstate.liter]
        a.extend(self.states)
        self.states = a

        self.loads = self.make_str()

        self.ready = self.self_state_ready

    #region parse
    def check_all_parametrs(self):
        if (self.ready != self.self_state_in_progress):
            raise Exception("Данный метод не может быть вызван на этом этапе")

        # Проверка формата алфавита
        # - алфавит задан
        self.parse_alphabet_format()

        # Проверка формата вершин
        # - вершины заданы
        self.parse_states_format()

        # Проверка на совпадение и уникальность
        # - алфавит и вершины не пересекаются
        # - алфавит состоит из уникальных символов
        # - вершины состоят из уникальных символов
        self.parse_alphabet_states_equal()

        # Проверка начального состояния
        # - единственный знак
        # - присутствует в вершинах
        self.parse_startstate()

        # Проверка конечных состояний
        # - все присутствуют в вершинах
        self.parse_finalstates()

        # Проверка переходов
        # - проверка формата переходов
        # - проверка на присутствие в алфавите
        self.parse_transitions()

    def parse_alphabet_format(self):
        if (self.ready != self.self_state_in_progress):
            raise Exception("Данный метод не может быть вызван на этом этапе")

        if len(self.alphabet) == 0:
            raise Exception("Алфавит автомата не может быть пустым")

    def parse_states_format(self):
        if (self.ready != self.self_state_in_progress):
            raise Exception("Данный метод не может быть вызван на этом этапе")

        if len(self.states) == 0:
            raise Exception("Список вершин автомата не может быть пустым")

    def parse_alphabet_states_equal(self):
        if (self.ready != self.self_state_in_progress):
            raise Exception("Данный метод не может быть вызван на этом этапе")

        if len(self.alphabet) != len(set(self.alphabet)):
            raise Exception("Алфавит автомата содержит повторяющиеся символы")

        if len(self.states) != len(set(self.states)):
            raise Exception("Список вершин автомата содержит повторяющиеся символы")

        sings = self.alphabet.copy()
        sings.extend(self.states)

        if len(sings) != len(set(sings)):
            raise Exception("Алфавит и список вершин автомата неуникальны")

    def parse_startstate(self):
        if (self.ready != self.self_state_in_progress):
            raise Exception("Данный метод не может быть вызван на этом этапе")

        if len(self.startstate.split()) != 1:
            raise Exception("Начальное состояние автомата должно быть задано единственным символом")

        if self.startstate not in self.states:
            raise Exception("Начальное состояние автомата должно присутствовать в списке вершин автомата")

    def parse_finalstates(self):
        if (self.ready != self.self_state_in_progress):
            raise Exception("Данный метод не может быть вызван на этом этапе")

        for this_vertex in self.finalstates:
            if this_vertex not in self.states:
                raise Exception("Каждое из конечных состояний автомата должно присутствовать в списке вершин автомата")

    def parse_transitions(self):
        if (self.ready != self.self_state_in_progress):
            raise Exception("Данный метод не может быть вызван на этом этапе")

        pairs = set()
        new_transitions = []

        for this_transition in self.transitions:
            index_str = self.transitions.index(this_transition) + 5

            if len(this_transition) == 3:
                start = this_transition[0].strip()
                sign = this_transition[1].strip()
                end = this_transition[2].strip()

                if start not in self.states or end not in self.states or sign not in self.alphabet:
                    raise Exception("Синтаксическое содержание " + str(
                        index_str) + " строки (вершина -> символ -> вершина) задано неверно")

                to_set = start + " " + sign + " " + end
                check_set = set()
                check_set.add(to_set)

                if len(check_set & pairs) == 0:
                    pairs.add(to_set)
                else:
                    raise Exception("Cтрочка " + str(
                        index_str) + " нарушает принципы построения недетерминированных конечных автоматов")

            elif len(this_transition) == 2:
                start = this_transition[0].strip()
                end = this_transition[1].strip()

                if start not in self.states or end not in self.states:
                    raise Exception("Синтаксическое содержание " + str(
                        index_str) + " строки (вершина -> эпсилон -> вершина) задано неверно")

                to_set = start + " " + end
                check_set = set()
                check_set.add(to_set)

                if len(check_set & pairs) == 0:
                    pairs.add(to_set)
                else:
                    raise Exception("Cтрочка " + str(
                        index_str) + " нарушает принципы построения недетерминированных конечных автоматов")

            else:
                raise Exception("Формат переходов в " + str(index_str) + " строке задан неверно")

            new_transitions.append([i.strip() for i in this_transition])

        self.transitions = new_transitions

    def translate_transitions(self):
        if (self.ready != self.self_state_in_progress):
            raise Exception("Данный метод не может быть вызван на этом этапе")

        states = []
        for i in self.transitions:
            # [A, b, C]
            # [A, B]
            master = [j.liter for j in states]
            if i[0] not in master:
                this_state = state(i)
                states.append(this_state)
            else:
                this_state = states[[k.liter for k in states].index(i[0])]
                this_state.add_transition(i)

        for this_state in states:
            this_state_rules = this_state.symbol_to_next_state
            for rule in range(len(this_state_rules)):
                for states_ind in range(1, len(this_state_rules[rule])):
                    master = [k.liter for k in states]
                    if this_state_rules[rule][states_ind] in master:
                        this_state_rules[rule][states_ind] = states[master.index(this_state_rules[rule][states_ind])]
                    else:
                        new_state = state([this_state_rules[rule][states_ind], this_state_rules[rule][states_ind]])
                        this_state_rules[rule][states_ind] = new_state
                        states.append(new_state)

        self.vertexs = states
        self.startstate = states[[k.liter for k in self.vertexs].index(self.startstate)]
        for i in range(len(self.finalstates)):
            self.finalstates[i] = states[[k.liter for k in self.vertexs].index(self.finalstates[i])]
    #endregion

    def step_make_one(self, char):
        if (self.ready != self.self_state_ready):
            raise Exception("Автомат должен быть подготовлен")

        if len(self.now) == 0:
            self.now = [self.startstate].extend(self.e_childs_vertex(self.startstate))
            raise Exception("Нет дальнейшего перехода по данному символу")

        new_states = []
        for i in self.now:
            new_states.extend(self.x_childs_vertex(i, char))

        this_states = []

        for i in new_states:
            this_states.extend(self.e_childs_vertex(i))

        this_states.extend(new_states)

        self.now = this_states

    def step_check_now(self):
        if (self.ready != self.self_state_ready):
            raise Exception("Автомат должен быть подготовлен")

        correct = []
        for i in self.now:
            if i in self.finalstates:
                correct.append(i.liter)

        if len(correct != 0):
            return [True, correct]
        return [False, correct]

    def check_core(self, string):
        if (self.ready != self.self_state_ready):
            raise Exception("Автомат должен быть подготовлен")

        this_states = [self.startstate]
        new_states = []
        this_states.extend(self.e_childs_vertex(this_states[0]))
        is_correct = False

        for char in string:
            for i in this_states:
                new_states.extend(self.x_childs_vertex(i, char))
            this_states = []
            for i in new_states:
                this_states.extend(self.e_childs_vertex(i))

            this_states.extend(new_states)
            new_states = []

        for i in this_states:
            new_states.extend(self.e_childs_vertex(i))

        this_states.extend(new_states)

        for i in this_states:
            if i in self.finalstates:
                is_correct = True
                break

        return [is_correct, this_states]

    def check_string(self, string):
        if (self.ready != self.self_state_ready):
            raise Exception("Автомат должен быть подготовлен")

        return(self.check_core(string)[0])

    def check_system(self, string):
        if (self.ready != self.self_state_ready):
            raise Exception("Автомат должен быть подготовлен")

        result = list(set(self.check_core(string)[1]) & set(self.end))
        if len(result) == 0:
            return False
        else:
            return result[0].liter

    #region geting child
    def e_childs_vertex(self, vertex):
        this_vertex = set([vertex])
        new = set()
        prev_len = 0
        while len(this_vertex) != prev_len:
            prev_len = len(this_vertex)
            for i in this_vertex:
                new |= set(self.e_one_child_vertex(i))
            this_vertex = new
            new = set()

        return list(this_vertex)

    def e_one_child_vertex(self, vertex):
        list_vertex = []
        for stns in vertex.symbol_to_next_state:
            if stns[0] == "":
                for i in stns[1:]:
                    list_vertex.append(i)

        return list_vertex

    def x_childs_vertex(self, vertex, char):
        next_vertex = []
        for i in vertex.symbol_to_next_state:
            if i[0] == char:
                next_vertex.extend(i[1:])

        return next_vertex
    #endregion

    def print_structure(self):
        if (self.ready != self.self_state_ready):
            raise Exception("Автомат должен быть подготовлен")

        to_return = []
        A = ord('A')
        for i in self.states:
            to_return.append([i, chr(A)])
            A += 1

        vertex = [i[0] for i in to_return]
        # vertex = ["A", "B", "C", "D", "E", "F", "G", "H"]

        r = 10

        zapolnitel = "   "
        cirkle = " * "
        center = " o "

        # k = 0.8
        # h = int(2.5 * r * k) + 1 if int(2.5 * r * k) % 2 == 0 else int(2.5 * r * k)
        h = int(2.5 * r) + 1 if int(2.5 * r) % 2 == 0 else int(2.5 * r)
        w = int(2.5 * r) + 1 if int(2.5 * r) % 2 == 0 else int(2.5 * r)

        alph = []

        x = int(w / 2)
        y = int(h / 2)
        is_yet = False
        count = 360 / len(vertex)
        vertex1 = [[vertex[i], i * count, 1000, x, y] for i in range(len(vertex))]
        for i in range(h):
            alph.append([])
            for j in range(w):
                if y != i:
                    alpha = 180 - math.degrees(math.atan2((y - i), (x - j)))
                elif j < x:
                    alpha = 180
                else:
                    alpha = 0
                alph[i].append(alpha)

        for i in range(h):
            for j in range(w):
                for v in vertex1:
                    this_a = alph[i][j]
                    if v[1] == 180:
                        v[3] = x - r
                        v[4] = y
                    elif v[1] == 0:
                        v[3] = x + r
                        v[4] = y
                    elif (math.fabs(v[1] - this_a) < math.fabs(v[1] - v[2])) and\
                            (int((y - i) ** 2 + (x - j) ** 2) <= r ** 2 and not is_yet or
                             int((y - i) ** 2 + (x - j) ** 2) <= r ** 2 and int((y - i) ** 2 + (x - j - 1) ** 2) > r ** 2):
                        is_yet = True
                        v[2] = this_a
                        v[3] = j
                        v[4] = i
            is_yet = False

        string = ""
        for i in range(h):
            for j in range(w):
                o = zapolnitel
                if int((y - i) ** 2 + (x - j) ** 2) <= (r + 0) ** 2:
                    o = self.what_here(j, i, vertex1)
                for v in range(len(vertex1)):
                    if vertex1[v][4] == i and vertex1[v][3] == j:
                        o = " " + to_return[v][0] + " "
                        break
                string += o
            is_yet = False
            string += "\n"


        for i in to_return:
            print(i[0] + " ---> " + i[1])

        print(string)

    def print_loads(self):
        if (self.ready != self.self_state_ready):
            raise Exception("Автомат должен быть подготовлен")

        print(self.loads + "\n")

    def what_here(self, x, y, vertex):
        koeff = 0.17
        razdelitel = "   "
        epsilon = "~"
        delta = []
        for i in self.transitions:
            th_from = i[0]
            th_to = i[1] if len(i) == 2 else i[2]
            th_what = epsilon if len(i) == 2 else i[1]
            x_from = -1
            y_from = -1
            x_to = -1
            y_to = -1

            for j in vertex:

                if j[0] == th_from:
                    x_from = j[3]
                    y_from = j[4]
                if j[0] == th_to:
                    x_to = j[3]
                    y_to = j[4]

            if x != x_to and x != x_from and x_from != x_to:
                a1 = (y - y_to) / (x - x_to)
                a2 = (y - y_from) / (x - x_from)
                a3 = (y_to - y_from) / (x_to - x_from)
                if a3 - koeff <= a2 <= a3 + koeff and a3 - koeff <= a1 <= a3 + koeff:
                    delta.append([th_what, (math.fabs(a3 - a2) + math.fabs(a3 - a1)) / 2])
                    # return " " + th_what + " "

            if x_to == x_from and x_to - koeff <= x <= x_to + koeff:
                delta.append([th_what, math.fabs(x_to - x)])
                # return " " + th_what + " "

            if x_to == x and x_to != x_from and x_from != x:
                a1 = (y - y_from) / (x - x_from)
                a2 = (y_to - y_from) / (x_to - x_from)
                if a2 - koeff <= a1 <= a2 + koeff:
                    delta.append([th_what, math.fabs(a2 - a1)])
                    # return " " + th_what + " "

            if x_from == x and x_to != x_from and x_to != x:
                a1 = (y - y_to) / (x - x_to)
                a2 = (y_to - y_from) / (x_to - x_from)
                if a2 - koeff <= a1 <= a2 + koeff:
                    delta.append([th_what, math.fabs(a2 - a1)])
                    # return " " + th_what + " "

        # delta.append([razdelitel, 10000])

        if len(delta) == 0:
            return razdelitel

        string = " "
        for i in set([j[0] for j in delta]):
            string += i
        return string + " "
        return delta[[i[1] for i in delta].index(min([i[1] for i in delta]))][0]

    def clear(self):
        self.alphabet = []
        self.states = []
        self.startstate = ""
        self.finalstates = []
        self.vertexs = []
        self.transitions = []

        self.now = []

        self.ready = self.self_state_unloaded

    def make_str(self):
        alphabet = " ".join(self.alphabet)
        states = " ".join(self.states)
        startstate = self.startstate.liter
        finalstates = " ".join([i.liter for i in self.finalstates])

        transitions = ""
        for i in self.transitions:
            transitions += " ".join(i) + "\n"

        return alphabet + "\n" + states + "\n" + startstate + "\n" + finalstates + "\n" + transitions[:-1]


    def to_determinate(self):
        if (self.ready != self.self_state_ready):
            raise Exception("Автомат должен быть подготовлен")

        table1 = []
        for i in range(len(self.vertexs)):
            table1.append([None] * (len(self.alphabet) + 1))

        for state_x in range(len(self.vertexs)):
            for item_x in range(len(self.alphabet)):
                by_char = self.x_childs_vertex(self.vertexs[state_x], self.alphabet[item_x])
                if (len(by_char) != 0):
                    table1[state_x][item_x] = [i.liter for i in by_char]
            by_char = self.e_childs_vertex(self.vertexs[state_x])
            if len(by_char) != 0:
                q = [self.states[state_x]]
                q.extend([k.liter for k in by_char])
                table1[state_x][len(self.alphabet)] = q
            else:
                table1[state_x][len(self.alphabet)] = [self.states[state_x]]


        # DO SUDA _ OKK

        table2 = [[None] * len(self.alphabet)]
        new_vertex = [[self.states[0]]]
        state_x = 0

        while state_x != len(new_vertex):
            for item_x in range(len(self.alphabet)):
                state_before = set()
                for yet_one_this_vertex in new_vertex[state_x]:
                    index = self.states.index(yet_one_this_vertex)
                    if not (table1[index][item_x] is None):
                        for state_from_table in table1[index][item_x]:
                            state_before.add(state_from_table)
                        len_prev = -1
                        while len_prev != len(state_before):
                            len_prev = len(state_before)
                            for probegaem_po_yze_naidennim in list(state_before):
                                index = self.states.index(probegaem_po_yze_naidennim)
                                if not (table1[index][len(self.alphabet)] is None):
                                    for state_from_table in table1[index][len(self.alphabet)]:
                                        state_before.add(state_from_table)

                        is_ok_general = True
                        state_before_list = sorted(list(state_before))
                        for checking_our_array in new_vertex:
                            is_ok = False
                            for item in range(len(checking_our_array)):
                                if len(checking_our_array) != len(state_before_list) or checking_our_array[item] != state_before_list[item]:
                                    is_ok = True
                            if not is_ok:
                                is_ok_general = False

                        if is_ok_general:
                            new_vertex.append(state_before_list)
                            table2.append([None] * len(self.alphabet))

                        table2[state_x][item_x] = state_before_list

            state_x += 1

        print("Промежуточные состояния таблиц, начальная и преобразованная")
        self.print_list(table1, self.states)
        self.print_list(table2, [str(i) for i in new_vertex]) 

        alphabet = " ".join(self.alphabet)
        states = " ".join(["_".join(i) for i in new_vertex])
        startstate = "_".join(new_vertex[0])

        finalstate = []
        for zapis in new_vertex:
            if len(set(zapis) & set([i.liter for i in self.finalstates])) != 0:
                finalstate.append("_".join(zapis))
        finalstate = " ".join(finalstate)

        translation = []
        for stroka in range(len(table2)):
            for by_char in range(len(table2[stroka])):
                if not (table2[stroka][by_char] is None):
                    translation.append("_".join(new_vertex[stroka]) + " " + self.alphabet[by_char] + " " + "_".join(table2[stroka][by_char]))
        translation = "\n".join(translation)

        determinate_X = determinate()
        data = alphabet + "\n" + states + "\n" + startstate + "\n" + finalstate + "\n" + translation

        determinate_X.init_by_string(data)

        getter().put_automat_into_file(data, self.filename)

        return determinate_X

    def print_list(self, my_list, before):
        st = "\t\t" + "\t|  ".join(self.alphabet) + "\t| ~"
        print(st)
        for i in range(len(my_list)):
            st = before[i] + " \t| "
            for j in my_list[i]:
                st += "[" + " ".join(j) + "]\t| " if type(j) == list else " None\t| " if j is None else "[" + j + "]\t| "

            print(st)
        print()
