package main

import (
	"crypto/sha1"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"math/rand"
	"strconv"

	"github.com/hyperledger/fabric/core/chaincode/shim"
	sc "github.com/hyperledger/fabric/protos/peer"
)

var letterRunes = []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") //Criar sequencia de letras

func AleatString(n int) string { //Function to create a sequence of random numbers
	b := make([]rune, n)
	for i := range b {
		b[i] = letterRunes[rand.Intn(len(letterRunes))]
	}
	return string(b)
}

func Encode(msg string) string { //Function to create a sha-1 hash
	h := sha1.New()
	h.Write([]byte(msg))
	sha1_hash := hex.EncodeToString(h.Sum(nil))
	return sha1_hash
}

func Round(n float64) float64 {
	numberRounded := float64(int(n*10000)) / 10000
	return numberRounded
}

type SmartContract struct {
}

type Vehicle struct { //"vehi-"
	Hash         string  `json:"Hash"`
	VIN          string  `json:"VIN"`
	Co2Emitted   float64 `json:"Co2Emitted"`
	manufacturer string  `json:"Manufacturer"`
}

type Manufacturer struct { //"manu-""
	Co2Tot            float64 `json:"Co2_Tot"`
	CarbonBalance     float64 `json:"CarbonBalance"`
	Balance_Fiduciary float64 `json:"Balance_Fiduciary"`
}

type TransactionOrder struct { //"trans-"
	OwnerOrder      string  `json:"OwnerOrder"`
	TransactionType string  `json:"TransactionType"` // 1: Sell carbon -- 2: Buy carbon
	BalanceOffered  float64 `json:"BalanceOffered"`
	BuyerID         string  `json:"BuyerID"`
	AmountLastBid   float64 `json:"AmountLastBid"`
	StatusOrder     string  `json:"StatusOrder"` //Recent - Progress - Closed
}

func (s *SmartContract) Init(stub shim.ChaincodeStubInterface) sc.Response {
	return shim.Success(nil)
}

func (s *SmartContract) Invoke(stub shim.ChaincodeStubInterface) sc.Response {
	fn, args := stub.GetFunctionAndParameters()

	if fn == "registerVehicle" {
		return s.registerVehicle(stub, args)
	} else if fn == "registerManufacturer" {
		return s.registerManufacturer(stub, args)
	} else if fn == "registerCredit" {
		return s.registerCredit(stub, args)
	} else if fn == "announceOrder" {
		return s.announceOrder(stub, args)
	} else if fn == "bidOrder" {
		return s.bidOrder(stub, args)
	} else if fn == "closeOrder" {
		return s.closeOrder(stub, args)
	}
	return shim.Error("Chaincode does not support this function")
}

func (s *SmartContract) registerManufacturer(stub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 1 {
		return shim.Error("1 single argument was expected")
	}

	nameManu := args[0]

	manufacturerInfor := Manufacturer{
		Co2Tot:            0.0,
		CarbonBalance:     0.0,
		Balance_Fiduciary: 100000.0,
	}

	manufacturerAsBytes, _ := json.Marshal(manufacturerInfor)

	idCdgLedger := "manu-" + nameManu

	stub.PutState(idCdgLedger, manufacturerAsBytes)

	fmt.Println("Success in registering manufacturers")
	return shim.Success(nil)
}

func (s *SmartContract) registerVehicle(stub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 4 {
		return shim.Error("4 arguments were expected... Try again!")
	}

	vim := args[0]
	hash := args[1]
	co2 := args[2]
	manuName := args[3]

	co2VehiFloat, err := strconv.ParseFloat(co2, 64)

	//Create Struct to manipulate vehicle information
	userVehicle := Vehicle{
		Hash:         hash,
		VIN:          vim,
		Co2Emitted:   co2VehiFloat,
		manufacturer: manuName,
	}

	//Retrieving user data
	manufacturerAsBytes, err := stub.GetState("manu-" + manuName)
	if err != nil || manufacturerAsBytes == nil {
		manufacturerInfor := Manufacturer{
			Co2Tot:            0.0,
			CarbonBalance:     0.0,
			Balance_Fiduciary: 100000.0,
		}

		manufacturerInfor.Co2Tot += co2VehiFloat

		VehicleAsBytes, _ := json.Marshal(userVehicle)
		manufacturerAsBytes, _ = json.Marshal(manufacturerInfor)

		stub.PutState(("manu-" + manuName), manufacturerAsBytes)
		stub.PutState(("vehi-" + vim), VehicleAsBytes)

		fmt.Println("Success in registering Vehicle and manufacturer")
		return shim.Success(nil)

	}

	//Criando Struct para encapsular os dados do Vehicle
	manufacturer := Manufacturer{}
	json.Unmarshal(manufacturerAsBytes, &manufacturer)
	manufacturer.Co2Tot += co2VehiFloat

	VehicleAsBytes, _ := json.Marshal(userVehicle)
	manufacturerAsBytes, _ = json.Marshal(manufacturer)

	stub.PutState(("manu-" + manuName), manufacturerAsBytes)
	stub.PutState(("vehi-" + vim), VehicleAsBytes)

	fmt.Println("Success registering Vehicle")
	return shim.Success(nil)
}

