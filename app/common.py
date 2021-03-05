from rest_framework.exceptions import ValidationError

import requests
from bs4 import BeautifulSoup

from owners.excepts import BusinessLicenseNumberException


def check_owner_number(business_license_number):

    # 하이픈 값을 받았다면 지워주기
    if '-' in business_license_number:
        business_license_number.replace('-', '')
    URL = "https://teht.hometax.go.kr/wqAction.do?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn=false&realScreenId="
    xml = f'<map id="ATTABZAA001R08"><pubcUserNo/><mobYn>N</mobYn><inqrTrgtClCd>1</inqrTrgtClCd><txprDscmNo>{business_license_number}</txprDscmNo><dongCode>18</dongCode><psbSearch>Y</psbSearch><map id="userReqInfoVO"/></map><nts<nts>nts>19lTaNFpjNw6WO5INQpInNlIdcjIGeY3LoeHgMok08'
    headers = {'Content-Type': 'text/html'}

    res = requests.post(URL, data=xml, headers=headers)
    if 200 == res.status_code:
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        print(soup)
        result = soup.find('smpcbmantrtcntn').text
        added_value = soup.find('trtcntn').text
        if '않은' in result:
            raise BusinessLicenseNumberException
        else:
            return added_value, True
    else:
        # return res.text, False
        raise ValidationError
