import random

bankcard_prefix_list = ['6212261202043', '6228480328657', '6222620170000']


def generate():
    bankcard_prefix = bankcard_prefix_list[random.randint(0, len(bankcard_prefix_list)) - 1]
    bankcard_last_six_digit = random.randint(0, 999999)
    return bankcard_prefix + str(bankcard_last_six_digit).zfill(6)


print(generate())