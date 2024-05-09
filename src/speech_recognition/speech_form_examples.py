def get_examples() -> list:
    speech_form_examples = [

        {

            "intention": "buy",
            "item": "black car toy",
            "minimum_price": None,
            "maximum_price": None,

        },

        {

            "intention": "buy",
            "item": "gamer computer",
            "minimum_price": "5000",
            "maximum_price": "7000",

        },

        {

            "intention": "sell",
            "item": "car",
            "price": "35000",
            "description": "Honda black car with air-conditioner",

        },

        {
            "login": "useremail@email.com",
            "password": "user_password",
        }

    ]

    return speech_form_examples
