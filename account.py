import os

ACCOUNT_FILE = os.path.join(os.path.expanduser("~"), "finwise-data", "account_data.dat")

INFO_COUNT = 4

def open_account_file(mode):
    account_file = open(ACCOUNT_FILE, mode)
    return account_file

def create_account():
    account_file = open_account_file("w")

    account_file.write("account_name:Default\n")
    account_file.write("current_balance:0.00\n")
    account_file.write("transaction_count:0\n")
    account_file.write("xp:0\n")

    account_file.close()
    print("Account created successfully.")

def get_account_info():
    account_file = open_account_file("r")

    account_information = dict()

    info_text = account_file.readlines()
    for line in info_text:
        line = line.strip().split(":")
        if line[0] == "account_name":
            account_information[line[0]] = line[1]
        elif line[0] == "current_balance":
            account_information[line[0]] = float(line[1])
        else:
            account_information[line[0]] = int(line[1])

    account_file.close()
    
    return account_information

def update_account(key, value):
    information = get_account_info()
    if len(information) != INFO_COUNT:
        create_account()
        return 0
    
    if key not in information.keys():
        print(f"Error: {key} not found in account data. Exiting...")
        return 1
    
    if key == "account_name":
        information[key] = value
    elif key == "current_balance":
        information[key] += float(value)
    else:
        information[key] += int(value)

    account_file = open_account_file("w")
    for k, v in information.items():
        account_file.write(f"{k}:{v}\n")
    
    account_file.close()
    return 0

if __name__ == "__main__":
    create_account()