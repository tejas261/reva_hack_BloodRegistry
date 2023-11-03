from web3 import Web3
from solcx import compile_standard, install_solc
import json
from os.path import exists
private_key = "0x5df88fc582fcea7b9d612fea494b5ca24bff1df9bf37a8715f471095d356955a"
my_address = "0xa08b081eEeD834FAEa39EeB242EBF79ce24F031E"
def deploy(filename,contractName):
    with open(f"Contracts/{filename}", "r") as file:
        contract_file = file.read()
    install_solc("0.8.0")
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {".sol": {"content": contract_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.0",
    )
    # with open("compiled_code.json5", "w") as file:
    #     json.dump(compiled_sol, file)

    # Get Bytecode
    bytecode = compiled_sol["contracts"][".sol"][contractName]["evm"]["bytecode"]["object"]
    # Get ABI
    abi = compiled_sol["contracts"][".sol"][contractName]["abi"]
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    chain_id = 1337
    

    cntrct = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Get the latest Transaction
    nonce = w3.eth.getTransactionCount(my_address)
    #  1.Build Transaction
    #  2.Sign Transaction
    #  3.Send Transaction
    print("Building Transaction")
    transaction = cntrct.constructor().buildTransaction({
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce})
    print("Signing Transaction")
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    # Send signed transaction to blockchain
    print("Deploying signed transaction to blockchain")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Deployed")
    new_data = {filename:
        {
            'abi': abi,
            'contract_address': tx_receipt.contractAddress
        }
    }
    
    with open("deployed_contract.json", 'r+') as file:
        try:
            data = json.load(file)
            data.update(new_data)
            file.seek(0)
            json.dump(data, file)
        except:
            json.dump(new_data,file)

def register_blood_bank(id, name, email, address, password, licence_no,lat,longi):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['BloodBankRegistry.sol']['abi']
    contract_address = data['BloodBankRegistry.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    chain_id = 1337
    blood_bank = w3.eth.contract(abi=abi, address=contract_address)
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = blood_bank.functions.add(name, id, email, licence_no, password, address,lat,longi).buildTransaction({
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce
    })
    sign_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress
def bblogin(id):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['BloodBankRegistry.sol']['abi']
    contract_address = data['BloodBankRegistry.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    blood_bank = w3.eth.contract(abi=abi, address=contract_address)
    return blood_bank.functions.login(id).call()

def register_hospital(id, name, email, address, password, licence_no, lat,longi):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['HospitalRegistry.sol']['abi']
    contract_address = data['HospitalRegistry.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    chain_id = 1337
    blood_bank = w3.eth.contract(abi=abi, address=contract_address)
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = blood_bank.functions.add(name, id, email, licence_no, password, address, lat,longi).buildTransaction({
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce
    })
    sign_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress
def hosplogin(id):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['HospitalRegistry.sol']['abi']
    contract_address = data['HospitalRegistry.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    hospital = w3.eth.contract(abi=abi, address=contract_address)
    return hospital.functions.login(id).call()

def register_donor(d_name, d_id, d_email, d_aadhar_no, d_blood_type, d_dob):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['Donor.sol']['abi']
    contract_address = data['Donor.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    chain_id = 1337
    blood_bank = w3.eth.contract(abi=abi, address=contract_address)
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = blood_bank.functions.badd(d_name, d_id, d_email, d_aadhar_no, d_blood_type, d_dob).buildTransaction({
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce
    })
    sign_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress
def blood_bank_get_info(bb_id):
    return bblogin(bb_id)
def collect_sample(blood_type,donor_id, bb_id, blood_id,tod_date):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['BloodSample.sol']['abi']
    contract_address = data['BloodSample.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    chain_id = 1337
    blood_sample = w3.eth.contract(abi=abi, address=contract_address)
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = blood_sample.functions.collected(donor_id,bb_id,blood_id,blood_type,tod_date).buildTransaction({
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce
    })
    sign_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress

def retreive_collected_samples(bb_id):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['BloodSample.sol']['abi']
    contract_address = data['BloodSample.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    blood_sample = w3.eth.contract(abi=abi, address=contract_address)
    return blood_sample.functions.bbank_no_samples_collected(bb_id).call()

def change_sample_state(blood_id,state):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['BloodSample.sol']['abi']
    contract_address = data['BloodSample.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    chain_id = 1337
    blood_sample = w3.eth.contract(abi=abi, address=contract_address)
    nonce = w3.eth.getTransactionCount(my_address)
    if int(state) == 1:
        transaction = blood_sample.functions.tested(blood_id, "OK").buildTransaction({
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce
        })
    elif int(state) == 2:
        transaction = blood_sample.functions.tested(blood_id,"NOT OK").buildTransaction({
                    "gasPrice": w3.eth.gas_price,
                    "chainId": chain_id,
                    "from": my_address,
                    "nonce": nonce
                })
    elif int(state) == 3:
        transaction = blood_sample.functions.expired(blood_id).buildTransaction({
            "gasPrice": w3.eth.gas_price,
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce
        })
    sign_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress


def list_samples_of_blood_type(blood_type):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['BloodSample.sol']['abi']
    contract_address = data['BloodSample.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    blood_sample = w3.eth.contract(abi=abi, address=contract_address)
    return blood_sample.functions.eligible_blood_bags(blood_type).call()

def hospital_get_info(h_id):
    return hosplogin(h_id)

def hospital_request_blood(blood_id, h_id, a_id):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['BloodSample.sol']['abi']
    contract_address = data['BloodSample.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    chain_id = 1337
    blood_sample = w3.eth.contract(abi=abi, address=contract_address)
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = blood_sample.functions.requested(blood_id, h_id, a_id).buildTransaction({
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce
    })
    sign_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt.contractAddress
def fetch_agreement_contract(address):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['BloodSample.sol']['abi']
    contract_address = data['BloodSample.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    blood_sample = w3.eth.contract(abi=abi, address=contract_address)
    return blood_sample.functions.get_agreement_details(address).call()
def get_hospital_agreements(h_id):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['BloodSample.sol']['abi']
    contract_address = data['BloodSample.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    blood_sample = w3.eth.contract(abi=abi, address=contract_address)
    addresses = blood_sample.functions.query_agreement_for_hospital(h_id).call()
    agreements = []
    for address in addresses:
        agreements.append(fetch_agreement_contract(address))
    return agreements
def getBloodType(d_id):
    with open('blood_bank/deployed_contract.json', 'r') as file:
        data = json.load(file)
    abi = data['Donor.sol']['abi']
    contract_address = data['Donor.sol']['contract_address']
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8550"))
    chain_id = 1337
    donor = w3.eth.contract(abi=abi, address=contract_address)
    nonce = w3.eth.getTransactionCount(my_address)
    return donor.functions.donor_details_from_aadhar(d_id).call()

    
#*************** DEPLOY CONTRACTS ***************
# deploy("HospitalRegistry.sol", "Hospitals")
# deploy("BloodBankRegistry.sol", "BloodBank")
# deploy("BloodSample.sol", "BloodSample")
# deploy("Donor.sol", "BloodDonor")


