from dao.game_dao import GameDao
from model.game import Game
from model.player import Player
from model.vessel import Vessel
from model.battlefield import Battlefield

class GameService:
    def __init__(self):
        self.game_dao = GameDao()
    def create_game(self, player_name: str, min_x: int, max_x: int, min_y: int,max_y: int, min_z: int, max_z: int) -> int:
        game = Game()
        battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
        game.add_player(Player(player_name, battle_field))
        return self.game_dao.create_game(game)
    def join_game(self, game_id: int, player_name: str) -> bool:
        game=self.game_dao.find_game(game_id)
        player=self.game_dao.find_player(player_name)
        game.add_player(player)
        if player in game.get_players():
            return True
        else:
            return False
    def get_game(self, game_id: int) -> Game:
        game=self.game_dao.find_game(game_id)
        print(f"{game_id} de joueurs {game.get_players()}")
    def add_vessel(self, game_id: int, player_name: str, vessel_Id: str,x: int, y: int, z: int) -> bool:
        # j'ai changé vessel_type en vessel_Id pour pouvoir faire correspondre à la façon dont j'ai défini find_vessel
        game=self.game_dao.find_game(game_id)
        player = self.game_dao.find_player(player_name)
        vessel = self.game_dao.find_game(vessel_Id)
        vessel.coordinates=x,y,z
        player.get_battlefield().add_vessel(vessel)
        if vessel in player.get_battlefield().get_vessels():
            return True
        else:
            return False
    def shoot_at(self, game_id: int, shooter_name: str, vessel_id: int, x: int, y: int, z: int) -> bool:
        vessel = self.game_dao.find_vessel(vessel_id)
        game = self.game_dao.find_game(game_id)
        if vessel.weapon.ammunitions >= 1:
            stmt = WeaponEntity.update().where(WeaponEntity.vessel_id == vessel_id).values(
                {WeaponEntity.ammunitions: WeaponEntity.ammunitions - 1})
            self.db_session.scalars(stmt).one()
            for player in game.get_players():
                if player.get_name() != shooter_name:
                    if player.get_battlefield().fired_at(x, y, z):
                        stmt = VesselEntity.update().where(VesselEntity.coord_x == x, VesselEntity.coord_y == y, VesselEntity.coord_z == z).values({VesselEntity.hits_to_be_destroyed: VesselEntity.hits_to_be_destroyed - 1})
                        self.db_session.scalars(stmt).one()
                        return True
                    return False

    def get_game_status(self, game_id: int, shooter_name: str) -> str:
        game = self.game_dao.find_game(game_id)
        for player in game.get_players():
            if player.get_name() == shooter_name:
                if player.get_battlefield().get_vessels() is None:
                    return "PERDU"
            elif player.get_battlefield().get_vessels() is None:
                return "GAGNE"
        return "ENCOURS"