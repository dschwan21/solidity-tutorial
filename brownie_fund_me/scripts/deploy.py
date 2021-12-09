from brownie import FundMe
from scripts.helpful_scripts import get_account


def deploy_fund_me():
    account = get_account()
    fund_me = FundMe.deploy({"from": account})
    print(f"FundMe deployed at {fund_me.address}")


def main():
    deploy_fund_me()
