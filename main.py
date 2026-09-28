
user = {"name": "Roman", "city": "Odessa"}
extra = {"age": 31, "city": "Kyiv"}

profile = {**user, **extra}

print(profile)

print("Main branch change")
print("Feature branch")
print("Change from GitHub")

<<<<<<< HEAD
print("Local change")
=======
print("Remote change")
>>>>>>> aefbc969db8f3a8c5bcb806308ce77d876a23093
