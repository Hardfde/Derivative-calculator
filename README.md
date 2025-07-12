# Derivative-calculator
Video Demo: https://youtu.be/i1PkjoV16jw
Discription: This python code will ask the user for an input, and will output the input's derivative (from calculus)
Code explained: 
We start by importing in defaultdict and isclose, which we will need later
### main
main asks the user for input and assigns it to a variable called original_string.
then it calls 4 functions: **plus_index_calc**, **minus_index_calc**, **divide_index_calc**, and **differentiate**, which are all assigned to a unique variable (these will be explained later).
Then it main prints the derivativein the format Derivative: {derivative}
### check_real
the first helper function is check_real, which when inputed a string, outputs true or false based on whether the string is a real number.
This is accomplished through using try to see if if the string can be converted to a float and except to catch if it can not
### check_int
Very similar to check_real, except it outputs true or false based on whether the string is an integer.
### next_paren
finds the index of the next ')' given a string and a starting index, useful for isolating functions
## plus_index_calc
**This is a _very_ important function**
inputed into it is a string.
It first creates a defaultdict(list) and assigns it to a variable called **plus_index**.
then, it runs thorugh every character in the string, increasing a varible a by 1 when the character is '(' and decreasing a by 1 when the character is a ')'.
If the character is a '+', then it appends the index of that character to the ath level and all below of plus_index.
It then returns plus_index after all the characters have been cycled through.
The reason for this function is to determine the index of all the '+' signs and how nested they are by parenthesis
## minus_index_calc
minus_index_calc functions exactly the same as plus_index_calc, except for '-' instead of '+'
## divide_index_calc
minus_index_calc functions exactly the same as plus_index_calc and minus_index_calc, except for '/' instead of '+' or '-'
### function_check
function_check calls for an input of a string and a integer which represents which character function_check should start with.
It first sets a variable a to 0, then uses a for i in range loop of the length of the string - the integer.
It starts off similar to the index_calc functions for parenthesis, but then if a = 0, it checks if the for loop has cycled through all the characters in the string.
If it has not, it returns false, indicating the string is comprised of more than one function. Otherwise, it returns true.
### product_check
product check finds the index of the first character after parenthesis have closed thorugh very similar logic to function_check.
## differentiate
#### Input
The differentiate function takes as input a string as well as the plus, minus, and divide indices.
#### Output
differentiate outputs the derivative of string string input.
#### Intial variable
It first sets a variable called **recursion_level** to 0, this will be important later.
#### Process
It performs many checks on the string in order to determine what to output.
#### Constant
It checks whether the string is a real number with the **is_real** function, returning 0 as the derivative if so.
#### Linear
Then it checks if the function is linear, through seeing if the end character is an x and if what comes before x is a real number or nothing, returning either the real number or 1 if the string is just x.
#### Monomial
After that, it checks if the string is a monomial, if so, it applies the power rule -> d/dx x^n = nx^(n-1)
#### Common functions
Then, it performs many checks to see if the string is a common function like sinx, lnx, or arcsin, and differentiates accordingly.
#### Enclosed within parenthesis
After that, it checks if the string is enclosed by parenthesis and uses function_check to determine if the string is one function.
Then recursion is used by calling the derivative function to find the derivative of the string, excluding the parenthesis which the string is encolsed in, this also requires that plus_index, minus_index, and divide_index be recalculated.
#### Common functions with chain rule
differentiate then runs through all the functions which were just specifically checked (like sinx, lnx, and arcsin) and using function_check determines if there is a function inside of one of those specific function.
It then uses chain rule to calculate the derivative, which means recursion is used again, as well as recalculating the indices.
#### Exponents in the form a^f(x)
To deal with exponents in the form where a is real or 'e', we check if the string is in the form of a^x, where a is a real number or e, then differentiates accordingly -> d/dx a^f(x) = f'(x)(a^f(x))(ln(a))
#### Sum rule
After that, we have a much more complicted functionality which determines whether if it is valid to break the string into two substrings around a '+' sign.
This is done by cycling through each '+' sign and checking if its index is contained within plus_index at a recursion level of 1 greater than the current.
If so, it breaks the string into a left_substring and right_substring, which also means we need to increment recursion_level by 1.
Then, the left and right substring's indices are each recalculated, their derivatives are found, and then the two substring are merged together again by a '+' sign.
#### Difference rule
Handling '-' signs is almost exactly the same as handling '+', except we have to account for if there is a leading negative (ie -f(x), which would not be a suitible case for the subtraction of two string).
So we check if the first character of the string is a '-', if so, it finds the derivative of the substring after the negative sign (this entales 
After this, it adds the '-' back to the first character of the string, note: the indices have to be recalculated.
Then it performs executes the same as '+' except with '-'
#### Quotient rule
##### In the form a/(f(x))
To deal with quotients where in the form a/(f(x)) where a is a constant, we first need to check if a is a constant, which is done through the check_real function.
Then, we check the calculate the derivative by taking it as the function raised to the -1 power, note: a equaling 1 and the function being 1/x are specific cases handled first.
##### In the form f(x)/a
To deal with quotients where in the form (f(x))/a where a is a constant, we first check if a is a constant, if a is, we simply differentiate f(x), and then add /a to end of the string. Note: the indices have to be recalculated.
##### In the form (f(x))/(g(x))
To deal with quotients where in the form (f(x))/(g(x)), similarly to the sum rule, we check if the '/' index is contained within divide_index at a recursion level of 1 greater than the current. If so, we break the string into two substring's around the '/' and differentiate each substring. Note: the indices have to be recalculated.
Then, it outputs using quotient rule -> d/dx f(x)/g(x) = (f'(x)g(x)-f(x)g'(x))/(g(x)^2)
#### Multiple exponents
If there are multiple exponents in the string, similary to quotient rule in the (f(x))/(g(x)), we break the string into two substrings, and find the derivative of each.
Note: the indices have to be recalculated.
It also accounts for a base of e, and then applies a formula to combine them back together.
Formula: d/dx f(x)^g(x) = (f(x)^g(x))(g'(x)ln(f(x))+g(x)(f'(x)/f(x)))
#### In the form af(x)
Checks if the string is in the form af(x), where a is a constant. If it is, it finds the derivative of f(x) and attaches a to the front
#### Product rule
##### In the form f(x)(g(x))
ie: x(sinx+1)
Checks if the string is in the form f(x)(g(x)), then similarly to quotient rule, breaks the string into two substrings and finds the derivative of both.
Note: the indices have to be recalculated.
They are then combined together in the form of product rule -> d/dx f(x)g(x) = f'(x)g(x)+f(x)g'(x)
##### In the form (f(x))g(x)
ie: (sinx+1)lnx
Functions almost exactly the same as the first form, except a while loop is used to find the index of the last')' in order to correctly break up the string into two substrings. Note: the indices have to be recalculated.
##### In the form (f(x))(g(x))
ie: (sinx+1)(lnx+1)
Functions the same as the first form, except product_index is used to correctly break up the string into two substrings. Note: the indices have to be recalculated.
##### Else
If none of the previous checks catch the string, it returns Invalid format for: -whatever the string was-

AI was used to help create this project by explaining relevant concepts and suggested using defaultdict