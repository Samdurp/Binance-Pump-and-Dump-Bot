import math
import time
import sys
import decimal
import os
import shutil
import array
import numpy as np
from binance.enums import *
from binance.client import Client
from colorama import Fore, Back, Style

# 1 = uses output.txt as input for coin name, 0 doesnt
useOutputTxt = 1

if (useOutputTxt == 1):
    print("Scanning for output.txt...")
    while (1 == 1):
        try:
            file = open("output.txt", "r")
            if (os.stat("output.txt").st_size == 0):
                file.close()
                continue
            else:
                break;
        except:
            continue

    coinName1 = np.chararray(10)
    nameLength = 0
    while (1 == 1):
        char = file.read(1)
        if (char == '"'): # open quote
            while (1 == 1): # keep scanning
                char = file.read(1)
                if (char == '"'):
                    break
        if (char == '$'):
            while (1 == 1):
                char = file.read(1)
                if (char == ' ' or char == '\n'):
                    break
                else:
                    coinName1[nameLength] = char
                nameLength += 1
        if not char:
            break

    coinName2 = np.chararray(nameLength)
    iterator = 0
    while (iterator < nameLength):
        coinName2[iterator] = coinName1[iterator]
        iterator += 1

    fuck = coinName2.decode("utf-8")
    shit = str("")
    ass = ""
    if (nameLength == 2):
        ass = fuck[0] + fuck[1]
    elif (nameLength == 3):
        ass = fuck[0] + fuck[1] + fuck[2]
    elif (nameLength == 4):
        ass = fuck[0] + fuck[1] + fuck[2] + fuck[3]
    elif (nameLength == 4):
        ass = fuck[0] + fuck[1] + fuck[2] + fuck[3] + fuck[4]

    monkeyFucker = str(ass)

# Set to 1 if you want to the program to actually place REAL orders, 0 if not
enableOrders = 1

# Set to 1 if you want the user to be able to select max, min, or custom buy values, 0 if not
enableMaxMinCustom = 0
# If ^^ is 0, then this is used to determine pricing
defaultPurchaseOption = 2 # 1 = min, 2 = max, 3 = custom

# Universal minimum order size for Binance when trading BTC
universalMinOrder = 0.0001

# Length of the grace period
waitTime = 5

# Percent of all money in wallet that is placed for max orders
orderPercentage = 97

# Automatically create sell orders at these percentages relative to buy price
# 50% = .5x price (halved price), 100% = 1x price (no change), 200% = 2x price (doubled price), etc
maxPulloutPercent = 200 # Max price to sell at
minPulloutPercent = 100 # Min price to sell at

# Public and secret Binance API keys, respectively
client = Client('',
                '')

# Variable to hold the orderId of the maxPrice limit order
sellOrderId = 0

# Truncates a to b decimal places (thanks Brock)
def truncate(a, b):
  return math.floor(a * 10 ** b) / 10 ** b

# Function to place a BUY order
def placeBuyOrder(amountToBuy):
    # Truncates the amount of payCoin to the stepSize required by the market
    roundedAmountBuyable = truncate(amountToBuy, decimalPlaces)

    if (roundedAmountBuyable >= float(minQuantity) and roundedAmountBuyable <= float(maxQuantity)):
        # Sells max amount of payCoin for buyCoin
        if (enableOrders == 1):
            roundedAmountBuyable2 = (client.get_symbol_ticker(symbol=buyCoin + payCoin))
            amountBuyableDecimalsA = truncate((float(payCoinBalance["free"]) / float(roundedAmountBuyable2["price"])), decimalPlaces)
            amountBuyableDecimals2 = truncate((amountBuyableDecimalsA * orderPercentage) / 100, decimalPlaces)
            print(str(orderPercentage) + "% of max: " + str(amountBuyableDecimals2) + " " + buyCoin)
            output = "{:.8f}".format(amountBuyableDecimals2)
            if (priceFilterMinPrice == 0.00000001):
                output = "{:.8f}".format(amountBuyableDecimals2)
            elif (priceFilterMinPrice == 0.0000001):
                output = "{:.7f}".format(amountBuyableDecimals2)
            elif (priceFilterMinPrice == 0.000001):
                output = "{:.6f}".format(amountBuyableDecimals2)
            elif (priceFilterMinPrice == 0.00001):
                output = "{:.5f}".format(amountBuyableDecimals2)
            output2 = float(output)
            #output2 -= (stepSize * minQuantity)
            output2 = truncate(output2, decimalPlaces)
            print("Market buying " + str(output2) + " " + buyCoin)
            order = client.order_market_buy(symbol = buyCoin + payCoin, quantity = output2)
    else:
        print("Error! Amount being bought is out of bounds (" + str(roundedAmountBuyable) + ")! Order not placed.")

