currency_list = [
    {
        "base": "USD",
        "rates": {
            "UAH": 42.7,
            "USD": 1,
            "EUR": 0.83,
            "JPY": 154
        }
    },
    {
        "base": "EUR",
        "rates": {
            "UAH": 51.2,
            "USD": 1.19,
            "EUR": 1,
            "JPY": 185
        }
    },
    {
        "base": "JPY",
        "rates": {
            "UAH": 0.277,
            "USD": 0.0064,
            "EUR": 0.0054,
            "JPY": 1
        }
    },
    {
        "base": "UAH",
        "rates": {
            "UAH": 1,
            "USD": 0.0234,
            "EUR": 0.0195,
            "JPY": 3.6
        }
    }
]


def converter(amount,source):
    for currency in currency_list:
        if currency["base"] == source:
            for code,rate in currency["rates"].items():
                   if code != source:
                        print(f"{amount * rate:.2f} {code}")


def amount_validator():
    while True:
        amount = input("Введіть суму: ")
        try:
            number = float(amount)
            if number <= 0:
                print("Сума має бути більша за 0")
                continue
            return number
        except ValueError:
            print("Введіть число!")


def currency_validator(prompt):
        available_bases = [currency["base"] for currency in currency_list]
        while True:
            currency = input(prompt).upper()
            if currency in available_bases:
                return currency
            else:
                print("Введіть валюту зі списку:", ", ".join(available_bases))
    

amount = amount_validator()
source_currency = currency_validator("Введіть назву валюти з якої хочете перевести(USD/EUR/JPY/UAH): ")


converter(amount,source_currency)




