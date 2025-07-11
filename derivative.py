#might need to put main below differentiate
#collects string to be differentiated
from collections import defaultdict
from math import isclose
def main():
    original_string = input("Input: ")
    plus_index = plus_index_calc(original_string)
    minus_index = minus_index_calc(original_string)
    divide_index = divide_index_calc(original_string)
    exponent_index = exponent_index_calc(original_string)
    derivitive = differentiate(original_string, plus_index, minus_index, divide_index, exponent_index)
    print(f"Derivitive: {derivitive}")

#checks if a string is a real number
def check_real(string):
    try:
        float(string)
        return True
    except:
        return False

#checks if a string is an integer: only for formating
def check_int(string):
    try:
        int(string)
        return True
    except:
        return False
#finds the index of the next ')' given a string and a starting index, useful for isolating functions
def next_paren(string, start_index):
    for i in range(len(string) - start_index):
        if  string[start_index + i] == ')':
            return i + start_index


def plus_index_calc(string):
    plus_index = defaultdict(list)
    a = 0
    for i in range(len(string)):
        if string[i] == '(':
            a += 1
        elif string[i] == ')':
            a -= 1
        elif string[i] == '+':
            for d in range(a, -1, -1):
                plus_index[d].append(i)
    return plus_index


def minus_index_calc(string):
    minus_index = defaultdict(list)
    a = 0
    for i in range(len(string)):
        if string[i] == '(':
            a += 1
        elif string[i] == ')':
            a -= 1
        elif string[i] == '-':
            for d in range(a, -1, -1):
                minus_index[d].append(i)
    return minus_index

def divide_index_calc(string):
    divide_index = defaultdict(list)
    a = 0
    for i in range(len(string)):
        if string[i] == '(':
            a += 1
        elif string[i] == ')':
            a -= 1
        elif string[i] == '/':
            for d in range(a, -1, -1):
                divide_index[d].append(i)
    return divide_index

def exponent_index_calc(string):
    exponent_index = defaultdict(list)
    a = 0
    for i in range(len(string)):
        if string[i] == '(':
            a += 1
        elif string[i] == ')':
            a -= 1
        elif string[i] == '^':
            for d in range(a, -1, -1):
                exponent_index[d].append(i)
    return exponent_index

def function_check(string, starting_char):
    a = 0
    for i in range(len(string) - starting_char):
        if string[starting_char + i] == '(':
            a += 1
        elif string[starting_char + i] == ')':
            a -= 1
        if a == 0:
            if not isclose(i, len(string) - starting_char - 1):
                return False
    return True

