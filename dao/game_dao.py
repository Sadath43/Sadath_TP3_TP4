from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class GameEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    players = relationship("PlayerEntity", back_populates="game",cascade="all, delete-orphan")

class PlayerEntity(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship("GameEntity", back_populates="players")
    battle_field = relationship("BattlefieldEntity",back_populates="player",uselist=False, cascade="all, delete-orphan")

 class  BattleFieldEntity(Base):
     __tablename__ = 'BattleField'
     id = Column(Integer,primary_key=True)
     min_x = Column(Integer)
     min_y = Column(Integer)
     min_z = Column(Integer)
     max_x = Column(Integer)
     max_y = Column(Integer)
     max_z = Column(Integer)
     max_power = Column(Integer)
     player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
     player = relationship("playerEntity", back_populates="BattleField")
     Vessels = relationship("VesselEntity",back_populates="BattleField", uselist=False, cascade="all, delete-orphan")

class VesselEntity(Base):
    __tablename__ = 'vessel'
    id = Column(Integer, primary_key=True)
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    coord_z = Column(Integer)
    hits_to_be_destroyed = Column(Integer)
    type = Column(String)
    battle_field_id = Column(Integer, ForeignKey("battle_field.id"), nullable=False)
    battle_field = relationship("BattlefieldEntity",back_populates="Vessels",uselist=False, cascade="all, delete-orphan")
    weapans = relationship("weapansEntity",back_populates="Vessel",uselist=False, cascade="all, delete-orphan")

class WeaponEntity(Base):
    __tablename__ = 'Weapon'
    id = Column(Integer, primary_key=True)
    ammunitions = Column(Integer, nullable=False)
    range = Column(Integer, nullable=False)
    type = Column(String)
    Vessel_id = Column(Integer, ForeignKey("Vessel.id"), nullable=False)
    Vessel= relationship("VesselEntity",back_populates="weapans",uselist=False, cascade="all, delete-orphan")