from field import Field

class Phone(Field):
    def __init__(self, value):
        # another method
        # x = filter(str.isdecimal, phone)
        # check_phone = "".join(x)
        check_phone = "".join(x for x in value if x.isdecimal())
        assert len(check_phone)==len(value)==10, f"phone should include 10 digits"
        self.value = value

    def __str__(self):
        return str(self.value)

# phone1 = Phone("1234567890")
# print(phone1.value)
