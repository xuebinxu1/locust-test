from utils.timezone import change_timezone
from sqlalchemy import Column, String, create_engine, Integer, DateTime, DECIMAL, TEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class TableBase():
    __table_args__ = {"useexisting": True}
    id = Column(Integer, nullable=True, primary_key=True)
    is_deleted = Column(Integer, nullable=False, default=0)
    gmt_create = Column(DateTime, nullable=True, default=change_timezone())
    gmt_modified = Column(DateTime, nullable=True, default=change_timezone())


class UserCertification(Base, TableBase):
    __tablename__ = 'user_certification'

    company_id = Column(Integer, nullable=True)
    channel_id = Column(Integer, nullable=True)
    mobile = Column(String, nullable=True)
    type = Column(Integer, nullable=True)
    expiration_period = Column(Integer, nullable=True)
    status = Column(Integer, nullable=True)
    succeed_flag = Column(Integer, nullable=True)


class User(Base, TableBase):
    __tablename__ = 'user'

    company_id = Column(Integer, nullable=True)
    cid = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=True)
    register_channel = Column(String, nullable=True)
    register_channel_id = Column(Integer, nullable=True)
    mobile_md5 = Column(String, nullable=True)


class UserDetail(Base, TableBase):
    __tablename__ = 'user_detail'

    cert_item = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)
    cid = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=True)
    channel_id = Column(Integer, nullable=True)
    channel_name = Column(String, nullable=True)
    province = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    gender = Column(Integer, nullable=True)
    nationality = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    marital_status = Column(Integer, nullable=True)
    income_level = Column(Integer, nullable=True)
    education_level = Column(Integer, nullable=True)
    bank_account_id = Column(Integer, nullable=True)
    category = Column(Integer, nullable=True)
    mobile_platform = Column(Integer, nullable=True)
    operator_id = Column(Integer, nullable=True)
    first_apply_time = Column(DateTime, nullable=True)
    first_deduct_time = Column(DateTime, nullable=True)
    loan_amount = Column(DECIMAL, nullable=True)
    raise_amount = Column(DECIMAL, nullable=True)
    emrg_contact_name_a = Column(String, nullable=True)
    emrg_contact_name_b = Column(String, nullable=True)
    emrg_contact_mobile_a = Column(String, nullable=True)
    emrg_contact_mobile_b = Column(String, nullable=True)
    idcard_front_img = Column(String, nullable=True)
    idcard_back_img = Column(String, nullable=True)
    thirdparty_data = Column(TEXT)
    raise_comment = Column(String, nullable=True)
    update_count = Column(Integer, nullable=True)
    name_mirror = Column(String, nullable=True)
    raise_amount_sign = Column(Integer, nullable=True)


class UserApplyInfo(Base, TableBase):
    __tablename__ = 'user_apply_info'

    cert_item = Column(String, nullable=True)
    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)
    cid = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=True)
    channel_id = Column(Integer, nullable=True)
    channel_name = Column(String, nullable=True)
    province = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    gender = Column(Integer, nullable=True)
    nationality = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    marital_status = Column(Integer, nullable=True)
    income_level = Column(Integer, nullable=True)
    education_level = Column(Integer, nullable=True)
    bank_account_id = Column(Integer, nullable=True)
    category = Column(Integer, nullable=True)
    mobile_platform = Column(Integer, nullable=True)
    operator_id = Column(Integer, nullable=True)
    first_apply_time = Column(DateTime, nullable=True)
    first_deduct_time = Column(DateTime, nullable=True)
    loan_amount = Column(DECIMAL, nullable=True)
    raise_amount = Column(DECIMAL, nullable=True)
    emrg_contact_name_a = Column(String, nullable=True)
    emrg_contact_name_b = Column(String, nullable=True)
    emrg_contact_mobile_a = Column(String, nullable=True)
    emrg_contact_mobile_b = Column(String, nullable=True)
    idcard_front_img = Column(String, nullable=True)
    idcard_back_img = Column(String, nullable=True)
    thirdparty_data = Column(TEXT)
    raise_comment = Column(String, nullable=True)
    update_count = Column(Integer, nullable=True)
    name_mirror = Column(String, nullable=True)
    raise_amount_sign = Column(Integer, nullable=True)


class Bankcard(Base, TableBase):
    __tablename__ = 'bankcard'

    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)
    bank_code = Column(String, nullable=True)
    bank_account_number = Column(String, nullable=True)
    bank_account_name = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    is_default = Column(Integer, nullable=True)
    payment_channel = Column(String, nullable=True)
    payment_channel_id = Column(Integer, nullable=True)
    is_binding = Column(Integer, nullable=True)
    mchntcd = Column(Integer, nullable=True)


class PaymentChannel(Base, TableBase):
    __tablename__ = 'payment_channel'

    company_id = Column(Integer, nullable=True)
    payment_channel_id = Column(Integer, nullable=True)
    payment_channel_name = Column(String, nullable=True)
    mchntcd = Column(String, nullable=True)
    is_enabled = Column(Integer, nullable=True)
    type = Column(Integer, nullable=True)
    is_default = Column(Integer, nullable=True)
    priority = Column(Integer, nullable=True)


