import re

def validate_card_number(card_number):
    if re.match(r'^\d{13,19}$', card_number):
        # 1. Change datatype to list[int]
        card_number = [int(num) for num in card_number]

        # 2. Remove the last digit:
        checkDigit = card_number.pop(-1)

        # 3. Reverse the remaining digits:
        card_number.reverse()

        # 4. Double digits at even indices
        card_number = [num * 2 if idx % 2 == 0
                    else num for idx, num in enumerate(card_number)]

        # 5. Subtract 9 at even indices if digit is over 9
        # (or you can add the digits)
        card_number = [num - 9 if idx % 2 == 0 and num > 9
                    else num for idx, num in enumerate(card_number)]

        # 6. Add the checkDigit back to the list:
        card_number.append(checkDigit)

        # 7. Sum all digits:
        checkSum = sum(card_number)

        # 8. If checkSum is divisible by 10, it is valid.
        return checkSum % 10 == 0
    else: 
        return False

def validate_card_expiry(expiry):
    # Проверка формата срока действия (ММ/ГГ)
    return re.match(r'^(0[1-9]|1[0-2])\/?([0-9]{2})$', expiry) is not None

def validate_cvv(cvv):
    # Проверка формата CVV (3 или 4 цифры)
    return re.match(r'^\d{3}$', cvv) is not None