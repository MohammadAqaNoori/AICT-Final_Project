import datetime
import os

# ====================== GLOBAL VARIABLES ======================
members = []      # List of dictionaries for members
payments = []     # List of dictionaries for payments
packages = {}     # Dictionary: package_name -> price

# File names
MEMBERS_FILE = "members.txt"
PAYMENTS_FILE = "payments.txt"
PACKAGES_FILE = "packages.txt"

# ====================== COLORS FOR BEAUTIFUL UI ======================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ====================== HELPER FUNCTIONS ======================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print(Colors.BLUE + Colors.BOLD)
    print("═" * 70)
    print("                 GYM MANAGEMENT SYSTEM ".center(70))
    print("═" * 70)
    print(Colors.END)

def main_menu():
    print_header()
    print(Colors.GREEN + Colors.BOLD + "                       MAIN MENU".center(70) + Colors.END)
    print(Colors.BLUE + "═" * 70 + Colors.END)
    print(Colors.YELLOW + "  1. Add New Member")
    print("  2. View All Members")
    print("  3. Search Member")
    print("  4. Update Member Details")
    print("  5. Renew Membership")
    print("  6. Record Payment")
    print("  7. Generate Gym Report")
    print("  8. Save & Exit")
    print("  0. Exit Without Saving" + Colors.END)
    print(Colors.BLUE + "═" * 70 + Colors.END)
    choice = input(Colors.BOLD + "\n   Enter your choice (0-8): " + Colors.END)
    return choice

# ====================== 1. LOAD DATA ======================
def load_data():
    global members, payments, packages
    
    # Load packages
    try:
        with open(PACKAGES_FILE, "r") as f:
            packages.clear()
            for line in f:
                if line.strip():
                    name, price = line.strip().split("|")
                    packages[name] = int(price)
    except FileNotFoundError:
        # Default packages if file not found
        packages = {
            "Monthly": 2000,
            "Quarterly": 5500,
            "Half-Yearly": 10000,
            "Yearly": 18000
        }
    
    # Load members
    try:
        with open(MEMBERS_FILE, "r") as f:
            members.clear()
            for line in f:
                if line.strip():
                    parts = line.strip().split("|")
                    members.append({
                        'id': parts[0],
                        'name': parts[1],
                        'age': parts[2],
                        'contact': parts[3],
                        'package': parts[4],
                        'join_date': parts[5],
                        'expiry': parts[6]
                    })
    except FileNotFoundError:
        members = []
    
    # Load payments
    try:
        with open(PAYMENTS_FILE, "r") as f:
            payments.clear()
            for line in f:
                if line.strip():
                    parts = line.strip().split("|")
                    payments.append({
                        'member_id': parts[0],
                        'amount': int(parts[1]),
                        'date': parts[2],
                        'method': parts[3]
                    })
    except FileNotFoundError:
        payments = []

# ====================== 2. SAVE DATA ======================
def save_data():
    # Save packages
    with open(PACKAGES_FILE, "w") as f:
        for name, price in packages.items():
            f.write(f"{name}|{price}\n")
    
    # Save members
    with open(MEMBERS_FILE, "w") as f:
        for m in members:
            f.write(f"{m['id']}|{m['name']}|{m['age']}|{m['contact']}|{m['package']}|{m['join_date']}|{m['expiry']}\n")
    
    # Save payments
    with open(PAYMENTS_FILE, "w") as f:
        for p in payments:
            f.write(f"{p['member_id']}|{p['amount']}|{p['date']}|{p['method']}\n")

# ====================== 3. ADD MEMBER ======================
def add_member():
    print_header()
    print(Colors.GREEN + "               ADD NEW MEMBER" + Colors.END)
    print(Colors.BLUE + "─" * 70 + Colors.END)
    
    name = input("Enter member name: ").strip().title()
    while True:
        try:
            age = int(input("Enter age: "))
            if age < 15 or age > 80:
                print(Colors.RED + "Age should be between 15 and 80." + Colors.END)
                continue
            break
        except:
            print(Colors.RED + "Invalid age!" + Colors.END)
    
    contact = input("Enter contact number: ").strip()
    
    print("\nAvailable Packages:")
    for i, (pkg, price) in enumerate(packages.items(), 1):
        print(f"  {i}. {pkg} - Rs. {price}")
    
    while True:
        pkg_choice = input("\nChoose package by name: ").strip().title()
        if pkg_choice in packages:
            package = pkg_choice
            break
        print(Colors.RED + "Invalid package! Choose from the list." + Colors.END)
    
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # Calculate expiry based on package
    if "Monthly" in package:
        months = 1
    elif "Quarterly" in package:
        months = 3
    elif "Half-Yearly" in package:
        months = 6
    else:
        months = 12
    
    expiry_date = (datetime.date.today() + datetime.timedelta(days=30*months)).strftime("%Y-%m-%d")
    
    # Auto generate ID
    new_id = f"M{len(members)+1:03d}"
    
    members.append({
        'id': new_id,
        'name': name,
        'age': str(age),
        'contact': contact,
        'package': package,
        'join_date': today,
        'expiry': expiry_date
    })
    
    print(Colors.GREEN + f"\nMember added successfully! ID: {new_id}" + Colors.END)
    input("\nPress Enter to continue...")

