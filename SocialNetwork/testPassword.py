from django.contrib.auth.hashers import check_password

check_password('tajneheslo', 'pbkdf2_sha256$1000000$...')
from django.contrib.auth.models import User

# Nájdi svoj účet podľa používateľského mena alebo emailu:
user = User.objects.get(username="JakubZboron")  # alebo email="tvoj@email.com"

# Nastav nové heslo:
user.set_password("mojenoveheslo123")
user.save()

print("✅ Heslo bolo úspešne zmenené.")