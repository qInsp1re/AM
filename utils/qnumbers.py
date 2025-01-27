class QNumber:
    def __init__(self, m: int, n: int, value: int) -> None:
        """
        Инициализация объекта QNumber.
        :param m: Количество битов для целой части
        :param n: Количество битов для дробной части
        :param value: Значение в формате Q(m, n)
        """
        self.m = m
        self.n = n
        self.size = m + n
        self.value = value

    def __str__(self) -> str:
        """
        Возвращает строковое представление значения в шестнадцатеричном формате.
        """
        return hex(self.value)

    @staticmethod
    def from_float(value: float, m: int, n: int) -> 'QNumber':
        """
        Создает объект QNumber из обычного числа с плавающей запятой.
        :param value: Значение в формате float
        :param m: Количество битов для целой части
        :param n: Количество битов для дробной части
        :return: Объект QNumber
        """
        int_part = int(value)
        float_part = value - int_part

        # Преобразование целой части в бинарный формат
        bin_int_part = bin(int_part)[2:].rjust(m, "0")
        # Преобразование дробной части в бинарный формат
        bin_float_part = bin(int(float_part * (2 ** n)))[2:].rjust(n, "0")

        # Объединение целой и дробной частей
        res_bin = bin_int_part + bin_float_part
        res = int(res_bin, 2)

        return QNumber(m, n, res)

    def to_float(self) -> float:
        """
        Преобразует значение QNumber обратно в число с плавающей запятой.
        :return: Значение в формате float
        """
        bin_value = bin(self.value)[2:].rjust(self.size, "0")

        # Извлечение целой части и дробной части
        int_part = int(bin_value[:self.m], 2)
        decimal_part = int(bin_value[self.m:], 2) / (2 ** self.n)

        return int_part + decimal_part
