"""This module contains the Store model along with StoreDetail and StoreContactDetail models."""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ARRAY, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from azra_bills_api.core.utils import BaseEnum, ULIDGenerator
from azra_bills_api.models import BaseModalWithSoftDelete

if TYPE_CHECKING:
    from azra_bills_api.admin.models import City, Country, Holiday, SAASAdmin, State


class Store(BaseModalWithSoftDelete):
    """Represents a store in the database.

    This class defines the structure and relationships for the 'stores' table.

    Attributes:
        id (str): The primary key of the store.

        created_by_id (int): The ID of the user who created the store.
        created_by (SAASAdmin): The relationship to the SAASAdmin model.

        name (str): The name of the store.
        unique_indentifier (str): The unique identifier of the store.
        is_main_store (bool): Indicates if the store is the main store.
        status (int): The status of the store.

        store_holidays (List[Holiday]): The relationship to the Holiday model.
        store_detail (StoreDetail): The relationship to the StoreDetail model.

    Inherits from:
        BaseModalWithSoftDelete: Provides common functionality for all models.
    """

    __tablename__ = "stores"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=expression.FunctionElement(ULIDGenerator.generate)
    )

    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("saas_admins.id"))
    created_by: Mapped["SAASAdmin"] = relationship(back_populates="stores")

    name: Mapped[str] = mapped_column(String(length=255))
    unique_indentifier: Mapped[Optional[str]] = mapped_column(String, unique=True)
    is_main_store: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[int] = mapped_column(Integer)

    store_holidays: Mapped[List["Holiday"]] = relationship(back_populates="store")
    store_detail: Mapped["StoreDetail"] = relationship(
        back_populates="store", foreign_keys="[StoreDetail.store_id]"
    )


class StoreDetail(BaseModalWithSoftDelete):
    """Represents the details of a store in the database.

    This class defines the structure and relationships for the 'store_details' table.

    Attributes:
        id (int): The primary key of the store detail.

        store_id (str): The foreign key referencing the associated store.
        store (Store): The relationship to the Store model.
        country_id (int): The ID of the country.
        country (Country): The relationship to the Country model.
        state_id (int): The ID of the state.
        state (State): The relationship to the State model.
        city_id (int): The ID of the city.
        city (City): The relationship to the City model.
        parent_store_id (Optional[str]): The ID of the parent store.
        parent_store (Store): The relationship to the Store model.

        description (Optional[str]): The description of the store.
        slogan (Optional[str]): The slogan of the store.
        address (Optional[str]): The address of the store.
        postal_code (Optional[str]): The postal code of the store.
        logo (str): The logo of the store.
        cover_image (str): The cover image of the store.
        gst (Optional[str]): The GST number of the store.
        tin (Optional[str]): The TIN number of the store.
        services (List[int]): The list of services provided by the store.
        sub_services (List[int]): The list of sub-services provided by the store.
        has_online_booking (bool): Indicates if the store has online booking.
        has_delivery_service (bool): Indicates if the store has delivery service.
        has_parking_facility (bool): Indicates if the store has parking facility.
        has_wifi_facility (bool): Indicates if the store has WiFi facility.

        contact_details (List[StoreContactDetail]): The relationship to the
        StoreContactDetail model.

    Inherits from:
        BaseModalWithSoftDelete: Provides common functionality for all models.
    """

    __tablename__ = "store_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    store_id: Mapped[str] = mapped_column(String, ForeignKey("stores.id"))
    store: Mapped["Store"] = relationship(back_populates="store_detail", foreign_keys=[store_id])
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"))
    country: Mapped["Country"] = relationship()
    state_id: Mapped[int] = mapped_column(Integer, ForeignKey("states.id"))
    state: Mapped["State"] = relationship()
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id"))
    city: Mapped["City"] = relationship()
    parent_store_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("stores.id"))
    parent_store: Mapped["Store"] = relationship(foreign_keys=[parent_store_id])

    description: Mapped[Optional[str]] = mapped_column(Text)
    slogan: Mapped[Optional[str]] = mapped_column(String(length=100))
    address: Mapped[str] = mapped_column(String(length=255))
    postal_code: Mapped[str] = mapped_column(String(length=10))
    logo: Mapped[str] = mapped_column(String)
    cover_iamge: Mapped[str] = mapped_column(String)
    gst: Mapped[Optional[str]] = mapped_column(String(20))
    tin: Mapped[Optional[str]] = mapped_column(String(20))
    services: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    sub_services: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    has_online_booking: Mapped[Optional[bool]] = mapped_column(Boolean)
    has_delivery_service: Mapped[Optional[bool]] = mapped_column(Boolean)
    has_parking_facility: Mapped[Optional[bool]] = mapped_column(Boolean)
    has_wifi_facility: Mapped[Optional[bool]] = mapped_column(Boolean)

    contact_details: Mapped[List["StoreContactDetail"]] = relationship(
        back_populates="store_detail"
    )


