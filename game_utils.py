import sympy
from llm_chat import generate_response


# 定义关卡信息和验证逻辑

# 辅助函数 - 检查是否为质数
def is_prime(num):
    return sympy.isprime(num)


# 辅助函数 - 获取下一个质数
def next_prime(num):
    return sympy.nextprime(num)


# 辅助函数 - 检查是否为平方数
def is_square(n):
    return sympy.sqrt(n).is_integer


# 辅助函数 - 获取平方根
def get_square_root(n):
    return int(sympy.sqrt(n))


def validate_palindrome_invariance(origin_input, response):
    """
    验证器函数，检查对于给定的问题，正着问和倒着问的模型回答是否一致。

    :param origin_input: 原始问题
    :return: True 如果回答一致，否则 False
    """

    # 将原始问题倒序并提交
    reversed_question = origin_input[::-1]
    reversed_response = generate_response(reversed_question)

    # 比较两个回答是否一致
    return response.strip() == reversed_response.strip()


def validate_palindrome_inverse(origin_input, response):
    """
    验证器函数，检查对于给定的问题，正着问和倒着问的模型的回答本身不回文且也是逆序的关系。

    :param origin_input: 原始问题
    :param response: 模型对原始问题的回答
    :param model_fn: 能够返回模型回答的函数
    :return: True 如果回答本身不回文且也是逆序关系，否则 False
    """

    # 检查原始输入不是回文
    if origin_input == origin_input[::-1]:
        return False

    # 将原始问题倒序并获取模型回答
    reversed_question = origin_input[::-1]
    reversed_response = generate_response(reversed_question).strip()

    # 检查原始回答不是回文
    if response == response[::-1]:
        return False

    # 比较正着问和倒着问的回答是否是逆序关系
    return response == reversed_response[::-1]


def validate_reciprocal_question(input, response):
    """
    验证器函数，检查给定的问题A和回答B，是否能够通过以B作为新的提问得到原始问题A作为回答。

    :param response: 模型对问题A的回答B
    :param input: 原始问题A
    :param model_fn: 模型调用函数，接收问题并返回回答
    :return: True 如果以回答B作为新的提问能得到问题A作为回答，否则 False
    """

    # 确保回答B不等于原始问题A
    if response == input:
        return False

    # 以回答B作为新的提问
    new_response = generate_response(response)

    # 检查新的回答是否与原始问题A相等
    return new_response.strip() == input.strip()

