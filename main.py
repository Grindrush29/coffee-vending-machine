from machine_data import menu, resources
import math
machine_on = True
machine_state = "on"
vend_details = {"vend_power": True, "vend_state": "fine"}
def report():
    """Gives the stats of the machine this includes the materials and the state of the machine"""
    print(f"Water: {resources['water']}")
    print(f"Milk: {resources['milk']}")
    print(f"Coffee: {resources['coffee']}")
    print(f"Money made: {resources['money']}")
    print(f"Vending Power: {vend_details['vend_power']}")
    print(f"Vending State: {vend_details['vend_state']}")


def restock():
    """restock the materials"""
    resources["water"] = 300
    resources["milk"] = 200
    resources["coffee"] = 100


def ordering(user_input):
    """ subtracts the materials needed to make the ordered drink from reserves"""
    resources["water"] -= menu[user_input]["ingredients"]["water"]
    if "milk" in menu[user_input]["ingredients"]:
        resources["milk"] -= menu[user_input]["ingredients"]["milk"]
    resources["coffee"] -= menu[user_input]["ingredients"]["coffee"]


def hidden_input(user_input, options):
    """deals with inputs only the owner and the maintainer of the machine should know"""
    vending_power(user_input)
    options = material_sensing(options)
    if vend_details["vend_power"] == False:
        if user_input == "on":
            vend_details["vend_power"] = True
            options = material_sensing(options)
            return options
        else:
            return "Out of order (off): "
    elif user_input == "report":
        report()
        return options
    elif user_input == "restock":
        restock()
        return options

    elif not(vend_details["vend_state"] == "fine"):
        if user_input == "restock":
            vend_details["vend_state"] = "fine"
            restock()
        else:
            return "Out of order: "
    
    elif user_input == "on":
        options = material_sensing(options)
        return options
        
      
def vending_power(user_input):
    """Turns the power of the vending machine on or off"""
    if user_input == "on":
        vend_details["vend_power"] = True
    if user_input == "off":
        vend_details["vend_power"] = False


def material_sensing(options):
    """Checks if there is enough materials for the drink
    if no remove option and if no drink work turn off machine and signal restock
    """
    if not(vend_details['vend_power'] == False):
        sense = []
        options = "What would you like? ("
        if (resources["water"] >= menu["espresso"]["ingredients"]["water"]) and (resources["coffee"] >= menu["espresso"]["ingredients"]["coffee"]):
            options += "espresso/"
            sense.append("yes")
        if (resources["water"] >= menu["latte"]["ingredients"]["water"]) and (resources["coffee"] >= menu["latte"]["ingredients"]["coffee"]) and (resources["milk"] >= menu["latte"]["ingredients"]["milk"]):
            options += "latte"
            sense.append("yes")
        if (resources["water"] > menu["cappuccino"]["ingredients"]["water"]) and (resources["coffee"] >= menu["cappuccino"]["ingredients"]["coffee"]) and (resources["milk"] >= menu["cappuccino"]["ingredients"]["milk"]):
            options += "/cappuccino"
            sense.append("yes")

        if sense == []:
            vend_details["vend_state"] = "Needs restock"
            options = "Out of order: "
        else:
            vend_details["vend_state"] = "fine"
            options += "): "

        if "//" in options:
            options = options.replace("//", "/")
        if options == "What would you like? (espresso/): ":
            options = options.replace("/", "")

        if options == "(What would you like? (/cappuccino): ":
            options = options.replace("/", "")
        

        return options
    else:
        return options


def payment(user_input):
    """Adds the total of the money given to the vending machine"""
    total = 0
    print("Please insert coins")
    dollars = int(input("How many dollars: "))
    total += round(int(dollars) * 1, 2)

    quarters = int(input("How many quarters: "))
    total += round(quarters * 0.25, 2)
    dimes = int(input("How many dimes: "))
    total += round(dimes * 0.10, 2)
    nickles = int(input("How many nickles: "))
    total += round(nickles * 0.05, 2)
    pennies = int(input("How many pennies: "))
    total += round(pennies * 0.01, 2)
    print(f"Total {round(total, 2)}")
    success, refund = transaction(total, user_input)
    if success:
        ordering(user_input)
    return success, refund


def transaction(payment, user_input):
    """Checks if customer has enough money to get a drink. If not refund the money"""
    cost = menu[user_input]["cost"]
    refund = round(payment - cost, 2)
    payment = round(payment, 2)
    if refund >= 0:
        resources["money"] += round(menu[user_input]["cost"], 2)
        return True, refund
    else:
        return False, payment


def main():
    options = "What would you like? (espresso/latte/cappuccino)"
    options = material_sensing(options)
    while machine_on:
        options = material_sensing(options)
        user_input = input(options).lower()
        #deals with hidden inputs (report/off/on/restock)
        if user_input == "on" or user_input == "off" or user_input == "report" or user_input == "restock":
            options = hidden_input(user_input, options)


        # deals with the drink ordering
        elif user_input == "espresso" or user_input == "latte" or user_input == "cappuccino":
            successful, refund = payment(user_input)
            if successful:
                print(f"Here is {refund} in change.")
                print(f"Here is your {user_input} Enjoy!")
            
            else:
                print("Insufficient funds")
                print(f"Refund: {refund}")


        options = material_sensing(options)





if __name__ == "__main__":
    main()
