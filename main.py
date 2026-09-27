
user = {"name": "Roman", "city": "Odessa"}
extra = {"age": 31, "city": "Kyiv"}

profile = {**user, **extra}

print(profile)
