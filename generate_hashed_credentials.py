import streamlit_authenticator as stauth
import yaml



# For quick testing, you can hardcode values:
username = 'fintra research'
password = 'xxxx'
name = 'Fintra Research'

# Hash the password (correct usage)
hashed_password = stauth.Hasher().hash(password)

# Prepare credentials dict
credentials = {
    'credentials': {
        'usernames': {
            username: {
                'name': name,
                'password': hashed_password
            }
        }
    }
}

# Save to YAML file
with open('hashed_credentials.yml', 'w') as file:
    yaml.dump(credentials, file)

print('Hashed credentials saved to hashed_credentials.yml') 