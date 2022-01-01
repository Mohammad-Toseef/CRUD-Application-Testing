from dotenv import load_dotenv
import os

load_dotenv('../environment.env')
print(os.getenv('globalSecretUser'))
# print(os.environ['globalSecretUser'])
print(os.environ.get('globalSecretUser'))

