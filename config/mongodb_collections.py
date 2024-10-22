from config.config import DB_ABSENSI
from config.mongodb_type_checking import TMongoCollection

DB_USER: TMongoCollection = DB_ABSENSI["user"]
DB_ATTENDANCE: TMongoCollection = DB_ABSENSI["attendance"]