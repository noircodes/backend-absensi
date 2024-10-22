# ===== Module & Library
import re

from bson.objectid import ObjectId

# ===== Header
from fastapi import HTTPException

from config.config import ENVIRONMENT
from utils.datatypes_util import ObjectIdStr

regex_email = re.compile(
    r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)


# ===== Function

# ===== Class

# ===== Main
class ValidationUtils:
    @staticmethod
    def validate_phone(str_phone: str, min: int = 7, max: int = 14):
        """Function to validate phone number"""

        if not str_phone.isnumeric():
            raise HTTPException(status_code=400, detail="Nomor telepon bukan berupa angka.")

        if not min < len(str_phone) < max:
            raise HTTPException(status_code=400, detail=f"Panjang nomor telepon antara {min} - {max} angka.")

        return True

    @staticmethod
    def validate_email(str_email: str):
        """Function to validate email"""

        if not re.fullmatch(regex_email, str_email):
            raise HTTPException(status_code=400, detail="Format email tidak valid. contoh 'jhon.doe@email.com'.")

        return True

    @staticmethod
    def validate_password(password: str, min: int = 6, max: int = 24):
        """Function to validate password"""

        # if not min <= len(password) <= max:
        #     raise HTTPException(status_code=400, detail=f"Panjang password antara {min} - {max} karakter.")

        # if not re.search("[0-9]", password) and not len(password) > 6:
        #     return HTTPException(status_code=400, detail=f"Password minimal 6 karakter dengan kombinasi huruf dan angka.")

        has_letter = False
        has_digit = False

        for char in password:
            if char.isalpha():
                has_letter = True
            elif char.isdigit():
                has_digit = True
        if has_digit and has_letter and len(password) >= 6:
            print("Password is valid")
            pass
        else:
            print("Not a valid password")
            raise HTTPException(status_code=400, detail=f"Password minimal 6 karakter dengan kombinasi huruf dan angka.")

        return True

    @staticmethod
    def validate_objectid(str_objectid: str | ObjectIdStr, varName: str) -> ObjectId:
        """Function to validate ObjectId"""

        if not ObjectId.is_valid(str_objectid):
            raise HTTPException(status_code=400, detail=f"ObjectId '{varName}' tidak valid.")

        try:
            oid = ObjectId(str_objectid)
            return oid
        except Exception as err:
            if ENVIRONMENT == "development":
                print(err)
            raise HTTPException(status_code=400, detail=f"ObjectId '{varName}' tidak valid.")
