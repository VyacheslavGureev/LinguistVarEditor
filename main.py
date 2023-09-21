import pickle
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets
from menu import Menu_Ui


class LinguisticVariable():
    def __init__(self, name, terms):
        self.name = name
        self.terms = terms


class Term():
    def __init__(self, x_left, y_left, x_middle, y_middle, x_right, y_right, name, color):
        self.name = name
        self.color = color
        self.x_left = x_left
        self.y_left = y_left
        self.x_middle = x_middle
        self.y_middle = y_middle
        self.x_right = x_right
        self.y_right = y_right


def create_lin_var(name_lv, n, names_terms, x_max):
    step = round(x_max/(n-1), 2)
    terms_dict = {}
    if n > 1:
        for i in range(1, n + 1):
            if i == 1:
                terms_dict[1] = Term(x_left=[0, 0],
                                     y_left=[1, 1],
                                     x_middle=[0, 0],
                                     y_middle=[1, 1],
                                     x_right=[0, step],
                                     y_right=[1, 0],
                                     name = names_terms[0],
                                     color=[randint(0, 255), randint(0, 255), randint(0, 255)])
            elif i == n:
                terms_dict[n] = Term(x_left=[round((n-2)*step, 2), round((n-1)*step, 2)],
                                     y_left=[0, 1],
                                     x_middle=[round((n-1)*step, 2), round((n-1)*step, 2)],
                                     y_middle=[1, 1],
                                     x_right=[round((n-1)*step, 2), round((n-1)*step, 2)],
                                     y_right=[1, 1],
                                     name = names_terms[n - 1],
                                     color=[randint(0, 255), randint(0, 255), randint(0, 255)])
            else:
                terms_dict[i] = Term(
                                x_left=[round((i-2)*step, 2), round((i-1)*step, 2)],
                                y_left=[0, 1],
                                x_middle=[round((i-1)*step, 2), round((i-1)*step, 2)],
                                y_middle=[1, 1],
                                x_right=[round((i-1)*step, 2), round(i*step, 2)],
                                y_right=[1, 0],
                                name = names_terms[i - 1],
                                color=[randint(0, 255), randint(0, 255), randint(0, 255)])
    lin_var = LinguisticVariable(name_lv, terms_dict)
    return lin_var


def check_requirements(lin_var):
    terms = lin_var.terms
    n = len(terms)
    if n == 1:
        pass
    else:
        for key in terms:
            t = terms[key]
            if t.x_middle[0] >= t.x_left[0] and t.x_middle[1] <= t.x_right[1] and t.x_middle[0] <= t.x_middle[1]:
                pass
            else:
                return "Ошибка формы терма (не правильная трапеция)"
        x_max = terms[n].x_left[1]
        p = 0
        for i in range(1, n + 1):
            if terms[i].x_right[1] > p and terms[i].x_left[0] <= p:
                p = terms[i].x_right[1]
        if p < x_max:
            return "Ошибка полноты покрытия"
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                if terms[i].x_middle[1] < terms[j].x_middle[0] or terms[j].x_middle[1] < terms[i].x_middle[0]:
                    pass
                else:
                    return "Ошибка несовместимости максимумов"
    return "Ошибок нет"


def save_lin_variable(lin_var):
    name = lin_var.name
    with open(f"linguistic_variables/{name}.pkl", "wb") as f:
        pickle.dump(lin_var, f)


def load_lin_variable(filename):
    if len(filename) > 0:
        with open(filename, "rb") as f:
            lin_var = pickle.load(f)
        return lin_var
    return None


def init_ui(lin_var, n, x_max, window):
    window.tableView.setRowCount(n)
    window.tableView.setColumnCount(4)
    window.report.setText(check_requirements(lin_var))
    window.draw_lin_var(lin_var)
    window.fill_table(lin_var)
    window.maxXLineEdit.setText(str(x_max))

    window.lin_var = lin_var
    window.x_max = x_max


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    menu_window = QtWidgets.QMainWindow()
    menu_ui = Menu_Ui()
    menu_ui.setupUi(menu_window)
    menu_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()