func (s *SmartContract) registerCredit(stub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 1 {
		return shim.Error("1 single argument was expected... Try again!")
	}

	idmanufacturer := args[0]

	//Retrieving user data
	manufacturerAsBytes, err := stub.GetState(idmanufacturer)
	if err != nil || manufacturerAsBytes == nil {
		return shim.Error("Your manufacturer does not exist.")
	}

	//Criando Struct para encapsular os dados do Vehicle
	manufacturer := Manufacturer{}
	json.Unmarshal(manufacturerAsBytes, &manufacturer)

	if manufacturer.Co2Tot == 0.0 {
		fmt.Println("No carbon emission was computed for the manufacturer: " + idmanufacturer)
		return shim.Success(nil)
	}

	var saldo = 50000.0 - manufacturer.Co2Tot
	manufacturer.CarbonBalance = saldo
	manufacturer.Co2Tot = 0.0

	manufacturerAsBytes, _ = json.Marshal(manufacturer)

	stub.PutState(idmanufacturer, manufacturerAsBytes)

	fmt.Println("Successfully computed carbon balance: " + idmanufacturer)
	return shim.Success(nil)
}

func (s *SmartContract) announceOrder(stub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 3 {
		fmt.Println("3 arguments were expected")
		return shim.Error("3 arguments were expected... Try again!")
	}

	ownerOrder := args[0]
	TransactionType := args[1]
	Offerbalance := args[2]

	balanceOfferFloat, err := strconv.ParseFloat(Offerbalance, 64)

	//Checking if the manufacturer really exists
	manufacturerAsBytes, err := stub.GetState(ownerOrder)
	if err != nil || manufacturerAsBytes == nil {
		fmt.Println("Your manufacturer does not exist")
		return shim.Error("Your manufacturer does not exist.")
	}

	//Creating Struct to encapsulate manufacturer data
	manufacturer := Manufacturer{}
	json.Unmarshal(manufacturerAsBytes, &manufacturer)

	if TransactionType == "sell" {
		if balanceOfferFloat > manufacturer.CarbonBalance {
			fmt.Println("You don't have enough carbon balance")
			return shim.Error("You don't have enough carbon balance")
		}
		manufacturer.CarbonBalance -= balanceOfferFloat
	}

	if TransactionType == "buy" {
		if balanceOfferFloat > manufacturer.Balance_Fiduciary {
			fmt.Println("You don't have enough trust balance")
			return shim.Error("You don't have enough trust balance")
		}
		manufacturer.Balance_Fiduciary -= balanceOfferFloat
	}

	salesOrder := TransactionOrder{
		BuyerID:         "null",
		AmountLastBid:   0.0,
		StatusOrder:     "Recent",
		OwnerOrder:      ownerOrder,
		BalanceOffered:  balanceOfferFloat,
		TransactionType: TransactionType,
	}

	salesOrderAsBytes, _ := json.Marshal(salesOrder)
	manufacturerAsBytes, _ = json.Marshal(manufacturer)

	idOrder := "trans-" + Encode(AleatString(10))

	stub.PutState(ownerOrder, manufacturerAsBytes)
	stub.PutState(idOrder, salesOrderAsBytes)

	fmt.Println("order of " + TransactionType + " successfully announced!")
	return shim.Success(nil)
}

