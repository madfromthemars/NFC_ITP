import json

import vobject
from vobject import vcard


def VCardFile(user):
    file = vobject.vCard()
    file.add('N')
    file.n.value = vcard.Name(family=user.last_name, given=user.first_name)

    file.add("FN")
    file.fn.value = user.first_name + ' ' + user.last_name

    file.add("NICKNAME")
    file.nickname.value = user.username

    file.add('BDAY')
    file.bday.value = str(user.birthday)

    file.add("EMAIL")
    file.email.value = user.email

    file.add('TEL')
    file.tel.value = user.phone

    try:
        work = user.work_info
        if type(work) is str:
            work = eval(work)

        file.add("ORG")
        file.org.value = work.get('org' or '')
        file.add('ROLE')
        file.role.value = work.get('role' or '')
    except Exception:
        print("Without Work Info")

    address = user.address
    try:
        if type(address) is str:
            address = eval(address)
        file.add("ADR")
        file.adr.value = vcard.Address(
            street=(address.get('address') or ""),
            city=(address.get('city') or ""),
            region=(address.get('city') or ""),
            country=(address.get('city') or ""))
    except:
        print("Without Address")

    try:
        f = open(f'./files/user_{user.id}.vcf', 'w')
        f.write((file.serialize()))
        f.close()
    except Exception:
        print('---VCF Wrong---')
