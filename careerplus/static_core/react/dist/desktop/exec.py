def extract_phone_number(phone_number):
    if not phone_number:
        return ''

    phone_number = ''.join([digit for digit in phone_number if digit in string.digits + '+'])

    if phone_number.startswith('00'): #international number
        phone_number = '+' + phone_number[2:]
    elif phone_number.startswith('+91') and len(phone_number) != 13:
        phone_number = ''
    elif phone_number.startswith('91') and len(phone_number) == 12:
        phone_number = phone_number[2:]
    elif phone_number.startswith('0') and len(phone_number) == 11:
        phone_number = phone_number[1:]

    if not phone_number.startswith('+') and not len(phone_number) == 10:
        phone_number = ''

    phone_number = '+91' + phone_number if len(phone_number) == 10 and not phone_number.startswith('+') else phone_number

    return phone_number


def validate_phone_number(self):
        def is_digit(character):
            return character.isdigit()

        cell_phone = extract_phone_number(
            self.cell_phone)[-10:] if '91' in self.country_code else \
            ''.join(filter(is_digit, self.cell_phone))

        if not self.country_code or not cell_phone:
            return ''

        if self.country_code in ['91', '44', '1'] and \
                len(cell_phone) > 10 and not cell_phone.startswith('0'):
            return ''

        if len(cell_phone) + len(self.country_code) > 16:
            return ''

        if len(cell_phone) < 6:
            return ''

        if cell_phone in ['9999999999', '8888888888', '9876543210',
                          '7777777777', '9000000000', '8000000000',
                          '9898989898',
                          '6666666666']:
            return ''

        if self.country_code == '91' and cell_phone[0] in ['0', '1', '2', '3',
                                                           '4', '5']:
            return ''




validate_phone_number({'cell_phone' :"9958220358", 'country_code': '91'})