class Bid(Base, TableBase):
    __tablename__ = 'bid'

    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)
    product_id = Column(Integer, nullable=True)
    bank_account_id = Column(Integer, nullable=True)
    status = Column(Integer, nullable=True)
    amount = Column(DECIMAL, nullable=True)
    period = Column(Integer, nullable=True)
    cid = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    name = Column(String, nullable=True)
    contract_no = Column(String, nullable=True)
    latitude = Column(DECIMAL, nullable=True)
    longitude = Column(DECIMAL, nullable=True)
    ip_address = Column(String, nullable=True)
    risk_level = Column(Integer, nullable=True)
    bank_account_number = Column(String, nullable=True)
    channel_id = Column(Integer, nullable=True)
    channel_name = Column(String, nullable=True)
    channel_label = Column(String, nullable=True)
    operate_time = Column(DateTime, nullable=True)
    operator_id = Column(Integer, nullable=True)
    last_operate_time = Column(DateTime, nullable=True)
    last_operator_id = Column(Integer, nullable=True)
    deduct_time = Column(DateTime, nullable=True)
    repayment_time = Column(DateTime, nullable=True)
    extend_time = Column(DateTime, nullable=True)
    real_repayment_time = Column(DateTime, nullable=True)
    repayment_time_type = Column(Integer, nullable=True)
    repayment_approach_type = Column(Integer, nullable=True)
    repayment_credit_type = Column(Integer, nullable=True)
    is_force_settled = Column(Integer, nullable=True)
    waive_amount = Column(DECIMAL, nullable=True)
    extension_period = Column(DECIMAL, nullable=True)
    raise_amount = Column(DECIMAL, nullable=True)
    reject_type = Column(Integer, nullable=True)
    comment = Column(String, nullable=True)
    is_extending = Column(Integer, nullable=True)
    is_offline_repayment = Column(Integer, nullable=True)
    is_undetermined = Column(Integer, nullable=True)


class BidWorkflow(Base, TableBase):
    __tablename__ = 'bid_workflow'

    bid_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)
    last_status = Column(Integer, nullable=True)
    current_status = Column(Integer, nullable=True)
    operator_id = Column(Integer, nullable=True)
    operating_time = Column(DateTime, nullable=True)
    action = Column(String, nullable=True)
    suggestion = Column(String, nullable=True)
    channel_id = Column(Integer, nullable=True)


class Event(Base, TableBase):
    __tablename__ = 'event'

    event_id = Column(String, nullable=True)
    bid_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)
    channel_id = Column(Integer, nullable=True)
    mobile = Column(String, nullable=True)
    is_expired = Column(Integer, nullable=True)


class CurrentTransaction(Base, TableBase):
    __tablename__ = 'current_transaction'

    company_id = Column(Integer, nullable=True)
    contract_no = Column(String, nullable=True)
    type = Column(Integer, nullable=True)
    scene = Column(Integer, nullable=True)
    status = Column(Integer, nullable=True)
    amount = Column(DECIMAL, nullable=True)
    customer_name = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    bid_id = Column(Integer, nullable=True)
    bid_contract_no = Column(String, nullable=True)
    payment_channel = Column(String, nullable=True)
    payment_channel_id = Column(Integer, nullable=True)
    event_id = Column(String, nullable=True)
    channel_id = Column(Integer, nullable=True)
    transaction_time = Column(DateTime, nullable=True)
    comment = Column(String, nullable=True)


class Transaction(Base, TableBase):
    __tablename__ = 'transaction'

    company_id = Column(Integer, nullable=True)
    contract_no = Column(String, nullable=True)
    type = Column(Integer, nullable=True)
    scene = Column(Integer, nullable=True)
    status = Column(Integer, nullable=True)
    amount = Column(DECIMAL, nullable=True)
    customer_name = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    bid_id = Column(Integer, nullable=True)
    bid_contract_no = Column(String, nullable=True)
    payment_channel = Column(String, nullable=True)
    payment_channel_id = Column(Integer, nullable=True)
    event_id = Column(String, nullable=True)
    channel_id = Column(Integer, nullable=True)
    transaction_time = Column(DateTime, nullable=True)
    comment = Column(String, nullable=True)


class Channel(Base, TableBase):
    __tablename__ = 'channel'

    company_id = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    label = Column(String, nullable=True)
    link = Column(String, nullable=True)
    payment_type = Column(Integer, nullable=True)
    template_type = Column(String, nullable=True)
    is_enabled = Column(Integer, nullable=True)
    deduct_percent = Column(DECIMAL, nullable=True)


