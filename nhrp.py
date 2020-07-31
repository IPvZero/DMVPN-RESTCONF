import requests
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.apis import http_method


def nhrpconf(task, chained_url, headers):
    restconf_url = f"https://{task.host.hostname}/restconf/"

    task.run(
        task=http_method,
        name="RESTCONF PUT_POST",
        method="put",
        url=restconf_url + chained_url,
        auth=("john", "cisco"),
        headers=headers["put_post"],
        verify=False,
        json=task.host["int_configure"]
)

def cryptoconf(task, chained_url, headers):
    restconf_url = f"https://{task.host.hostname}/restconf/"

    task.run(
        task=http_method,
        name="RESTCONF PUT_POST",
        method="put",
        url=restconf_url + chained_url,
        auth=("john", "cisco"),
        headers=headers["put_post"],
        verify=False,
        json=task.host["crypto_configure"]
)

def eigrpconf(task, chained_url, headers):
    restconf_url = f"https://{task.host.hostname}/restconf/"

    task.run(
        task=http_method,
        name="RESTCONF PUT_POST",
        method="put",
        url=restconf_url + chained_url,
        auth=("john", "cisco"),
        headers=headers["put_post"],
        verify=False,
        json=task.host["router_configure"]
)

def main():
    requests.packages.urllib3.disable_warnings()

    nhrp_url = "data/native/interface"
    crypto_url = "data/native/crypto"
    eigrp_url = "data/native/router"
    headers = {
        "get": {"Accept": "application/yang-data+json"},
        "put_post": {
            "Content-Type": "application/yang-data+json",
            "Accept": "application/yang-data+json, application/yang-data.errors+json",
        },
    }

    nr = InitNornir()
    crypto_result = nr.run(task=cryptoconf,name="PUSHING CRYPTOGRAPHY VIA RESTCONF",chained_url=crypto_url,headers=headers,)
    nhrp_result = nr.run(task=nhrpconf,name="PUSHING NHRP VIA RESTCONF",chained_url=nhrp_url,headers=headers,)
    eigrp_result = nr.run(task=eigrpconf,name="PUSHING EIGRP VIA RESTCONF",chained_url=eigrp_url,headers=headers,)
    print_result(crypto_result)
    print_result(nhrp_result)
    print_result(eigrp_result)

if __name__ == "__main__":
    main()