# ====================== 4. VIEW ALL MEMBERS ======================
def view_members():
    print_header()
    print(Colors.GREEN + "                 ALL MEMBERS" + Colors.END)
    print(Colors.BLUE + "─" * 100 + Colors.END)
    
    if not members:
        print(Colors.YELLOW + "No members registered yet!" + Colors.END)
    else:
        print(f"{'ID':<6} {'Name':<18} {'Age':<5} {'Contact':<15} {'Package':<15} {'Join Date':<12} {'Expiry':<12} {'Status'}")
        print("─" * 100)
        
        for m in members:
            expiry = datetime.datetime.strptime(m['expiry'], "%Y-%m-%d").date()
            today = datetime.date.today()
            status = "Active" if expiry >= today else "Expired"
            color = Colors.GREEN if status == "Active" else Colors.RED
            
            print(f"{m['id']:<6} {m['name']:<18} {m['age']:<5} {m['contact']:<15} {m['package']:<15} "
                  f"{m['join_date']:<12} {m['expiry']:<12} {color}{status}{Colors.END}")
    
    print(Colors.BLUE + "─" * 100 + Colors.END)
    input(Colors.BOLD + "\nPress Enter to return to menu..." + Colors.END)

# ====================== 5. SEARCH MEMBER ======================
def search_member():
    print_header()
    print(Colors.GREEN + "                 SEARCH MEMBER" + Colors.END)
    print(Colors.BLUE + "─" * 70 + Colors.END)
    
    if not members:
        print(Colors.YELLOW + "No members to search!" + Colors.END)
        input("\nPress Enter to continue...")
        return
    
    query = input("Enter Member ID or Name: ").strip().lower()
    found = [m for m in members if query in m['id'].lower() or query in m['name'].lower()]
    
    if not found:
        print(Colors.RED + "No member found!" + Colors.END)
    else:
        print(f"{'ID':<6} {'Name':<18} {'Contact':<15} {'Package':<15} {'Expiry':<12} {'Status'}")
        print("─" * 85)
        for m in found:
            expiry = datetime.datetime.strptime(m['expiry'], "%Y-%m-%d").date()
            status = "Active" if expiry >= datetime.date.today() else "Expired"
            color = Colors.GREEN if status == "Active" else Colors.RED
            print(f"{m['id']:<6} {m['name']:<18} {m['contact']:<15} {m['package']:<15} {m['expiry']:<12} {color}{status}{Colors.END}")
    
    input("\nPress Enter to continue...")

# ====================== 6. UPDATE MEMBER ======================
def update_member():
    print_header()
    print(Colors.GREEN + "                UPDATE MEMBER" + Colors.END)
    search_member()
    
    member_id = input("\nEnter Member ID to update: ").strip().upper()
    member = next((m for m in members if m['id'] == member_id), None)
    
    if not member:
        print(Colors.RED + "Member not found!" + Colors.END)
        input("\nPress Enter to continue...")
        return
    
    print(f"\nCurrent Details: {member['name']} ({member['id']})")
    print("Leave blank to keep current value.")
    
    new_name = input(f"New name [{member['name']}]: ").strip()
    if new_name: member['name'] = new_name.title()
    
    new_contact = input(f"New contact [{member['contact']}]: ").strip()
    if new_contact: member['contact'] = new_contact
    
    print(Colors.GREEN + "Member updated successfully!" + Colors.END)
    input("\nPress Enter to continue...")

