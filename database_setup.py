from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Logindata(Base):
    __tablename__ = 'logindata'
   
    user = Column(String(250), primary_key=True)
    email_id = Column(String(40), nullable=False)
    passwd = Column(String(250), nullable=False)

    @property
    def serialize(self):
       return {
           'user'         : self.user,
           'pass'           : self.passwd,
           'email_id'       : self.email_id,
       }

class Bankdata(Base):
    __tablename__ = 'bankinfo'

    trans_id = Column(String(250), primary_key=True)
    user = Column(String(250), nullable=False)
    name = Column(String(250))
    cardno = Column(String(250))
    expirym = Column(String(250))
    expiryy = Column(String(250))
    cvv = Column(String(250))
    bank = Column(String(250))
    trans_type = Column(String(250))
    coursetype = Column(String(250))
    amount = Column(String(250))

    @property
    def serialize(self):
       return {
           'trans_id'         : self.trans_id,
           'user'           : self.user,
           'name'       : self.name,
           'cardno'       : self.cardno,
           'expirym'       : self.expirym,
           'expiryy'       : self.expiryy,
           'cvv'       : self.cvv,
           'bank'       : self.bank,
           'trans_type'       : self.trans_type,
           'coursetype'       : self.coursetype,
           'amount'       : self.amount,
       }

class Verify(Base):
    __tablename__ = 'check_verified'

    email_id = Column(String(40), primary_key = True)
    token = Column(String(80), nullable = False)
    verified = Column(String(1))

    @property
    def serialize(self):
        return {
            'email id'      : self.email_id,
            'verified'      : self.verified,
            'token'         : self.token,
            
        }



engine = create_engine('sqlite:///login.db')
 

Base.metadata.create_all(engine)
