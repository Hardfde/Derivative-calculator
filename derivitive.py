#might need to put main below differentiate
#collects string to be differentiated
def main():
    original_string = input("Input: ")
    print(f"Derivitive: {differentiate(original_string)}")

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


def differentiate(string):
    #checks if input is a real number
    if check_real(string):
        a = 0
        return a
    #checks if input is a linear function
    elif string[-1] == 'x' and check_real(string[:-1]):
        result = string[:-1]
        return result
    
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
    #checks if the string is a constant times a function
    elif check_real(string[0]):
        i = 0
        while check_real(string[i]) or string[i] == '.':
            i += 1
        if i == 1:
            return string[0] + "(" + differentiate(string[1:]) + ")"
        else:
            return string[0:i - 1] + differentiate(string[i+1:])
    #checks if the string is a sum of multiple functions
    elif string.count('+') > 0:
        return differentiate(string[0:string.index('+')]) + "+" + differentiate(string[int(string.index('+')) + 1:])
    #checks if the string is the difference of multiple functions
    elif string.count('-') > 0:
        #accounts for leading negative sign
        if string[0] =='-':
            return '-' + differentiate(string[1:])
        return differentiate(string[0:string.index('-')]) + "-" + differentiate(string[int(string.index('-')) + 1:])











main()