class StoreContactDetail(BaseModalWithSoftDelete):
    """Represents the contact details of a store in the database.

    This class defines the structure and relationships for the 'store_contact_details' table.

    Attributes:
        id (int): The primary key of the store contact detail.

        store_detail_id (str): The foreign key referencing the associated store detail.
        store_detail (StoreDetail): The relationship to the StoreDetail model.

        email (str): The email address of the store.
        is_email_verified (bool): Indicates if the email is verified.
        phone_country_code (str): The country code of the phone number.
        phone_number (str): The phone number of the store.
        is_phone_number_verified (bool): Indicates if the phone number is verified.
        alternate_email (Optional[str]): The alternate email address of the store.
        is_alternate_email_verified (bool): Indicates if the alternate email is verified.
        alternate_phone_country_code (Optional[str]): The country code of the
        alternate phone number.
        alternate_phone_number (Optional[str]): The alternate phone number of the store.
        is_alternate_phone_number_verified (bool): Indicates if the alternate phone number
        is verified.
        social_links (Optional[JSONB]): The social media links of the store.

    Inherits from:
            BaseModalWithSoftDelete: Provides common functionality for all models.
    """

    __tablename__ = "store_contact_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    store_detail_id: Mapped[int] = mapped_column(Integer, ForeignKey("store_details.id"))
    store_detail: Mapped["StoreDetail"] = relationship(back_populates="contact_details")

    email: Mapped[str] = mapped_column(String(length=100))
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    phone_country_code: Mapped[str] = mapped_column(String(length=5))
    phone_number: Mapped[str] = mapped_column(String(length=15))
    is_phone_number_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    alternate_email: Mapped[Optional[str]] = mapped_column(String(length=100))
    is_alternate_email_verified: Mapped[Optional[bool]] = mapped_column(Boolean)
    alternate_phone_country_code: Mapped[Optional[str]] = mapped_column(String(length=5))
    alternate_phone_number: Mapped[Optional[str]] = mapped_column(String(length=15))
    is_alternate_phone_number_verified: Mapped[Optional[bool]] = mapped_column(Boolean)
    social_links: Mapped[Optional[JSONB]] = mapped_column(JSONB)


# list of enum class
class StoreStatusEnum(BaseEnum):
    """Enumeration of possible store statuses.

    Attributes:
        CREATING (int): Store is in the process of being created.
        ACTIVE (int): Store is currently active and operational.
        INACTIVE (int): Store is not currently active.
        FAILED (int): Store creation or operation has failed.
        SUSPENDED (int): Store operations are temporarily suspended.
        DELETED (int): Store has been deleted from the system.
        PENDING_APPROVAL (int): Store is awaiting approval.
        UNDER_REVIEW (int): Store is currently under review.
        MAINTENANCE (int): Store is undergoing maintenance.
        TEMPORARILY_CLOSED (int): Store is temporarily closed.
    """

    CREATING = 10
    ACTIVE = 20
    INACTIVE = 30
    FAILED = 40
    SUSPENDED = 50
    DELETED = 60
    PENDING_APPROVAL = 70
    UNDER_REVIEW = 80
    MAINTENANCE = 90
    TEMPORARILY_CLOSED = 100


class StoreServiceEnum(BaseEnum):
    """Enumeration of primary services offered by stores.

    Attributes:
        ALL (int): All services are offered.
        LAUNDRY (int): Laundry services are offered.
        SELLING_WHOLESALE (int): Wholesale selling services are offered.
        SELLING_RETAIL (int): Retail selling services are offered.
        CUT_PIECE_CENTER (int): Cut piece center services are offered.
    """

    ALL = 10
    LAUNDRY = 20
    SELLING_WHOLESALE = 30
    SELLING_RETAIL = 40
    CUT_PIECE_CENTER = 70


class StoreSubServiceEnum(BaseEnum):
    """Enumeration of sub-services offered by stores.

    Attributes:
        WASHING (int): Washing service.
        IRON (int): Ironing service.
        DRY_CLEANING (int): Dry cleaning service.
        STAIN_REMOVAL (int): Stain removal service.
        FOLDING (int): Folding service.
        DYEING (int): Dyeing service.
        BLEACHING (int): Bleaching service.
        BULK_ORDER_PROCESSING (int): Bulk order processing service.
        CUSTOM_PACKAGING (int): Custom packaging service.
        WAREHOUSING (int): Warehousing service.
        DISTRIBUTION (int): Distribution service.
        SHIPPING_LOGISTICS (int): Shipping and logistics service.
        CUSTOM_FITTING (int): Custom fitting service.
        GIFT_WRAPPING (int): Gift wrapping service.
        HOME_DELIVERY (int): Home delivery service.
        IN_STORE_PICKUP (int): In-store pickup service.
        PERSONAL_SHOPPER (int): Personal shopper service.
        WHOLESALE_LAUNDRY_PACKAGING (int): Wholesale laundry packaging service.
        RETAIL_LAUNDRY_SERVICE (int): Retail laundry service.
        FABRIC_CUTTING (int): Fabric cutting service.
        FABRIC_SORTING (int): Fabric sorting service.
        CUSTOM_LABELING (int): Custom labeling service.
    """

    WASHING = 10
    IRON = 20
    DRY_CLEANING = 30
    STAIN_REMOVAL = 40
    FOLDING = 50
    DYEING = 60
    BLEACHING = 70
    BULK_ORDER_PROCESSING = 80
    CUSTOM_PACKAGING = 90
    WAREHOUSING = 100
    DISTRIBUTION = 110
    SHIPPING_LOGISTICS = 120
    CUSTOM_FITTING = 130
    GIFT_WRAPPING = 140
    HOME_DELIVERY = 150
    IN_STORE_PICKUP = 160
    PERSONAL_SHOPPER = 170
    WHOLESALE_LAUNDRY_PACKAGING = 180
    RETAIL_LAUNDRY_SERVICE = 190
    FABRIC_CUTTING = 200
    FABRIC_SORTING = 210
    CUSTOM_LABELING = 220