class Product(Base, TableBase):
    __tablename__ = 'product'

    company_id = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    daily_interest_rate = Column(DECIMAL, nullable=True)
    annually_interest_rate = Column(DECIMAL, nullable=True)
    amount = Column(DECIMAL, nullable=True)
    period_day = Column(Integer, nullable=True)
    manage_fee = Column(DECIMAL, nullable=True)
    overdue_manage_fee = Column(DECIMAL, nullable=True)
    overdue_interest_rate = Column(DECIMAL, nullable=True)
    bad_bid_deadline = Column(Integer, nullable=True)
    cut_interest_fee = Column(DECIMAL, nullable=True)
    is_prepayment_enabled = Column(Integer, nullable=True)
    is_enabled = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    repayment_type = Column(Integer, nullable=True)
    name_image_filename = Column(String, nullable=True)
    message_service_fee_rate = Column(DECIMAL, nullable=True)
    account_manage_fee_rate = Column(DECIMAL, nullable=True)
    breach_account_fee_rate = Column(DECIMAL, nullable=True)
    interest_collect_style = Column(Integer, nullable=True)
    max_loan_amount = Column(DECIMAL, nullable=True)
    composite_daily_rate = Column(DECIMAL, nullable=True)
    composite_overdue_daily_rate = Column(DECIMAL, nullable=True)
    manage_fee_style = Column(Integer, nullable=True)
    collect_scale = Column(DECIMAL, nullable=True)
    is_auto = Column(Integer, nullable=True)
    overdue_number = Column(Integer, nullable=True)
    repeated_loan_scope_A = Column(String, nullable=True)
    repeated_loan_scope_B = Column(String, nullable=True)
    raise_amount_A = Column(DECIMAL, nullable=True)
    raise_amount_B = Column(DECIMAL, nullable=True)


class Bill(Base, TableBase):
    __tablename__ = 'bill'

    bid_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    product_id = Column(Integer, nullable=True)
    company_id = Column(Integer, nullable=True)
    channel_id = Column(Integer, nullable=True)
    status = Column(Integer, nullable=True)
    deduct_time = Column(DateTime, nullable=True)
    deduct_operator = Column(Integer, nullable=True)
    loan_amount = Column(DECIMAL, nullable=True)
    period = Column(Integer, nullable=True)
    daily_interest_rate = Column(DECIMAL, nullable=True)
    manage_fee = Column(DECIMAL, nullable=True)
    bad_bid_period = Column(Integer, nullable=True)
    repayment_time = Column(DateTime, nullable=True)
    repayment_amount = Column(DECIMAL, nullable=True)
    repayment_corpus = Column(DECIMAL, nullable=True)
    repayment_interest = Column(DECIMAL, nullable=True)
    extension_period = Column(Integer, nullable=True)
    extension_interest_rate = Column(DECIMAL, nullable=True)
    extension_interest = Column(DECIMAL, nullable=True)
    extension_manage_fee = Column(DECIMAL, nullable=True)
    extension_repayment_time = Column(DateTime, nullable=True)
    extension_repayment_amount = Column(DECIMAL, nullable=True)
    extension_returned_amount = Column(DECIMAL, nullable=True)
    total_overdue_days = Column(Integer, nullable=True)
    overdue_interest_rate = Column(DECIMAL, nullable=True)
    overdue_manage_fee = Column(DECIMAL, nullable=True)
    overdue_fine = Column(DECIMAL, nullable=True)
    waive_amount = Column(DECIMAL, nullable=True)
    mark_overdue_time = Column(DateTime, nullable=True)
    mark_bad_time = Column(DateTime, nullable=True)
    current_repayment_corpus = Column(DECIMAL, nullable=True)
    current_manage_fee = Column(DECIMAL, nullable=True)
    current_total_daily_interest = Column(DECIMAL, nullable=True)
    current_overdue_manage_fee = Column(DECIMAL, nullable=True)
    current_overdue_fine = Column(DECIMAL, nullable=True)
    current_repayment_time = Column(DateTime, nullable=True)
    current_repayment_amount = Column(DECIMAL, nullable=True)
    current_returned_amount = Column(DECIMAL, nullable=True)
    current_extension_period = Column(Integer, nullable=True)
    current_extension_interest = Column(DECIMAL, nullable=True)
    current_extension_manage_fee = Column(DECIMAL, nullable=True)
    current_extension_repayment_amount = Column(DECIMAL, nullable=True)
    real_repayment_time = Column(DateTime, nullable=True)
    real_repayment_corpus = Column(DECIMAL, nullable=True)
    real_repayment_interest = Column(DECIMAL, nullable=True)
    real_repayment_amount = Column(DECIMAL, nullable=True)
    interest_collect_style = Column(Integer, nullable=True)
    prepayment_amount = Column(DECIMAL, nullable=True)
    last_update_time = Column(DateTime, nullable=True)


# 初始化数据库连接:
# engine = create_engine("mysql+pymysql://root:Cisco123@10.10.10.200:33061/sake")
engine = create_engine('mysql+mysqldb://sake_demo:3imZYs7Vgm1EzQKp@rm-bp17kkg9v94pvnmla1o.mysql.rds.aliyuncs.com:3306/staging_sake?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