# ====================== 7. RENEW MEMBERSHIP ======================
def renew_membership():
    print_header()
    print(Colors.GREEN + "               RENEW MEMBERSHIP" + Colors.END)
    search_member()
    
    member_id = input("\nEnter Member ID to renew: ").strip().upper()
    member = next((m for m in members if m['id'] == member_id), None)
    
    if not member:
        print(Colors.RED + "Member not found!" + Colors.END)
        input("\nPress Enter to continue...")
        return
    
    print(f"\nRenewing for: {member['name']} ({member['id']})")
    print("Available Packages:")
    for pkg, price in packages.items():
        print(f"  {pkg} - Rs. {price}")
    
    while True:
        pkg = input("\nChoose new package: ").strip().title()
        if pkg in packages:
            member['package'] = pkg
            break
        print(Colors.RED + "Invalid package!" + Colors.END)
    
    # Calculate new expiry
    if "Monthly" in pkg:
        months = 1
    elif "Quarterly" in pkg:
        months = 3
    elif "Half-Yearly" in pkg:
        months = 6
    else:
        months = 12
    
    member['expiry'] = (datetime.date.today() + datetime.timedelta(days=30*months)).strftime("%Y-%m-%d")
    
    print(Colors.GREEN + f"Membership renewed! New expiry: {member['expiry']}" + Colors.END)
    input("\nPress Enter to continue...")

# ====================== 8. RECORD PAYMENT ======================
def record_payment():
    print_header()
    print(Colors.GREEN + "                RECORD PAYMENT" + Colors.END)
    print(Colors.BLUE + "─" * 70 + Colors.END)
    
    search_member()
    member_id = input("\nEnter Member ID who paid: ").strip().upper()
    
    member = next((m for m in members if m['id'] == member_id), None)
    if not member:
        print(Colors.RED + "Member not found!" + Colors.END)
        input("\nPress Enter to continue...")
        return
    
    try:
        amount = int(input("Enter amount paid: "))
        method = input("Payment method (Cash/Card/UPI): ").strip().title()
        date = datetime.date.today().strftime("%Y-%m-%d")
        
        payments.append({
            'member_id': member_id,
            'amount': amount,
            'date': date,
            'method': method
        })
        
        print(Colors.GREEN + f"Payment of Rs. {amount} recorded successfully!" + Colors.END)
    except:
        print(Colors.RED + "Invalid amount!" + Colors.END)
    
    input("\nPress Enter to continue...")

# ====================== 9. GENERATE REPORT ======================
def generate_report():
    print_header()
    print(Colors.GREEN + "                  GYM REPORT" + Colors.END)
    print(Colors.BLUE + "─" * 70 + Colors.END)
    
    total_members = len(members)
    active = sum(1 for m in members if datetime.datetime.strptime(m['expiry'], "%Y-%m-%d").date() >= datetime.date.today())
    expired = total_members - active
    total_revenue = sum(p['amount'] for p in payments)
    
    print(f"Total Members        : {total_members}")
    print(f"Active Members       : {Colors.GREEN}{active}{Colors.END}")
    print(f"Expired Members      : {Colors.RED}{expired}{Colors.END}")
    print(f"Total Revenue        : {Colors.GREEN}Rs. {total_revenue}{Colors.END}")
    
    if members:
        from collections import Counter
        pkg_count = Counter(m['package'] for m in members)
        print("\nPackage Distribution:")
        for pkg, count in pkg_count.most_common():
            print(f"  {pkg}: {count} members")
    
    print(Colors.BLUE + "─" * 70 + Colors.END)
    input("\nPress Enter to return to menu...")

# ====================== MAIN PROGRAM ======================
def main():
    load_data()
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            add_member()
        elif choice == '2':
            view_members()
        elif choice == '3':
            search_member()
        elif choice == '4':
            update_member()
        elif choice == '5':
            renew_membership()
        elif choice == '6':
            record_payment()
        elif choice == '7':
            generate_report()
        elif choice == '8':
            save_data()
            print_header()
            print(Colors.GREEN + "All data saved successfully!".center(70) + Colors.END)
            print("Thank you for using Gym Management System! 💪".center(70))
            break
        elif choice == '0':
            confirm = input(Colors.RED + "Are you sure you want to exit without saving? (y/n): " + Colors.END).lower()
            if confirm == 'y':
                print_header()
                print(Colors.YELLOW + "Goodbye! Changes not saved.".center(70) + Colors.END)
                break
        else:
            print(Colors.RED + "Invalid choice! Please try again." + Colors.END)
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()