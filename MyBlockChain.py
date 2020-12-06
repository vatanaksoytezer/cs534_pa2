class MyBlock(object):
    def __init__(self, data):
        # No access to data
        self.__data = data
        self.next = None 

    def getData(self):
        return self.__data

class MyBlockChain(object):
    def __init__(self, chainName):
        self.chainName = chainName
        self.head = None

    def createAccount(self, amount):
        # Check account number, create new account with "account number +1"
        # Initial balance is amount
        # Creates a MyBlock
        # return account number
        accountNo = self.__getMaxAccountNumber() + 1
        data = ("CREATEACCOUNT",(accountNo, amount))
        self.__appendToEnd(data)
        return accountNo

    def calculateBalance(self, account_no):
        # Returns the balance on the given account
        # ! Make sure that account exists before this function is called
        if not (self.checkAccount(account_no)):
            raise Exception
        balance = 0
        last = self.head
        while last: 
            data = last.getData()
            if(data[1][0] == account_no and data[0] == "CREATEACCOUNT"):
                balance = data[1][1]
            elif (data[0] == "TRANSFER" or data[0] == "EXCHANGE") and (data[1][0] == account_no or data[1][1] == account_no):
                amount = data[1][2] if data[0] == "TRANSFER" else data[1][3]
                # It doesn't matter if amount is less than 0
                if data[1][0] == account_no:
                    balance -= amount
                elif data[1][1] == account_no:
                    balance += amount
            last = last.next
        return balance

    def transfer(self, from_, to_, amount):
        # Check from and to account by traversing the chain
        # Pass amount coins from "from" to "to"
        # If not enough balance or account cannot be found return -1
        # If amount < 0 from and to are swapped
        # Calculate balances, generates a new block and Return 1 on success
        if not (self.checkAccount(from_) and self.checkAccount(to_)):
            return -1
        fromAccount = from_
        toAccount = to_
        if amount < 0:
            # Swap the operation
            fromAccount = to_
            toAccount = from_
        # Check from account's balance
        fromBalance = self.calculateBalance(fromAccount)
        if (fromBalance - abs(amount)) < 0:
            return -1

        data = ("TRANSFER", (from_, to_, amount))
        self.__appendToEnd(data)
        return 1
        

    def exchange(self, from_, to_, toChain, amount):
        # Exchange rate is 1
        # the first check is if from account exists in the host chain and to account exists in toChain
        # Next, it is checked whether the account that will lose money has enough balance
        # If amount < 0 from and to are swapped
        # return -1 on fail
        # return 1 on success

        if not (self.checkAccount(from_) and toChain.checkAccount(to_)):
            return -1

        if amount > 0:
            # Check balance of current chain
            balance = self.calculateBalance(from_)
            if (balance - abs(amount)) < 0:
                return -1
        else:
            # Check balance of the other chain
            balance = toChain.calculateBalance(to_)
            if (balance - abs(amount)) < 0:
                return -1

        # Append data to current chain
        data = ("EXCHANGE", (from_, to_, toChain.chainName, amount))
        self.__appendToEnd(data)
        # Append data to other chain
        other_data = ("EXCHANGE", (to_, from_, self.chainName, -amount))
        toChain.__appendToEnd(other_data)
        return 1        

    def printChain(self):
        # Prints the transactions of all blocks in order to the console
        last = self.head
        chain = []
        while last: 
            chain.append(last.getData())
            last = last.next
        print(chain)

    # Helper for checking if account exists or not
    def checkAccount(self, account):
        last = self.head
        while last: 
            data = last.getData()
            if(data[0] == "CREATEACCOUNT"):
                accountNo = data[1][0]
                if account == accountNo:
                    return True
            last = last.next
        return False        


    # Appends to the end of blockchain
    def __appendToEnd(self, new_data): 
        new_block = MyBlock(new_data) 
        
        if self.head is None: 
                self.head = new_block 
                return
        
        last = self.head 
        while last.next: 
            last = last.next
        last.next = new_block 

    # Gets the max account number by traversing the chain
    def __getMaxAccountNumber(self):
        last = self.head
        maxAccountNo = 0
        while last: 
            data = last.getData()
            if(data[0] == "CREATEACCOUNT"):
                accountNo = data[1][0]
                if accountNo > maxAccountNo:
                    maxAccountNo = accountNo
            last = last.next
        return maxAccountNo


if __name__ == "__main__":
    BTC = MyBlockChain("BTC")
    BTC.createAccount(100)
    BTC.createAccount(900)
    BTC.createAccount(1800)
    BTC.transfer(1, 2, -50)
    BTC.transfer(2, 1, 30)
    print(BTC.calculateBalance(1))
    print(BTC.calculateBalance(2))
    print(BTC.calculateBalance(3))
    BTC.printChain()

    ETH = MyBlockChain("ETH")
    ETH.createAccount(500)
    ETH.createAccount(1500)

    BTC.exchange(2, 1, ETH, 80)
    print(BTC.calculateBalance(2))
    print(ETH.calculateBalance(1))
    ETH.printChain()
