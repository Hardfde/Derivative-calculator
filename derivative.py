from collections import defaultdict
from math import isclose
def main():
    original_string = input("Input: ")
    plus_index = plus_index_calc(original_string)
    minus_index = minus_index_calc(original_string)
    divide_index = divide_index_calc(original_string)
    derivative = differentiate(original_string, plus_index, minus_index, divide_index)
    print(f"Derivative: {derivative}")

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

#constructs a 2d array where the the index of plus signs are recorded based on how nested they are within parenthesis 
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

#constructs a 2d array where the the index of negative signs are recorded based on how nested they are within parenthesis 
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

#constructs a 2d array where the the index of division signs are recorded based on how nested they are within parenthesis 
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

#determines whether an expression is a singular function
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

#finds the index of the first character after parenthesis have closed
def product_check(string):
    a = 0
    for i in range(len(string)):
        if string[i] == '(':
            a += 1
        elif string[i] == ')':
            a -= 1
        if a == 0:
            return int(i + 1)

#given a string and it's indexes calculates the derivative
def differentiate(string, plus_index, minus_index, divide_index):
    recursion_level = 0
    #checks if input is a real number
    if check_real(string):
        return '0'
    #checks if input is a linear function
    if string[-1] == 'x' and (check_real(string[:-1]) or string == 'x'):
        if string == 'x':
            return '1'
        return string[:-1]
    #checks if input is a polynomial
    if string.count('x^') == 1 and (check_real(string[0:(string.index('x^'))]) or string[0:(string.index('x^'))] == '') and check_real(string[(string.index('x^') + 2):]):
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
    if string == "sinx":
        return "cosx"
    #checks if the string is cosx
    if string == "cosx":
        return "-sinx"
    #checks if the string is lnx
    if string == "lnx":
        return "(1/x)"
    #checks if the string is sqrtx
    if string == "sqrtx":
        return "1/(2sqrtx)"
    #checks if the string is tanx
    if string == "tanx":
        return "((secx)^2)"
    #checks if the string is secx
    if string == "secx":
        return "secxtanx" # might be good to change this to secx*tanx
    #checks if the string is cscx
    if string == "cscx":
        return "-cscxcotx" # might be good to change this to -cscx*cotx
    #checks if the string is cotx
    if string == "cotx":
        return "-((cscx)^2)"
    #checks if the string is arcsinx
    if string == "arcsinx":
        return "1/((1-x^2)^(1/2))"
    #checks if the string is arccosx
    if string == "arccosx":
        return "-1/((1-x^2)^(1/2))"
    #checks if the string is arctanx
    if string == "arctanx":
        return "1/(1+x^2)"
    #checks if the string is contained within parentheses
    if string[0] == '(' and string[-1] == ')' and function_check(string, 0):
        inside_parenthesis = string[1:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '(' + differentiate(string[1:-1], center_plus_index, center_minus_index, center_divide_index) + ')'
    #checks if the string is a function inside of sinx
    if string.startswith('sin(') and string.endswith(')') and function_check(string, len('sin')):
        inside_parenthesis = string[4:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index) + ')cos(' + string[4:]
    #checks if the string is a function inside of cosx
    if string.startswith('cos(') and string.endswith(')') and function_check(string, len('cos')):
        inside_parenthesis = string[4:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '-(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index) + ')' + "sin(" + string[4:]
    #checks if the string is a function inside of tanx
    if string.startswith('tan(') and string.endswith(')') and function_check(string, len('tan')):
        inside_parenthesis = string[4:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index) + ')' + "(sec(" + string[4:] + "))^2"
    #checks if the string is a function inside of cotx
    if string.startswith('cot(') and string.endswith(')') and function_check(string, len('cot')):
        inside_parenthesis = string[4:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '-(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index) + ')' + "(csc(" + string[4:] + "))^2"
    #checks if the string is a function inside of secx
    if string.startswith('sec(') and string.endswith(')') and function_check(string, len('sec')):
        inside_parenthesis = string[4:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index) + ')' + "sec(" + string[4:] + "tan(" + string[4:]
    #checks if the string is a function inside of cscx
    if string.startswith('csc(') and string.endswith(')') and function_check(string, len('csc')):
        inside_parenthesis = string[4:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '-(' + differentiate(string[4:-1], center_plus_index, center_minus_index, center_divide_index) + ')' + "csc(" + string[4:] + "cot(" + string[4:]
    #checks if the string is a function inside of arcsinx
    if string.startswith('arcsin(') and string.endswith(')') and function_check(string, len('arcsin')):
        inside_parenthesis = string[7:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '(' + differentiate(string[7:-1], center_plus_index, center_minus_index, center_divide_index) + ')' + "(1/((1-(" + string[7:] + '^2)^(1/2))'
    #checks if the string is a function inside of arccosx
    if string.startswith('arccos(') and string.endswith(')') and function_check(string, len('arccos')):
        inside_parenthesis = string[7:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '-(' + differentiate(string[7:-1], center_plus_index, center_minus_index, center_divide_index) + ')' + "(1/((1-(" + string[7:] + '^2)^(1/2))'
    #checks if the string is a function inside of arctanx
    if string.startswith('arctan(') and string.endswith(')') and function_check(string, len('arctan')):
        inside_parenthesis = string[7:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '(' + differentiate(string[7:-1], center_plus_index, center_minus_index, center_divide_index) + ')' + "(1/(1+(" + string[7:] + '^2))'
    #checks if the string is a function inside of lnx
    if string.startswith('ln(') and string.endswith(')') and function_check(string, len('ln')):
        inside_parenthesis = string[3:-1]
        center_plus_index = plus_index_calc(inside_parenthesis)
        center_minus_index = minus_index_calc(inside_parenthesis)
        center_divide_index = divide_index_calc(inside_parenthesis)
        return '(' + differentiate(string[3:-1], center_plus_index, center_minus_index, center_divide_index) + ')' + "(1/(" + string[3:] + ')'
    #checks if the string is a constant raised to the power of an expression
    if string.count('^') == 1 and (check_real(string[0:string.index('^')]) or string[0] == 'e'):
        #if the base is e, differentiate such that ln(e) is not included
        if string[0] == 'e':
            if string[int(string.index('^')) + 1] == 'x':
                return string
            inside_parenthesis = string[3:-1]
            center_plus_index = plus_index_calc(inside_parenthesis)
            center_minus_index = minus_index_calc(inside_parenthesis)
            center_divide_index = divide_index_calc(inside_parenthesis)
            return "(" + differentiate(string[int(string.index('^')) + 1:], center_plus_index, center_minus_index, center_divide_index) + ')' + string
        #differentiates an exponential function with a real base
        else:
            if string[int(string.index('^')) + 1] == 'x':
                return string + '(ln(' + string[0:string.index('^')] + '))'
            inside_parenthesis = string[3:-1]
            center_plus_index = plus_index_calc(inside_parenthesis)
            center_minus_index = minus_index_calc(inside_parenthesis)
            center_divide_index = divide_index_calc(inside_parenthesis)
            return "(" + differentiate(string[int(string.index('^')) + 1:], center_plus_index, center_minus_index, center_divide_index) + ')' + '(ln(' + string[0:string.index('^')] + '))' + string 
    
    #checks if the string contains plus signs
    if string.count('+') > 0:
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
                #differentiates both expressions
                differentiated_left = differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index)
                differentiated_right = differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index)
                #returns the sum of the two expressions
                return differentiated_left + "+" + differentiated_right
            #cycles to next plus sign
            if not isclose(i, string.count('+') - 1):
                index = string.index('+', index + 1)
    if string.count('-') > 0:
        #handles leading negative
        if string[0] == '-':
            sub_expression = string[1:]
            sub_plus_index = plus_index_calc(sub_expression)
            sub_minus_index = minus_index_calc(sub_expression)
            sub_divide_index = divide_index_calc(sub_expression)
            differentiated = differentiate(sub_expression, sub_plus_index, sub_minus_index, sub_divide_index)
            return "-" + differentiated
        index = string.index('-')
        for i in range(string.count('-')):
            if index not in minus_index[recursion_level + 1]:
                recursion_level += 1
                #splits the expression into two expressions
                left_substring = string[0:index]
                right_substring = string[index + 1:]
                left_plus_index = plus_index_calc(left_substring)
                right_plus_index = plus_index_calc(right_substring)
                left_minus_index = minus_index_calc(left_substring)
                right_minus_index = minus_index_calc(right_substring)
                left_divide_index = divide_index_calc(left_substring)
                right_divide_index = divide_index_calc(right_substring)
                #differentiates both expressions
                differentiated_left = differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index)
                differentiated_right = differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index)
                #returns the sum of the two expressions
                return differentiated_left + "-" + differentiated_right
            #cycles to next negative sign
            if not isclose(i, string.count('-') - 1):
                index = string.index('-', index + 1)
    #checks if the string is a simple quotient -> in the form of a/(f(x))
    if string.count('/') == 1 and check_real(string[0]):
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
                return '(' + '-' + string[0] + '(' + differentiate(string[string.index('(') + 1:string.index(')')], center_plus_index, center_minus_index, center_divide_index) + '))/((' + string[string.index('(') + 1:string.index(')')] + ')^2)'
            else:
                center_plus_index = plus_index_calc(string[string.index('(') + 1:string.index(')')])
                center_minus_index = minus_index_calc(string[string.index('(') + 1:string.index(')')])
                center_divide_index = divide_index_calc(string[string.index('(') + 1:string.index(')')])
                return '(' + '-' + string[0:string.index('/')] + '(' + differentiate(string[string.index('(') + 1:string.index(')')], center_plus_index, center_minus_index, center_divide_index) + '))/((' + string[string.index('(') + 1:string.index(')')] + ')^2)'
        else:
            if i == 1:
                center_plus_index = plus_index_calc(string[string.index('/') + 1:])
                center_minus_index = minus_index_calc(string[string.index('/') + 1:])
                center_divide_index = divide_index_calc(string[string.index('/') + 1:])
                return '(' + '-' + string[0] + '(' + differentiate(string[string.index('/') + 1:], center_plus_index, center_minus_index, center_divide_index) + '))/((' + string[string.index('/') + 1:] + ')^2)'
            else:
                center_plus_index = plus_index_calc(string[string.index('/') + 1:])
                center_minus_index = minus_index_calc(string[string.index('/') + 1:])
                center_divide_index = divide_index_calc(string[string.index('/') + 1:])
                return '(' + '-' + string[0:string.index('/')] + '(' + differentiate(string[string.index('/') + 1:], center_plus_index, center_minus_index, center_divide_index) + '))/((' + string[string.index('/') + 1:] + ')^2)'
    #checks if the string is a function divided by a constant -> in the form of f(x)/a
    if string.count('/') == 1 and (check_real(string[string.index('/') + 1:]) or (check_real(string[-1]) and len(string[string.index('/') + 1:]) == 0)):
        if (check_real(string[-1]) and len(string[string.index('/'):]) == 0):
            center_plus_index = plus_index_calc(string[0:string.index('/')])
            center_minus_index = minus_index_calc(string[0:string.index('/')])
            center_divide_index = divide_index_calc(string[0:string.index('/')])
            return differentiate(string[0:string.index('/')], center_plus_index, center_minus_index, center_divide_index) + '/' + string[-1]
        center_plus_index = plus_index_calc(string[0:string.index('/')])
        center_minus_index = minus_index_calc(string[0:string.index('/')])
        center_divide_index = divide_index_calc(string[0:string.index('/')])
        return differentiate(string[0:string.index('/')], center_plus_index, center_minus_index, center_divide_index) + '/' + string [string.index('/') + 1:]
    if string.count('/') > 0:
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
            #applies quotient rule
            differentiated_left = differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index)
            differentiated_right = differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index)
            return '((' + differentiated_left + ')(' + right_substring + ')-(' + left_substring + ')(' + differentiated_right + '))/((' + right_substring + ')^2)'
    if string.count('^') > 0:
        #checks if there are multiple exponents in the function
        if string.index('^') not in divide_index[recursion_level + 1]:
            recursion_level += 1
            base_substring = string[0:string.index('^')]
            exponent_substring = string[int(string.index('^')) + 1:]
            base_plus_index = plus_index_calc(base_substring)
            exponent_plus_index = plus_index_calc(exponent_substring)
            base_minus_index = minus_index_calc(base_substring)
            exponent_minus_index = minus_index_calc(exponent_substring)
            base_divide_index = divide_index_calc(base_substring)
            exponent_divide_index = divide_index_calc(exponent_substring)
            #applies exponential rule
            differentiated_base = differentiate(base_substring, base_plus_index, base_minus_index, base_divide_index)
            differentiated_exponent = differentiate(exponent_substring, exponent_plus_index, exponent_minus_index, exponent_divide_index)
            if check_real(base_substring) or ((check_int(string[0]) or string[0] == 'e') and string[0:string.index('^')] == ''):
                if string[0] == 'e':
                    return '(' + differentiated_exponent + ')(' + string + ')'
                elif check_real(base_substring):
                    return '(' + differentiated_exponent + ')(' + string + ')' + '(ln(' + base_substring + '))'
            else:
                return string + '((' + differentiated_exponent + ')ln(' + base_substring + ')+(' + exponent_substring + ')((' + differentiated_base + ')/(' + base_substring + '))'
    #checks if the string is a constant times a function
    if check_real(string[0]):
        i = 0
        while check_real(string[i]) or string[i] == '.':
            i += 1
        if i == 1:
            center_plus_index = plus_index_calc(string[1:])
            center_minus_index = minus_index_calc(string[1:])
            center_divide_index = divide_index_calc(string[1:])
            return string[0] + "(" + differentiate(string[1:], center_plus_index, center_minus_index, center_divide_index) + ")"
        else:
            center_plus_index = plus_index_calc(string[i+1:])
            center_minus_index = minus_index_calc(string[i+1:])
            center_divide_index = divide_index_calc(string[i+1:])
            return string[0:i - 1] + differentiate(string[i+1:], center_plus_index, center_minus_index, center_divide_index)
    #first case of product rule ->   in the form x(sinx+1)
    if string[0] != '(' and string.count('(') > 0:
        left_substring = string[0:string.index('(')]
        right_substring = string[int(string.index('(')):]
        left_plus_index = plus_index_calc(left_substring)
        right_plus_index = plus_index_calc(right_substring)
        left_minus_index = minus_index_calc(left_substring)
        right_minus_index = minus_index_calc(right_substring)
        left_divide_index = divide_index_calc(left_substring)
        right_divide_index = divide_index_calc(right_substring)
        return '(' + differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index) + ')(' + right_substring + ')+(' + left_substring + ')(' + differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index) + ')'
    #second case of product rule ->   in the form (sinx+1)lnx
    if string[-1] != ')' and string[0] == '(' and string.count('(') > 0:
        i = len(string) - 1
        while string[i] != ')':
            i -= 1
        left_substring = string[0:i]
        right_substring = string[i + 1:]
        left_plus_index = plus_index_calc(left_substring)
        right_plus_index = plus_index_calc(right_substring)
        left_minus_index = minus_index_calc(left_substring)
        right_minus_index = minus_index_calc(right_substring)
        left_divide_index = divide_index_calc(left_substring)
        right_divide_index = divide_index_calc(right_substring)
        return '(' + differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index) + ')(' + right_substring + ')+(' + left_substring + ')(' + differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index) + ')'
    #third case of product rule ->   in the form (sinx+1)(lnx+1)
    if string[0] == '(':
        product_index = product_check(string)
        left_substring = string[0:product_index]
        right_substring = string[product_index:]
        left_plus_index = plus_index_calc(left_substring)
        right_plus_index = plus_index_calc(right_substring)
        left_minus_index = minus_index_calc(left_substring)
        right_minus_index = minus_index_calc(right_substring)
        left_divide_index = divide_index_calc(left_substring)
        right_divide_index = divide_index_calc(right_substring)
        return '(' + differentiate(left_substring, left_plus_index, left_minus_index, left_divide_index) + ')(' + right_substring + ')+(' + left_substring + ')(' + differentiate(right_substring, right_plus_index, right_minus_index, right_divide_index) + ')'
    else:
        return "Invalid format for: -" + string + '- '

 










main()