# Function to place a SELL order. 'type' parameter can be either "market" or "limit", case-sensitive.
def placeSellOrder(type, amountToSell):
    # Truncates the amount of buyCoin to the stepSize required by the market
    roundedAmountSellable = truncate(float(buyCoinBalance["free"]), decimalPlaces)

    if (type == "market"):
        print("Market selling " + str(roundedAmountSellable) + " " + buyCoin)
    elif (type == "limit"):
        print("Limit selling " + str(roundedAmountSellable) + " " + buyCoin)

    if (roundedAmountSellable >= float(minQuantity) and roundedAmountSellable <= float(maxQuantity)):
        if (type == "market"):
            # Sells max amount of buyCoin for payCoin
            if (enableOrders == 1):
                order = client.order_market_sell(symbol = buyCoin + payCoin, quantity = roundedAmountSellable)
        elif (type == "limit"):
            # Sells max amount of buyCoin for payCoin
            if (enableOrders == 1):
                output = "{:.8f}".format(maxPrice)
                if (priceFilterMinPrice == 0.00000001):
                    output = "{:.8f}".format(maxPrice)
                elif (priceFilterMinPrice == 0.0000001):
                    output = "{:.7f}".format(maxPrice)
                elif (priceFilterMinPrice == 0.000001):
                    output = "{:.6f}".format(maxPrice)
                elif (priceFilterMinPrice == 0.00001):
                    output = "{:.5f}".format(maxPrice)
                order = client.order_limit_sell(symbol = buyCoin + payCoin, quantity = roundedAmountSellable, price = output)
    else:
        print("Error! Amount being sold is out of bounds (" + str(roundedAmountSellable) + ")! Order not placed.")

# This is just for ease when programming. The final program gets this automatically from Discord
#buyCoinInput = input("Enter the coin you are buying: ")
#payCoinInput = input("Enter the coin you are paying with: ") # This will always be BTC when we're actually using it
#buyCoin = buyCoinInput.upper()
#payCoin = payCoinInput.upper()

if (useOutputTxt == 1):
    buyCoin = monkeyFucker.upper()
else:
    buyCoinInput = input("Enter the coin you are buying: ")
    buyCoin = buyCoinInput.upper()
payCoin = 'BTC'

startTime = time.time()

info = client.get_symbol_info(symbol=buyCoin + payCoin)
print("\nSome values may appear in scientific notation; they still work.")
#print(info)

# Calculates & prints the amount of payCoin in the account's wallet
payCoinBalance = client.get_asset_balance(asset=payCoin)
buyCoinBalance = client.get_asset_balance(asset=buyCoin)
print("\nAccount's wallet has " + payCoinBalance["free"] + " " + payCoin + " and " + buyCoinBalance["free"] + " " + buyCoin)
# Gets the price of buyCoin in terms of payCoin
buyCoinPrice = client.get_symbol_ticker(symbol=buyCoin + payCoin)
print("The price of " + buyCoin + " is " + buyCoinPrice["price"] + " " + payCoin)

stepSize = float(info['filters'][2]['stepSize'])

