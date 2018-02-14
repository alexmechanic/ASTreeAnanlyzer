#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re
functionsList = []
noCallsFuncList = []

def FindFuncDefs(lines): # функция поиска определений всех функций / search for function definitions
    for line in lines:
        # шаблон поиска прототипа / prototype search pattern
        funcName = re.findall(r'(?<=(?<=int\s)|(?<=void\s)|(?<=string\s)|(?<=double\s)|(?<=struct\s)|(?<=float\s)|(?<=char\s)).*?(?=\s?\(.+[\n ]{)', line)
        if funcName:
            try: # удаление пробелов и указателей / removing spaces and pointers
                idx = funcName[0].index(' ') 
                funcName[0] = funcName[0][idx+1:]
                idx = funcName[0].index('*')
                funcName[0] = funcName[0][idx+1:]
                functionsList.append(funcName)       
            except:
                functionsList.append(funcName)
    functionsList.append(["none, probably prototypes"]) # группа для функций без внутренних вызовов / functions with no internal calls

def FindFuncCalls(lines): # функция поиска вызовов одних функций из других / search for internal function calls
    for _def in functionsList: # для каждой функции из списка ищем ее вызов в других функциях / for each function from list, search for its call in other functions
        currentFunc = "none, probably prototypes"
        lineIdx = 0 # запоминание номера строки / saving line number
        for line in lines:
            lineIdx+=1
        # шаблон поиска прототипа / prototype search pattern
            funcName = re.findall(r'(?<=(?<=int\s)|(?<=void\s)|(?<=string\s)|(?<=double\s)|(?<=struct\s)|(?<=float\s)|(?<=char\s)).*?(?=\s?\(.+[\n ]{)', line)
            if funcName:
                try:
                    idx = funcName[0].index(' ')
                    funcName[0] = funcName[0][idx+1:]
                    idx = funcName[0].index('*')
                    funcName[0] = funcName[0][idx+1:]
                    currentFunc = funcName[0]
                except:
                    currentFunc = funcName[0]
                continue # если в строке найден прототип функции, то она запоминается (из нее будут вызываться другие), пока не встретится новый прототип
                         # if the function prototype is found, save it until new prototype is found

            else:
                funcCall = re.findall(re.escape(_def[0]) + r'[ ]*\(', line) # ищем вызов функции (текущей из списка [_def]) / search for function call (from current [_def])
                if funcCall:
                    idx = 0
                    for _def2 in functionsList: # ищем индекс функции, из которой была вызвана найденная / get index of function that calls the current function
                        if _def2[0] == currentFunc:
                            break
                        idx+=1

                    try:
                        spaceIdx = funcCall[0].index(" ") # удаляем пробелы и '(', если они есть / remove spaces and braces if the exist
                        funcCall[0] = funcCall[0][:spaceIdx]
                    except:
                        funcCall[0] = funcCall[0][:len(funcCall[0])-1] # иначе просто удаляем '(' / else remove just braces
                    functionsList[idx].append("(" + str(lineIdx) + ") " + funcCall[0]) # дописываем вызов в список для функции, откуда вызывалась (со 2го элемента) / append call to the list it's been called from

if __name__ == "__main__":
    if len(sys.argv) > 1:
        f = open(sys.argv[1], 'r')
        lines = [line.rstrip('\n') for line in f]
        f.close()

        FindFuncDefs(lines)
        FindFuncCalls(lines)

        # итоговый список выглядит так:
        # final list representation:
        # [['func1', 'call_of_func5_from_func1', 'call_of_func2_from_func1', ...], ['func2', 'call_of_func1_from_func2', ...], ...]

        for func in functionsList: # вывод на экран / print out the list
            try:
                funcHasCalls = func[1]
                print func[0].upper() + "()"
                for call in func[1:]:
                    print "\t--> " + call + "()"
            except:
                noCallsFuncList.append(func[0].upper() + "()")
        print "[i] Functions with no internal calls:"
        print "\t" + "\n\t".join(noCallsFuncList)
    else:
        print("Please provide a filename as argument")
    
