from core.utils import BaseEnum


class StateTypeEnum(BaseEnum):
    STATE = 10
    UNION_TERITORY = 20


class StoreTypesEnum(BaseEnum):
    LAUNDRY = 10
    SELLING_WHOLESALE = 20
    SELLING_RETAIL = 30
    SELLING_WHOLESALE_WITH_LAUNDRY = 40
    SELLING_RETAIL_WITH_LAUNDRY = 50
    CUT_PIECE_CENTER = 60


class UserTypeEnum(BaseEnum):
    CUSTOMER = 10
    STORE_EMPLOYEE = 20