d = decimal.Decimal(str(stepSize).rstrip('0'))
decimalPlaces = abs(d.as_tuple().exponent)
#print("Precision for " + (buyCoin + payCoin) + " market is " + str(decimalPlaces) + " decimal places")
print("\nstepSize: " + str(truncate(float(info['filters'][2]['stepSize']), decimalPlaces)))

minQuantity = truncate(universalMinOrder / float(buyCoinPrice["price"]) + stepSize, decimalPlaces)
print("minQuantity: " + str(minQuantity))
maxQuantity = truncate(float(info['filters'][2]['maxQty']), decimalPlaces)
print("maxQuantity: " + str(truncate(float(info['filters'][2]['maxQty']), decimalPlaces)))

priceFilterMinPrice = info['filters'][0]['minPrice']
print("price filter min price: " + priceFilterMinPrice)
#priceFilterTickPrice = info['filters'][0]['tickPrice']

# Calculates the amount of buyCoin that is obtainable with the amount of owned payCoin
amountBuyableDecimals = truncate((float(payCoinBalance["free"]) / float(buyCoinPrice["price"])), decimalPlaces)
amountBuyable = truncate(amountBuyableDecimals, decimalPlaces)
print("There is " + str(amountBuyable) + " " + buyCoin + " buyable using " + payCoin + "\n")

if (enableMaxMinCustom == 1):
    runTypeInput = input("Do you want to buy 'max', 'min', or 'custom'?: ")
    runType = runTypeInput.upper()
    if (runType == "CUSTOM"):
        customAmount = float(input("Enter custom amount in " + buyCoin + ": "))
    if (runType == "MAX"):
        placeBuyOrder(amountBuyable)
    elif (runType == "MIN"):
        placeBuyOrder(minQuantity)
    elif (runType == "CUSTOM"):
        placeBuyOrder(customAmount)
elif (enableMaxMinCustom == 0):
    if (defaultPurchaseOption == 1): # min
        placeBuyOrder(minQuantity)
    elif (defaultPurchaseOption == 2): # max
        placeBuyOrder(amountBuyable)
    elif (defaultPurchaseOption == 3): #custom
        customAmount1 = float(input("Enter custom amount in " + buyCoin + ": "))
        placeBuyOrder(customAmount1)

try:
    orderInfo = client.get_my_trades(symbol=buyCoin + payCoin)
    #print(orderInfo[len(orderInfo) - 1])
    integerId = int(orderInfo[len(orderInfo) - 1]["orderId"])
except:
    print("\nError! You do not have any " + buyCoin + payCoin + " trades!")
    sys.exit()

print("\nWaiting for order #" + str(integerId) + " to be filled...")
purchasePrice = 0
while (1 == 1):
    try:
        checkOrder = client.get_order(symbol=buyCoin + payCoin, orderId=integerId)
    except:
        continue;
    if (checkOrder["status"] == "FILLED"):
        orderInfo = client.get_my_trades(symbol=buyCoin + payCoin)
        purchaseTime = orderInfo[len(orderInfo) - 1]["time"]
        purchasePrice = orderInfo[len(orderInfo) - 1]["price"]
        currentServerTime = client.get_server_time()
        print("Order #" + str(integerId) + " filled at " + str(purchasePrice) + " " + payCoin + " at time " + str(purchaseTime) + ".")
        print("That's " + str((currentServerTime["serverTime"]) - purchaseTime) + " time units ago!\n")
        break

# Calculates and prints the high and low coin value thresholds that we would pull out at
maxPrice = float(purchasePrice) * (maxPulloutPercent / 100.0)
maxPriceFormatted = "{:.8f}".format(maxPrice)
minPrice = float(purchasePrice) * (minPulloutPercent / 100.0)
minPriceFormatted = "{:.8f}".format(minPrice)
print("Sell at or above " + maxPriceFormatted + " " + buyCoin + " (" + str(maxPulloutPercent) + "%)")
print("Sell at or below " + minPriceFormatted + " " + buyCoin + " (" + str(minPulloutPercent) + "%)\n")

