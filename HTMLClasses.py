# -*- coding:utf-8 -*-
import sublime_plugin
import sublime
import re
import os
import threading


def debug(*args):
    to_debug = True
    if to_debug:
        print args


class GetCssClassesCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        file_path = self.view.file_name()

        directory, file_name = os.path.split(file_path)

        # testa se o arquivo terminar com .html (acho que vou ter que mudar
        # esse teste)
        if not file_name.split('.')[-1] in ('html', ):
            return True

        # path do css
        css_file = os.path.join(directory,
                                "%s.css" % (file_name.split('.')[0]))

        # cria o arquivo css se ele não for criado
        if not os.path.exists(css_file):
            open(css_file, 'a').close()

        # as classes ficarao nessa tupla
        final_classes = []

        # string regex para a classe
        # qualquer coisa que começa com classe= => class=
        # depois ' ou " => (?:\'|\")
        # depois qualquer coisa que nao seja seguido por ' ou "
        # e salve => ([^\'\"]+)
        # depois ' ou " => (?:\'|\")
        class_re_string = r'class=(?:\'|\")([^\'\"]+)(?:\'|\")'

        # cria uma regex a partir da string
        class_re = re.compile(class_re_string)

        # procuramos na view do sublime se possui alguma classe
        # retorna uma lista com as selecoes
        class_selections = self.view.find_all(class_re_string)

        # para cada seleção
        for class_sel in class_selections:
            # pega o conteudo da selecao
            html_class_atribute = self.view.substr(class_sel)

            # procura pelas classes e separa por espaço
            for cl in class_re.findall(html_class_atribute)[0].split(' '):

                # adiciona {}
                cl = '.%s {}' % cl

                # coloca no final classes, caso não tenha
                if not cl in final_classes:
                    final_classes.append(cl)

        # cria uma string das classes
        classes_string = '\n'.join(final_classes)

        # abre uma nova janela
        view = self.view.window().open_file(css_file)

        def in_thread():

            def func():
                # cria um edit, necessário para escrever na view
                # o edit serve para delimitar o control z
                edit = view.begin_edit()

                # coloca o conteudo na view
                view.insert(edit, 0, classes_string)

                # fecha a view, necessário
                view.end_edit(edit)

            sublime.set_timeout(func, 100)

        threading.Thread(target=in_thread).start()