def differentiate(string, plus_index, minus_index, divide_index, exponent_index):
    recursion_level = 0
    #checks if input is a real number
    if check_real(string):
        return '0'
    #checks if input is a linear function
    elif string[-1] == 'x' and (check_real(string[:-1]) or string == 'x'):
        if string == 'x':
            return '1'
        return string[:-1]
    #checks if input is a polynomial
    elif string.count('x^') == 1 and (check_real(string[0:(string.index('x^'))]) or string[0:(string.index('x^'))] == '') and check_real(string[(string.index('x^') + 2):]):
        #applies power rule
        #checks if the function has a coefficient 
        if string[0:(string.index('x^'))] == '':
            if float(string[(string.index('x^') + 2):]) - 1 == 1:
                result = (str(string[(string.index('x^') + 2):])) + "x"
            else:
                result = (str(string[(string.index('x^') + 2):])) + "x^" + (str((float(string[(string.index('x^') + 2):]) - 1)))
        elif float(string[(string.index('x^') + 2):]) - 1 == 1:
            result = str((float(string[0:(string.index('x^'))])*float(string[(string.index('x^') + 2):]))) + "x"
        else:
            result = str((float(string[0:(string.index('x^'))])*float(string[(string.index('x^') + 2):]))) + "x^" + (str((float(string[(string.index('x^') + 2):]) - 1)))
        return result
    #checks if the string is sinx
    elif string == "sinx":
        return "cosx"
    #checks if the string is cosx
    elif string == "cosx":
        return "-sinx"
    #checks if the string is lnx
    elif string == "lnx":
        return "(1/x)"
    #checks if the string is sqrtx
    elif string == "sqrtx":
        return "1/(2sqrtx)"
    #checks if the string is tanx
    elif string == "tanx":
        return "((secx)^2)"
    #checks if the string is secx
    elif string == "secx":
        return "secxtanx" # might be good to change this to secx*tanx
    #checks if the string is cscx
    elif string == "cscx":
        return "-cscxcotx" # might be good to change this to -cscx*cotx
    #checks if the string is cotx
    elif string == "cotx":
        return "-((cscx)^2)"
    #checks if the string is arcsinx
    elif string == "arcsinx":
        return "1/((1-x^2)^(1/2))"
    #checks if the string is arccosx
    elif string == "arccosx":
        return "-1/((1-x^2)^(1/2))"
    #checks if the string is arctanx
    elif string == "arctanx":
        return "1/(1+x^2)"
    #checks if the string is contained within parentheses
    elif string[0] == '(' and string[-1] == ')' and function_check(string, 0):
        center_plus_index = plus_index_calc(string[1:-1])
        center_minus_index = minus_index_calc(string[1:-1])
        center_divide_index = divide_index_calc(string[1:-1])
        center_exponent_index = exponent_index_calc(string[1:-1])
        return '(' + differentiate(string[1:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')'
    #checks if the string is a function inside of sinx
    elif string[0:4] == "sin(" and string[-1] == ')' and function_check(string, len('sin')):
        center_plus_index = plus_index_calc(string[4:-1])
        center_minus_index = minus_index_calc(string[4:-1])
        center_divide_index = divide_index_calc(string[4:-1])
        center_exponent_index = exponent_index_calc(string[4:-1])
        return '(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "cos(" + string[4:]
    #checks if the string is a function inside of cosx
    elif string[0:4] == "cos(" and string[-1] == ')' and function_check(string, len('cos')):
        center_plus_index = plus_index_calc(string[4:-1])
        center_minus_index = minus_index_calc(string[4:-1])
        center_divide_index = divide_index_calc(string[4:-1])
        center_exponent_index = exponent_index_calc(string[4:-1])
        return '-(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "sin(" + string[4:]
    #checks if the string is a function inside of tanx
    elif string[0:4] == "tan(" and string[-1] == ')' and function_check(string, len('tan')):
        center_plus_index = plus_index_calc(string[4:-1])
        center_minus_index = minus_index_calc(string[4:-1])
        center_divide_index = divide_index_calc(string[4:-1])
        center_exponent_index = exponent_index_calc(string[4:-1])
        return '(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "(sec(" + string[4:] + "))^2"
    #checks if the string is a function inside of cotx
    elif string[0:4] == "cot(" and string[-1] == ')' and function_check(string, len('cot')):
        center_plus_index = plus_index_calc(string[4:-1])
        center_minus_index = minus_index_calc(string[4:-1])
        center_divide_index = divide_index_calc(string[4:-1])
        center_exponent_index = exponent_index_calc(string[4:-1])
        return '-(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "(csc(" + string[4:] + "))^2"
    #checks if the string is a function inside of secx
    elif string[0:4] == "sec(" and string[-1] == ')' and function_check(string, len('sec')):
        center_plus_index = plus_index_calc(string[4:-1])
        center_minus_index = minus_index_calc(string[4:-1])
        center_divide_index = divide_index_calc(string[4:-1])
        center_exponent_index = exponent_index_calc(string[4:-1])
        return '(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "sec(" + string[4:] + "tan(" + string[4:]
    #checks if the string is a function inside of cscx
    elif string[0:4] == "csc(" and string[-1] == ')' and function_check(string, len('csc')):
        center_plus_index = plus_index_calc(string[4:-1])
        center_minus_index = minus_index_calc(string[4:-1])
        center_divide_index = divide_index_calc(string[4:-1])
        center_exponent_index = exponent_index_calc(string[4:-1])
        return '-(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "csc(" + string[4:] + "cot(" + string[4:]
    #checks if the string is a function inside of arcsinx
    elif string[0:7] == 'arcsin(' and string[-1] == ')' and function_check(string, len('arcsin')):
        center_plus_index = plus_index_calc(string[7:-1])
        center_minus_index = minus_index_calc(string[7:-1])
        center_divide_index = divide_index_calc(string[7:-1])
        center_exponent_index = exponent_index_calc(string[7:-1])
        return '(' + differentiate(string[7:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "(1/((1-(" + string[7:] + '^2)^(1/2))'
    #checks if the string is a function inside of arccosx
    elif string[0:7] == 'arccos(' and string[-1] == ')' and function_check(string, len('arccos')):
        center_plus_index = plus_index_calc(string[7:-1])
        center_minus_index = minus_index_calc(string[7:-1])
        center_divide_index = divide_index_calc(string[7:-1])
        center_exponent_index = exponent_index_calc(string[7:-1])
        return '-(' + differentiate(string[7:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "(1/((1-(" + string[7:] + '^2)^(1/2))'
    #checks if the string is a function inside of arctanx
    elif string[0:7] == 'arctan(' and string[-1] == ')' and function_check(string, len('arctan')):
        center_plus_index = plus_index_calc(string[7:-1])
        center_minus_index = minus_index_calc(string[7:-1])
        center_divide_index = divide_index_calc(string[7:-1])
        center_exponent_index = exponent_index_calc(string[7:-1])
        return '(' + differentiate(string[7:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "(1/(1+(" + string[7:] + '^2))'
    #checks if the string is a function inside of lnx
    elif string[0:3] == "ln(" and string[-1] == ')' and function_check(string, len('ln')):
        center_plus_index = plus_index_calc(string[3:-1])
        center_minus_index = minus_index_calc(string[3:-1])
        center_divide_index = divide_index_calc(string[3:-1])
        center_exponent_index = exponent_index_calc(string[3:-1])
        return '(' + differentiate(string[3:-1], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + "(1/(" + string[3:] + ')'
    #checks if the string is a constant raised to the power of an expression
    elif string.count('^') == 1 and (check_real(string[0:string.index('^')]) or string[0] == 'e'):
        #if the base is e, differentiate such that ln(e) is not included
        if string[0] == 'e':
            if string[int(string.index('^')) + 1] == 'x':
                return string
            center_plus_index = plus_index_calc(string[3:-1])
            center_minus_index = minus_index_calc(string[3:-1])
            center_divide_index = divide_index_calc(string[3:-1])
            center_exponent_index = exponent_index_calc(string[3:-1])
            return "(" + differentiate(string[int(string.index('^')) + 1:], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + string
        else:
            if string[int(string.index('^')) + 1] == 'x':
                return string + '(ln(' + string[0:string.index('^')] + '))'
            center_plus_index = plus_index_calc(string[3:-1])
            center_minus_index = minus_index_calc(string[3:-1])
            center_divide_index = divide_index_calc(string[3:-1])
            center_exponent_index = exponent_index_calc(string[3:-1])
            return "(" + differentiate(string[int(string.index('^')) + 1:], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ')' + '(ln(' + string[0:string.index('^')] + '))' + string 
        #checks if the string is a simple quotient -> in the form of a/(f(x))
    elif string.count('/') == 1 and check_real(string[0]):
        i = 0
        while check_real(string[i]) or string[i] == '.':
            i += 1
        if string[string.index('/'):] == '/x':
            if i == 1:
                return '-' + string[0] + '/(x^2)'
            else:
                return '-' + string[0:string.index('/')] + '/(x^2)'
        if string[(string.index('/') + 1)] == '(':
            if i == 1:
                string
                center_plus_index = plus_index_calc(string[string.index('(') + 1:string.index(')')])
                center_minus_index = minus_index_calc(string[string.index('(') + 1:string.index(')')])
                center_divide_index = divide_index_calc(string[string.index('(') + 1:string.index(')')])
                center_exponent_index = exponent_index_calc(string[string.index('(') + 1:string.index(')')])
                return '(' + '-' + string[0] + '(' + differentiate(string[string.index('(') + 1:string.index(')')], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + '))/((' + string[string.index('(') + 1:string.index(')')] + ')^2)'
            else:
                center_plus_index = plus_index_calc(string[string.index('(') + 1:string.index(')')])
                center_minus_index = minus_index_calc(string[string.index('(') + 1:string.index(')')])
                center_divide_index = divide_index_calc(string[string.index('(') + 1:string.index(')')])
                center_exponent_index = exponent_index_calc(string[string.index('(') + 1:string.index(')')])
                return '(' + '-' + string[0:string.index('/')] + '(' + differentiate(string[string.index('(') + 1:string.index(')')], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + '))/((' + string[string.index('(') + 1:string.index(')')] + ')^2)'
        else:
            if i == 1:
                center_plus_index = plus_index_calc(string[string.index('/') + 1:])
                center_minus_index = minus_index_calc(string[string.index('/') + 1:])
                center_divide_index = divide_index_calc(string[string.index('/') + 1:])
                center_exponent_index = exponent_index_calc(string[string.index('/') + 1:])
                return '(' + '-' + string[0] + '(' + differentiate(string[string.index('/') + 1:], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + '))/((' + string[string.index('/') + 1:] + ')^2)'
            else:
                center_plus_index = plus_index_calc(string[string.index('/') + 1:])
                center_minus_index = minus_index_calc(string[string.index('/') + 1:])
                center_divide_index = divide_index_calc(string[string.index('/') + 1:])
                center_exponent_index = exponent_index_calc(string[string.index('/') + 1:])
                return '(' + '-' + string[0:string.index('/')] + '(' + differentiate(string[string.index('/') + 1:], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + '))/((' + string[string.index('/') + 1:] + ')^2)'
    #checks if the string is a function divided by a constant -> in the form of f(x)/a
    elif string.count('/') == 1 and (check_real(string[string.index('/') + 1:]) or (check_real(string[-1]) and len(string[string.index('/') + 1:]) == 0)):
        if (check_real(string[-1]) and len(string[string.index('/'):]) == 0):
            center_plus_index = plus_index_calc(string[0:string.index('/')])
            center_minus_index = minus_index_calc(string[0:string.index('/')])
            center_divide_index = divide_index_calc(string[0:string.index('/')])
            center_exponent_index = exponent_index_calc(string[0:string.index('/')])
            return differentiate(string[0:string.index('/')], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + '/' + string[-1]
        center_plus_index = plus_index_calc(string[0:string.index('/')])
        center_minus_index = minus_index_calc(string[0:string.index('/')])
        center_divide_index = divide_index_calc(string[0:string.index('/')])
        center_exponent_index = exponent_index_calc(string[0:string.index('/')])
        return differentiate(string[0:string.index('/')], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + '/' + string [string.index('/') + 1:]
    
    
    #checks if the string contains plus signs
    elif string.count('+') > 0:
        #checks if whether treating the expression as the sum of two expressions is valid
        index = string.index('+')
        for i in range(string.count('+')):
            if index not in plus_index[recursion_level + 1]:
                recursion_level += 1
                #splits the expression into two expressions
                left_substring = string[0:index]
                right_substring = string[int(index) + 1:]
                left_plus_index = plus_index_calc(left_substring)
                right_plus_index = plus_index_calc(right_substring)
                left_minus_index = minus_index_calc(left_substring)
                right_minus_index = minus_index_calc(right_substring)
                left_divide_index = divide_index_calc(left_substring)
                right_divide_index = divide_index_calc(right_substring)
                left_exponent_index = exponent_index_calc(left_substring)
                right_exponent_index = exponent_index_calc(right_substring)
                #differentiates both expressions
                differentiated_left = differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index, left_exponent_index)
                differentiated_right = differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index, right_exponent_index)
                #returns the sum of the two expressions
                return differentiated_left + "+" + differentiated_right
            if not isclose(i, string.count('+') - 1):
                index = string.index('+', index + 1)
    elif string.count('-') > 0:
        #handles leading negative
        if string[0] == '-':
            sub_expression = string[1:]
            sub_plus_index = plus_index_calc(sub_expression)
            sub_minus_index = minus_index_calc(sub_expression)
            sub_divide_index = divide_index_calc(sub_expression)
            sub_exponent_index = exponent_index_calc(sub_expression)
            differentiated = differentiate(sub_expression, sub_plus_index, sub_minus_index, sub_divide_index, sub_exponent_index)
            return "-" + differentiated
        index = string.index('-')
        for i in range(string.count('-')):
            if string.index('-') not in minus_index[recursion_level + 1]:
                recursion_level += 1
                left_substring = string[0:index]
                right_substring = string[index:]
                left_plus_index = plus_index_calc(left_substring)
                right_plus_index = plus_index_calc(right_substring)
                left_minus_index = minus_index_calc(left_substring)
                right_minus_index = minus_index_calc(right_substring)
                left_divide_index = divide_index_calc(left_substring)
                right_divide_index = divide_index_calc(right_substring)
                left_exponent_index = exponent_index_calc(left_substring)
                right_exponent_index = exponent_index_calc(right_substring)
                #differentiates both expressions
                differentiated_left = differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index, left_exponent_index)
                differentiated_right = differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index, right_exponent_index)
                #returns the sum of the two expressions
                if not isclose(i, string.count('-') - 1):
                    return differentiated_left + "-" + differentiated_right
            index = string.index('-', index + 1)
    elif string.count('/') > 0:
        #checks if whether treating the expression as the quotient of two expressions is valid
        if string.index('/') not in divide_index[recursion_level + 1]:
            recursion_level += 1
            left_substring = string[0:string.index('/')]
            right_substring = string[int(string.index('/')) + 1:]
            left_plus_index = plus_index_calc(left_substring)
            right_plus_index = plus_index_calc(right_substring)
            left_minus_index = minus_index_calc(left_substring)
            right_minus_index = minus_index_calc(right_substring)
            left_divide_index = divide_index_calc(left_substring)
            right_divide_index = divide_index_calc(right_substring)
            left_exponent_index = exponent_index_calc(left_substring)
            right_exponent_index = exponent_index_calc(right_substring)
            #applies quotient rule
            differentiated_left = differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index, left_exponent_index)
            differentiated_right = differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index, right_exponent_index)
            return '((' + differentiated_left + ')(' + right_substring + ')-(' + left_substring + ')(' + differentiated_right + '))/((' + right_substring + ')^2)'
    elif string.count('^') > 0:
        #checks if there are multiple exponents in the function
        if string.index('^') not in divide_index[recursion_level + 1]:
            recursion_level += 1
            left_substring = string[0:string.index('^')]
            right_substring = string[int(string.index('^')) + 1:]
            left_plus_index = plus_index_calc(left_substring)
            right_plus_index = plus_index_calc(right_substring)
            left_minus_index = minus_index_calc(left_substring)
            right_minus_index = minus_index_calc(right_substring)
            left_divide_index = divide_index_calc(left_substring)
            right_divide_index = divide_index_calc(right_substring)
            left_exponent_index = exponent_index_calc(left_substring)
            right_exponent_index = exponent_index_calc(right_substring)
            #applies quotient rule
            differentiated_left = differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index, left_exponent_index)
            differentiated_right = differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index, right_exponent_index)
            if check_real(left_substring) or ((check_int(string[0]) or string[0] == 'e') and string[0:string.index('^')] == ''):
                if string[0] == 'e':
                    return '(' + differentiated_right + ')(' + string + ')'
                elif check_real(left_substring):
                    return '(' + differentiated_right + ')(' + string + ')' + '(ln(' + left_substring + '))'
            else:
                return string + '((' + differentiated_right + ')ln(' + left_substring + ')+(' + right_substring + ')((' + differentiated_left + ')/(' + left_substring + '))'
    #checks if the string is a constant times a function
    elif check_real(string[0]):
        i = 0
        while check_real(string[i]) or string[i] == '.':
            i += 1
        if i == 1:
            center_plus_index = plus_index_calc(string[1:])
            center_minus_index = minus_index_calc(string[1:])
            center_divide_index = divide_index_calc(string[1:])
            center_exponent_index = exponent_index_calc(string[1:])
            return string[0] + "(" + differentiate(string[1:], center_plus_index, center_minus_index, center_divide_index, center_exponent_index) + ")"
        else:
            center_plus_index = plus_index_calc(string[i+1:])
            center_minus_index = minus_index_calc(string[i+1:])
            center_divide_index = divide_index_calc(string[i+1:])
            center_exponent_index = exponent_index_calc(string[1:])
            return string[0:i - 1] + differentiate(string[i+1:], center_plus_index, center_minus_index, center_divide_index, center_exponent_index)
    else:
        return "Invalid format for: -" + string + '- '

 










main()
