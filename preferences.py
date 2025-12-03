import os

PREFERENCES_FILE = os.path.join(os.path.expanduser("~"), "finwise-data", "preferences.dat")
PREFERENCES_COUNT = 1

def open_preferences_file(mode):
    pref_file = open(PREFERENCES_FILE, mode)
    return pref_file

def set_defaults():
    pref_file = open_preferences_file("w")

    pref_file.write("categories:Food,Travel,Subscriptions,Bills,Entertainment,Misc\n")

    pref_file.close()
    print("Default preferences set successfully.")

def get_preferences():
    pref_file = open_preferences_file("r")

    preferences = dict()

    info_text = pref_file.readlines()
    for line in info_text:
        line = line.strip().split(":")
        if line[0] == "categories":
            preferences[line[0]] = line[1].split(",")
        else:
            preferences[line[0]] = line[1]
    
    pref_file.close()

    return preferences

def update_preferences(key, value):
    information = get_preferences()
    if len(information) != PREFERENCES_COUNT:
        set_defaults()
        return 0
    
    if key not in information.keys():
        print(f"Error: {key} not found in preferences. Exiting...")
        return 1
    
    information[key] = value

    pref_file = open_preferences_file("w")
    for k, v in information.items():
        if k == "categories":
            categories_str = ",".join(v)
            pref_file.write(f"{k}:{categories_str}")
        else:
            pref_file.write(f"{k}:{v}")

    pref_file.close()
    return 0

if __name__ == "__main__":
    set_defaults()