func (s *SmartContract) bidOrder(stub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 3 {
		fmt.Println("2 arguments were expected")
		return shim.Error("Era esperado 2 argumentos... Tente novamente!")
	}

	idTransaction := args[0]
	valorLance := args[1]
	BuyerID := args[2]

	valueLanceFloat, err := strconv.ParseFloat(valorLance, 64)

	//Retrieving transaction data
	OrderTransactionAsBytes, err := stub.GetState(idTransaction)
	if err != nil || OrderTransactionAsBytes == nil {
		fmt.Println("Your owner does not exist")
		return shim.Error("Your owner does not exist.")
	}

	//Retrieving owner data
	manufacturerAsBytes, err := stub.GetState(BuyerID)
	if err != nil || OrderTransactionAsBytes == nil {
		fmt.Println("Your manufacturer does not exist")
		return shim.Error("Your manufacturer does not exist.")
	}

	//Encapsulating transaction order and manufacturer data
	order := TransactionOrder{}
	json.Unmarshal(OrderTransactionAsBytes, &order)

	if order.StatusOrder == "Closed" {
		fmt.Println("This order is closed")
		return shim.Error("This order can no longer be moved as the owner has closed it.")
	}

	if BuyerID == order.BuyerID {
		fmt.Println("You cannot bid twice")
	}

	manufacturer := Manufacturer{}
	json.Unmarshal(manufacturerAsBytes, &manufacturer)

	if valueLanceFloat > manufacturer.Balance_Fiduciary && order.TransactionType == "sell" {
		fmt.Println("You don't have enough trust balance")
		return shim.Error("You don't have enough trust balance.")
	}

	if valueLanceFloat > manufacturer.CarbonBalance && order.TransactionType == "buy" {
		fmt.Println("You don't have enough carbon balance")
		return shim.Error("You don't have enough carbon balance.")
	}

	if order.AmountLastBid > valueLanceFloat {
		fmt.Println("Your bid is lower than the previous bid")
		return shim.Error("Your bid is lower than the previous bid.")
	}

	order.StatusOrder = "Progress"
	order.AmountLastBid = valueLanceFloat
	order.BuyerID = BuyerID

	OrderTransactionAsBytes, _ = json.Marshal(order)
	stub.PutState(idTransaction, OrderTransactionAsBytes)

	fmt.Println("Successful bid registered")

	return shim.Success(nil)
}

func (s *SmartContract) closeOrder(stub shim.ChaincodeStubInterface, args []string) sc.Response {

	if len(args) != 2 {
		fmt.Println("2 arguments were expected")
		return shim.Error("2 arguments were expected... Try again!")
	}

	idTransaction := args[0]
	ownerid := args[1]

	//Retrieving transaction data
	OrderTransactionAsBytes, err := stub.GetState(idTransaction)
	if err != nil || OrderTransactionAsBytes == nil {
		fmt.Println("This order does not exist")
		return shim.Error("This order does not exist")
	}

	//Encapsulating manufacturer data
	order := TransactionOrder{}
	json.Unmarshal(OrderTransactionAsBytes, &order)

	if order.OwnerOrder != ownerid {
		fmt.Println("You do not own this order")
		return shim.Error("You do not own this order")
	}

	//Retrieving owner data
	ownerAsBytes, err := stub.GetState(order.OwnerOrder)
	if err != nil || OrderTransactionAsBytes == nil {
		fmt.Println("Your owner does not exist")
		return shim.Error("Your owner does not exist")
	}

	//Encapsulating manufacturer data
	owner := Manufacturer{}
	json.Unmarshal(ownerAsBytes, &owner)

	//Retrieving buyer data
	buyerAsBytes, err := stub.GetState(order.BuyerID)
	if err != nil || OrderTransactionAsBytes == nil {
		fmt.Println("Your buyer does not exist")
		return shim.Error("Your buyer does not exist")
	}

	//Encapsulating manufacturer data
	buyer := Manufacturer{}
	json.Unmarshal(buyerAsBytes, &buyer)

	if order.BuyerID == "null" {
		fmt.Println("There were no bids for this order")

		return shim.Error("There were no bids for this order")
	}

	if order.TransactionType == "sell" {
		owner.Balance_Fiduciary += order.AmountLastBid
		buyer.Balance_Fiduciary -= order.AmountLastBid
		order.StatusOrder = "Closed"
	}

	if order.TransactionType == "buy" {
		owner.CarbonBalance += order.AmountLastBid
		buyer.CarbonBalance -= order.AmountLastBid
		order.StatusOrder = "Closed"
	}

	OrderTransactionAsBytes, _ = json.Marshal(order)
	ownerAsBytes, _ = json.Marshal(owner)
	buyerAsBytes, _ = json.Marshal(buyer)

	stub.PutState(idTransaction, OrderTransactionAsBytes)
	stub.PutState(ownerid, ownerAsBytes)
	stub.PutState(order.BuyerID, buyerAsBytes)

	fmt.Println("Transaction successfully closed")
	return shim.Success(nil)

}

func main() {
	if err := shim.Start(new(SmartContract)); err != nil {
		fmt.Printf("Error compiling Smart Contract: %s\n", err)
	}
}
