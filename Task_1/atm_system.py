"""
ATM Interface System
====================

Python Programming Internship - Task 1
Brainwave Matrix Solutions
Intern: Sylvester Elorm Kpei
Date: June 2025

Description:
A comprehensive ATM interface system demonstrating core banking operations
with security features, data persistence, and professional user experience.
"""

import json
import os
from datetime import datetime
import getpass

class ATMSystem:
    """
    Comprehensive ATM Interface System
    
    Features:
    - User authentication with PIN security
    - Balance inquiry and account management
    - Money withdrawal with daily limits
    - Cash deposits and transfers
    - Transaction history tracking
    - PIN change functionality
    - Persistent data storage using JSON
    """
    
    def __init__(self):
        """Initialize ATM system with default configuration"""
        self.accounts_file = "accounts.json"
        self.transactions_file = "transactions.json"
        self.current_account = None
        self.daily_withdrawal_limit = 500.00
        self.max_login_attempts = 3
        
        # Load existing data or create default accounts
        self.load_accounts()
        self.load_transactions()
        
        print("🏦 ATM System Initialized Successfully")
    
    def load_accounts(self):
        """Load account data from JSON file or create default test accounts"""
        try:
            with open(self.accounts_file, 'r') as f:
                self.accounts = json.load(f)
                print(f"✓ Loaded {len(self.accounts)} accounts from {self.accounts_file}")
        except FileNotFoundError:
            # Create default test accounts for demonstration
            self.accounts = {
                "1234567890": {
                    "pin": "1234",
                    "name": "John Doe",
                    "balance": 1000.00,
                    "account_type": "Checking",
                    "created_date": datetime.now().strftime("%Y-%m-%d")
                },
                "9876543210": {
                    "pin": "5678",
                    "name": "Jane Smith", 
                    "balance": 2500.00,
                    "account_type": "Savings",
                    "created_date": datetime.now().strftime("%Y-%m-%d")
                },
                "5555444433": {
                    "pin": "9999",
                    "name": "Sylvester Kpei",
                    "balance": 5000.00,
                    "account_type": "Premium",
                    "created_date": datetime.now().strftime("%Y-%m-%d")
                }
            }
            self.save_accounts()
            print("✓ Created default test accounts")
    
    def save_accounts(self):
        """Persist account data to JSON file"""
        try:
            with open(self.accounts_file, 'w') as f:
                json.dump(self.accounts, f, indent=2)
            print("✓ Account data saved successfully")
        except Exception as e:
            print(f"✗ Error saving accounts: {e}")
    
    def load_transactions(self):
        """Load transaction history from JSON file"""
        try:
            with open(self.transactions_file, 'r') as f:
                self.transactions = json.load(f)
                print(f"✓ Loaded transaction history")
        except FileNotFoundError:
            self.transactions = {}
            print("✓ Initialized new transaction history")
    
    def save_transactions(self):
        """Persist transaction history to JSON file"""
        try:
            with open(self.transactions_file, 'w') as f:
                json.dump(self.transactions, f, indent=2)
        except Exception as e:
            print(f"✗ Error saving transactions: {e}")
    
    def add_transaction(self, account_number, transaction_type, amount, description=""):
        """
        Add a new transaction to the history
        
        Args:
            account_number (str): Account identifier
            transaction_type (str): Type of transaction
            amount (float): Transaction amount
            description (str): Optional description
        """
        if account_number not in self.transactions:
            self.transactions[account_number] = []
        
        transaction = {
            "transaction_id": f"TXN{len(self.transactions[account_number]) + 1:04d}",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "description": description,
            "balance_after": self.accounts[account_number]["balance"]
        }
        
        self.transactions[account_number].append(transaction)
        self.save_transactions()
    
    def authenticate_user(self):
        """
        Handle user authentication with security measures
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        print("\n" + "="*60)
        print("           🏦 WELCOME TO BRAINWAVE ATM SYSTEM 🏦")
        print("="*60)
        print("              Secure Banking Made Simple")
        print("="*60)
        
        attempts = 0
        
        while attempts < self.max_login_attempts:
            try:
                print(f"\nLogin Attempt {attempts + 1} of {self.max_login_attempts}")
                
                account_number = input("👤 Enter your account number: ").strip()
                
                if not account_number:
                    print("❌ Account number cannot be empty!")
                    continue
                
                if account_number not in self.accounts:
                    print("❌ Invalid account number!")
                    attempts += 1
                    continue
                
                # Secure PIN entry
                pin = getpass.getpass("🔐 Enter your PIN: ")
                
                if self.accounts[account_number]["pin"] == pin:
                    self.current_account = account_number
                    account_name = self.accounts[account_number]['name']
                    print(f"\n✅ Authentication Successful!")
                    print(f"🎉 Welcome back, {account_name}!")
                    
                    # Log successful login
                    self.add_transaction(account_number, "Login", 0, "Successful authentication")
                    return True
                else:
                    print("❌ Incorrect PIN!")
                    attempts += 1
                    
            except KeyboardInterrupt:
                print("\n\n🚫 Session cancelled by user.")
                return False
            except Exception as e:
                print(f"❌ Authentication error: {e}")
                attempts += 1
        
        print(f"\n🔒 Account locked after {self.max_login_attempts} failed attempts.")
        print("Please contact customer service for assistance.")
        return False
    
    def display_menu(self):
        """Display the main ATM menu with professional formatting"""
        account = self.accounts[self.current_account]
        
        print("\n" + "="*50)
        print("               🏦 ATM MAIN MENU 🏦")
        print("="*50)
        print(f"  Account Holder: {account['name']}")
        print(f"  Account Type: {account['account_type']}")
        print(f"  Current Balance: ${account['balance']:,.2f}")
        print("="*50)
        print("  1. 💰 Check Balance")
        print("  2. 💸 Withdraw Money")
        print("  3. 💵 Deposit Money")
        print("  4. 🔄 Transfer Money")
        print("  5. 🔐 Change PIN")
        print("  6. 📋 Transaction History")
        print("  7. ℹ️  Account Information")
        print("  8. 🚪 Exit")
        print("="*50)
    
    def check_balance(self):
        """Display detailed account balance information"""
        account = self.accounts[self.current_account]
        
        print(f"\n{'='*40}")
        print("          💰 BALANCE INQUIRY 💰")
        print(f"{'='*40}")
        print(f"  Account Holder: {account['name']}")
        print(f"  Account Number: {self.current_account}")
        print(f"  Account Type: {account['account_type']}")
        print(f"  Current Balance: ${account['balance']:,.2f}")
        print(f"  Account Status: Active")
        print(f"{'='*40}")
        
        self.add_transaction(self.current_account, "Balance Inquiry", 0, "Balance checked via ATM")
    
    def withdraw_money(self):
        """Handle money withdrawal with security checks and limits"""
        account = self.accounts[self.current_account]
        current_balance = account['balance']
        
        print(f"\n{'='*40}")
        print("            💸 CASH WITHDRAWAL 💸")
        print(f"{'='*40}")
        print(f"  Available Balance: ${current_balance:,.2f}")
        print(f"  Daily Limit: ${self.daily_withdrawal_limit:,.2f}")
        print(f"{'='*40}")
        
        try:
            amount = float(input("💵 Enter withdrawal amount: $"))
            
            # Input validation
            if amount <= 0:
                print("❌ Invalid amount! Please enter a positive number.")
                return
            
            if amount != round(amount, 2):
                print("❌ Invalid amount! Please enter amount in cents precision.")
                return
            
            # Balance check
            if amount > current_balance:
                print("❌ Insufficient funds!")
                print(f"   Available balance: ${current_balance:,.2f}")
                self.add_transaction(self.current_account, "Failed Withdrawal", amount, "Insufficient funds")
                return
            
            # Daily limit check
            if amount > self.daily_withdrawal_limit:
                print(f"❌ Daily withdrawal limit exceeded!")
                print(f"   Daily limit: ${self.daily_withdrawal_limit:,.2f}")
                return
            
            # Transaction confirmation
            print(f"\n📋 Transaction Summary:")
            print(f"   Withdrawal Amount: ${amount:,.2f}")
            print(f"   Remaining Balance: ${current_balance - amount:,.2f}")
            
            confirm = input("\n✅ Confirm withdrawal? (y/n): ").lower()
            if confirm != 'y':
                print("🚫 Transaction cancelled.")
                return
            
            # Process withdrawal
            account['balance'] -= amount
            self.save_accounts()
            
            print(f"\n🎉 TRANSACTION SUCCESSFUL! 🎉")
            print(f"   Amount Withdrawn: ${amount:,.2f}")
            print(f"   New Balance: ${account['balance']:,.2f}")
            print(f"   📄 Please take your cash and receipt.")
            
            self.add_transaction(self.current_account, "Withdrawal", amount, f"ATM cash withdrawal")
            
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"❌ Transaction failed: {e}")
    
    def deposit_money(self):
        """Handle money deposit with validation"""
        account = self.accounts[self.current_account]
        
        print(f"\n{'='*40}")
        print("             💵 CASH DEPOSIT 💵")
        print(f"{'='*40}")
        print(f"  Current Balance: ${account['balance']:,.2f}")
        print(f"{'='*40}")
        
        try:
            amount = float(input("💰 Enter deposit amount: $"))
            
            # Input validation
            if amount <= 0:
                print("❌ Invalid amount! Please enter a positive number.")
                return
            
            if amount != round(amount, 2):
                print("❌ Invalid amount! Please enter amount in cents precision.")
                return
            
            # Large deposit check (for demonstration)
            if amount > 10000:
                print("⚠️  Large deposit detected. Additional verification may be required.")
                confirm_large = input("Continue with deposit? (y/n): ").lower()
                if confirm_large != 'y':
                    print("🚫 Transaction cancelled.")
                    return
            
            # Transaction confirmation
            print(f"\n📋 Deposit Summary:")
            print(f"   Deposit Amount: ${amount:,.2f}")
            print(f"   New Balance: ${account['balance'] + amount:,.2f}")
            
            confirm = input("\n✅ Confirm deposit? (y/n): ").lower()
            if confirm != 'y':
                print("🚫 Transaction cancelled.")
                return
            
            # Process deposit
            account['balance'] += amount
            self.save_accounts()
            
            print(f"\n🎉 DEPOSIT SUCCESSFUL! 🎉")
            print(f"   Amount Deposited: ${amount:,.2f}")
            print(f"   New Balance: ${account['balance']:,.2f}")
            print(f"   📄 Please take your receipt.")
            
            self.add_transaction(self.current_account, "Deposit", amount, "ATM cash deposit")
            
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"❌ Transaction failed: {e}")
    
    def transfer_money(self):
        """Handle money transfer between accounts"""
        account = self.accounts[self.current_account]
        
        print(f"\n{'='*45}")
        print("           🔄 MONEY TRANSFER 🔄")
        print(f"{'='*45}")
        print(f"  Available Balance: ${account['balance']:,.2f}")
        print(f"{'='*45}")
        
        try:
            recipient_account = input("👤 Enter recipient account number: ").strip()
            
            # Validation checks
            if recipient_account == self.current_account:
                print("❌ Cannot transfer to the same account!")
                return
            
            if recipient_account not in self.accounts:
                print("❌ Recipient account not found!")
                print("Please verify the account number and try again.")
                return
            
            amount = float(input("💰 Enter transfer amount: $"))
            
            # Input validation
            if amount <= 0:
                print("❌ Invalid amount! Please enter a positive number.")
                return
            
            if amount > account['balance']:
                print("❌ Insufficient funds!")
                print(f"   Available balance: ${account['balance']:,.2f}")
                return
            
            recipient_name = self.accounts[recipient_account]['name']
            
            # Transaction confirmation
            print(f"\n📋 Transfer Summary:")
            print(f"   From: {account['name']} ({self.current_account})")
            print(f"   To: {recipient_name} ({recipient_account})")
            print(f"   Amount: ${amount:,.2f}")
            print(f"   Your remaining balance: ${account['balance'] - amount:,.2f}")
            
            confirm = input("\n✅ Confirm transfer? (y/n): ").lower()
            if confirm != 'y':
                print("🚫 Transaction cancelled.")
                return
            
            # Process transfer
            account['balance'] -= amount
            self.accounts[recipient_account]['balance'] += amount
            self.save_accounts()
            
            print(f"\n🎉 TRANSFER SUCCESSFUL! 🎉")
            print(f"   Amount Transferred: ${amount:,.2f}")
            print(f"   To: {recipient_name}")
            print(f"   Your New Balance: ${account['balance']:,.2f}")
            print(f"   📄 Please take your receipt.")
            
            # Record transactions for both accounts
            self.add_transaction(self.current_account, "Transfer Out", amount, f"Transfer to {recipient_name}")
            self.add_transaction(recipient_account, "Transfer In", amount, f"Transfer from {account['name']}")
            
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"❌ Transaction failed: {e}")
    
    def change_pin(self):
        """Allow user to change their PIN with security validation"""
        print(f"\n{'='*40}")
        print("              🔐 CHANGE PIN 🔐")
        print(f"{'='*40}")
        print("  For your security, please verify your identity")
        print(f"{'='*40}")
        
        try:
            # Verify current PIN
            current_pin = getpass.getpass("🔐 Enter current PIN: ")
            
            if current_pin != self.accounts[self.current_account]['pin']:
                print("❌ Incorrect current PIN!")
                print("PIN change cancelled for security reasons.")
                return
            
            # Get new PIN
            new_pin = getpass.getpass("🆕 Enter new PIN (4 digits): ")
            
            # PIN validation
            if len(new_pin) != 4:
                print("❌ PIN must be exactly 4 digits!")
                return
                
            if not new_pin.isdigit():
                print("❌ PIN must contain only numbers!")
                return
            
            if new_pin == current_pin:
                print("❌ New PIN must be different from current PIN!")
                return
            
            # Confirm new PIN
            confirm_pin = getpass.getpass("🔁 Confirm new PIN: ")
            
            if new_pin != confirm_pin:
                print("❌ PINs do not match!")
                return
            
            # Update PIN
            self.accounts[self.current_account]['pin'] = new_pin
            self.save_accounts()
            
            print(f"\n🎉 PIN CHANGED SUCCESSFULLY! 🎉")
            print("   Your PIN has been updated securely.")
            print("   Please remember your new PIN.")
            
            self.add_transaction(self.current_account, "PIN Change", 0, "PIN updated via ATM")
            
        except KeyboardInterrupt:
            print("\n🚫 PIN change cancelled.")
        except Exception as e:
            print(f"❌ Error changing PIN: {e}")
    
    def show_transaction_history(self):
        """Display comprehensive transaction history"""
        print(f"\n{'='*60}")
        print("              📋 TRANSACTION HISTORY 📋")
        print(f"{'='*60}")
        
        if self.current_account not in self.transactions:
            print("   No transactions found for this account.")
            return
        
        transactions = self.transactions[self.current_account]
        
        if not transactions:
            print("   No transactions found for this account.")
            return
        
        # Display options
        print("  1. Show last 10 transactions")
        print("  2. Show all transactions")
        print("  3. Show transactions by type")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            display_transactions = transactions[-10:]
            print(f"\n📊 Last 10 Transactions:")
        elif choice == "2":
            display_transactions = transactions
            print(f"\n📊 All Transactions ({len(transactions)} total):")
        elif choice == "3":
            print("\nAvailable transaction types:")
            types = set(tx['type'] for tx in transactions)
            for i, tx_type in enumerate(types, 1):
                print(f"  {i}. {tx_type}")
            
            try:
                type_choice = int(input("Select type number: ")) - 1
                selected_type = list(types)[type_choice]
                display_transactions = [tx for tx in transactions if tx['type'] == selected_type]
                print(f"\n📊 {selected_type} Transactions:")
            except (ValueError, IndexError):
                print("❌ Invalid selection!")
                return
        else:
            print("❌ Invalid option!")
            return
        
        print("-" * 80)
        print(f"{'ID':<8} {'Date':<20} {'Type':<15} {'Amount':<12} {'Balance':<12} {'Description'}")
        print("-" * 80)
        
        for tx in display_transactions:
            tx_id = tx.get('transaction_id', 'N/A')
            date = tx['date']
            tx_type = tx['type']
            amount = f"${tx['amount']:,.2f}" if tx['amount'] != 0 else "-"
            balance = f"${tx['balance_after']:,.2f}"
            description = tx.get('description', '')[:25]
            
            print(f"{tx_id:<8} {date:<20} {tx_type:<15} {amount:<12} {balance:<12} {description}")
    
    def show_account_info(self):
        """Display comprehensive account information"""
        account = self.accounts[self.current_account]
        
        print(f"\n{'='*45}")
        print("           ℹ️  ACCOUNT INFORMATION ℹ️")
        print(f"{'='*45}")
        print(f"  Account Number: {self.current_account}")
        print(f"  Account Holder: {account['name']}")
        print(f"  Account Type: {account['account_type']}")
        print(f"  Current Balance: ${account['balance']:,.2f}")
        print(f"  Account Created: {account.get('created_date', 'N/A')}")
        print(f"  Account Status: Active")
        
        # Transaction statistics
        if self.current_account in self.transactions:
            total_transactions = len(self.transactions[self.current_account])
            print(f"  Total Transactions: {total_transactions}")
        
        print(f"{'='*45}")
    
    def run(self):
        """Main ATM program execution loop"""
        print("🚀 Starting ATM System...")
        
        # Authenticate user
        if not self.authenticate_user():
            print("👋 Thank you for visiting. Have a great day!")
            return
        
        # Main program loop
        while True:
            try:
                self.display_menu()
                choice = input("\n🎯 Select an option (1-8): ").strip()
                
                if choice == '1':
                    self.check_balance()
                elif choice == '2':
                    self.withdraw_money()
                elif choice == '3':
                    self.deposit_money()
                elif choice == '4':
                    self.transfer_money()
                elif choice == '5':
                    self.change_pin()
                elif choice == '6':
                    self.show_transaction_history()
                elif choice == '7':
                    self.show_account_info()
                elif choice == '8':
                    print(f"\n{'='*50}")
                    print("    🎉 Thank you for using Brainwave ATM! 🎉")
                    print("           Have a wonderful day!")
                    print(f"{'='*50}")
                    
                    # Log logout
                    self.add_transaction(self.current_account, "Logout", 0, "Session ended")
                    break
                else:
                    print("❌ Invalid option! Please select 1-8.")
                
                # Pause before continuing
                input("\n⏸️  Press Enter to continue...")
                
            except KeyboardInterrupt:
                print(f"\n\n{'='*40}")
                print("  🚫 Session interrupted by user")
                print("  👋 Thank you for using Brainwave ATM!")
                print(f"{'='*40}")
                break
            except Exception as e:
                print(f"❌ System error: {e}")
                print("Please try again or contact customer service.")
                input("Press Enter to continue...")

def main():
    """Main function to run the ATM system"""
    print("🏦 Brainwave Matrix Solutions - ATM Interface System")
    print("📚 Python Programming Internship - Task 1")
    print("👨‍💻 Developed by: Sylvester Elorm Kpei")
    print("📅 Date: June 2025")
    print("-" * 60)
    
    try:
        atm = ATMSystem()
        atm.run()
    except Exception as e:
        print(f"❌ Critical system error: {e}")
        print("Please restart the application.")

if __name__ == "__main__":
    main()