# Gets the amount of buyCoin that is in the account's wallet
buyCoinBalance = client.get_asset_balance(asset=buyCoin)
buyCoinBalanceFloat = truncate(float(buyCoinBalance["free"]), decimalPlaces)
#print(buyCoinBalanceFloat)
placeSellOrder("limit", buyCoinBalanceFloat)

while (1 == 1):
    try:
        maxSellOrder = client.get_open_orders(symbol=buyCoin + payCoin)
        maxSellOrderId = int(maxSellOrder[len(maxSellOrder) - 1]["orderId"])
        break
    except:
        continue

print("Sell order id: #" + str(maxSellOrderId))

endTime = time.time()
print("\nTime taken: " + str(endTime - startTime) + " sec")

# Waits waitTime seconds before scanning the price, to avoid instant pullouts
# Think of this as a grace period for the coin to fluctuate
print("\nWaiting " + str(waitTime) + " seconds before continuing (grace period)...\n")
time.sleep(waitTime)

# Infinitely checks the price of the coin until one of the high or low thresholds is met
print("------- ROLLING PRICE CHECKER (Only reflects changes) -------")
rollingCounter = 0
previousPrice = 0

# Infinite loop that will only ever stop once a sell order is placed. Meat & potatoes of the program.
while (1 == 1):

    # Keeps count of what iteration of the infinite loop we're in
    rollingCounter += 1

    # Gets the current price of buyCoin from Binance API
    rollingBuyCoinPrice = client.get_symbol_ticker(symbol = buyCoin + payCoin)

    # Checks to see if the read price of buyCoin is the same as the previously recorded price
    # If prev and current prices differ, update prev price
    if (previousPrice != float(rollingBuyCoinPrice["price"])):
        previousPrice = float(rollingBuyCoinPrice["price"])
    # If prev and current prices are the same, restart loop (this saves resources)
    else:
        continue;

    # Ratio of current price and price purchased at. 1.0 = break even, <1.0 = loss, >1.0 = gain
    boughtCurrentRatio = truncate(float(rollingBuyCoinPrice["price"]) / float(purchasePrice), 8)

    # Converts the boughtCurrentRatio to a percentage
    percentDiff = truncate((boughtCurrentRatio - 1) * 100, 8) # Float version
    percentDiffString = str(percentDiff) # String version

    # Decides if the printed percentage change will have positive, negative, or even attributes
    printColor = Fore.RED # Init printColor
    # If positive, add a + and make it green
    if (boughtCurrentRatio > 1):
        percentDiffString = "+" + str(percentDiff)
        printColor = Fore.GREEN
    # If even, add a +- and make it yellow
    elif(boughtCurrentRatio == 1):
        percentDiffString = "+-" + str(percentDiff)
        printColor = Fore.YELLOW
    # If negative, make it red (negative sign is already part of percentDiffString in this case)
    else:
        printColor = Fore.RED

    # Prints current price of the buyCoin, along with the percentage change
    print(str(rollingCounter) + ": Current price of " + buyCoin + ": " + rollingBuyCoinPrice["price"] + " " +
          payCoin + " (" + printColor + percentDiffString + "%" + Style.RESET_ALL + ")")

    # The money has reached minPrice, sell :(
    if (float(rollingBuyCoinPrice["price"]) <= minPrice):
        print("\n" + buyCoin + " has reached " + str(minPulloutPercent) + "%... selling :(")

        while (1 == 1):
            try:
                result = client.cancel_order(symbol=buyCoin + payCoin, orderId=maxSellOrderId)
                print("Cancelled sell order #" + str(maxSellOrderId))
                break
            except:
                continue

        # Gets the amount of buyCoin that is in the account's wallet & places market sell to minimize losses
        buyCoinBalance = client.get_asset_balance(asset=buyCoin)
        placeSellOrder("market", truncate(float(buyCoinBalance["free"]), decimalPlaces))
        break










