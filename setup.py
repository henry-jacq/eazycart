from config import helper

if __name__ == "__main__":
    cred = helper.get_app_details()
    print(f"\n[+] Setting up {cred.get('name')}...\n")
    if helper.rename_config_file() == True:
        print(f"[+] Done!\n")
    else:
        print(f"[-] Cannot setup the application!\n")
        print(f"[-] ERROR: {helper.rename_config_file()}")
