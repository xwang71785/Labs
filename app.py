'''
先通过和LLM对话，设计软件的逻辑框架，自顶向下细化到函数一级
以函数为单元，撰写函数的功能说明
为函数取有实际意义的名字
在docstring中写明输入输出和处理逻辑以及测试用例
触发copilot自动提示和补全功能来完成代码编写
'''

#function that takes two numbers and returns their sum
def add_numbers(num1, num2):
    """Returns the sum of two numbers."""
    return num1 + num2

def larger_number(num1, num2):
    """Returns the larger of two numbers."""
    return num1 if num1 > num2 else num2    

# call the larger_number function with values 10 and 20
# store the result in a variable and print it
result = larger_number(10, 20)  
print(f"The larger number is: {result}")


def best_word(word_list):
    """
    word_list is a list of words.
    Return the word worth the most points.
    """
    best_word = ""
    best_points = 0 # Initialize best points to zero
    for word in word_list:
        points = num_points(word) # Calculate points for the word
        if points > best_points:
            best_word = word
            best_points = points # Update best points if current word has more points
    return best_word


import doctest
doctest.testmod(verbose=True) # Run tests in the docstrings