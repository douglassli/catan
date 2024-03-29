import socket_server.message_values as mv


class InputMessage:
    def __init__(self, msg, websocket):
        self.msg = msg
        self.websocket = websocket
        self.msg_type = mv.InTypes(msg[mv.TYPE])

    def is_valid(self, rooms):
        room_id = self.msg[mv.ROOM_ID]
        plyr_id = self.msg[mv.PLAYER_ID]
        return room_id in rooms and rooms[room_id].has_plyr_id(plyr_id)

    async def handler(self, room):
        pass


class CreateRoomMsg(InputMessage):
    def is_valid(self, rooms):
        return self.msg[mv.NAME].isalnum()

    async def handler(self, room):
        await room.add_player(self.websocket, self.msg[mv.NAME])


class JoinRoomMsg(InputMessage):
    def is_valid(self, rooms):
        room_id = self.msg[mv.ROOM_ID]
        name = self.msg[mv.NAME]
        return room_id in rooms and name.isalnum() and rooms[room_id].is_name_available(name)

    async def handler(self, room):
        await room.add_player(self.websocket, self.msg[mv.NAME])


class ReadyMsg(InputMessage):
    async def handler(self, room):
        await room.mark_ready(self.msg[mv.PLAYER_ID])


class StartGameMsg(InputMessage):
    def is_valid(self, rooms):
        return super().is_valid(rooms) and rooms[self.msg[mv.ROOM_ID]].is_room_ready()

    async def handler(self, room):
        await room.start_game()


class StartSettleSelectMsg(InputMessage):
    async def handler(self, room):
        await room.start_settle_select(self.msg[mv.PLAYER_ID])


class StartRoadSelectMsg(InputMessage):
    async def handler(self, room):
        await room.start_road_select(self.msg[mv.PLAYER_ID])


class StartCitySelectMsg(InputMessage):
    async def handler(self, room):
        await room.start_city_select(self.msg[mv.PLAYER_ID])


class ChoseSettleMsg(InputMessage):
    async def handler(self, room):
        await room.chose_settle(self.msg[mv.PLAYER_ID], self.msg[mv.ROW], self.msg[mv.COL])


class ChoseRoadMsg(InputMessage):
    async def handler(self, room):
        await room.chose_road(self.msg[mv.PLAYER_ID], self.msg[mv.ROW], self.msg[mv.COL])


class ChoseCityMsg(InputMessage):
    async def handler(self, room):
        await room.chose_city(self.msg[mv.PLAYER_ID], self.msg[mv.ROW], self.msg[mv.COL])


class EndTurnMsg(InputMessage):
    async def handler(self, room):
        await room.end_turn(self.msg[mv.PLAYER_ID])


class RollDiceMsg(InputMessage):
    async def handler(self, room):
        await room.roll_dice(self.msg[mv.PLAYER_ID])


class ChoseRobberMsg(InputMessage):
    async def handler(self, room):
        await room.robber_moved(self.msg[mv.PLAYER_ID], self.msg[mv.ROW], self.msg[mv.COL])


class ChosePlayerRobMsg(InputMessage):
    async def handler(self, room):
        await room.chose_player_rob(self.msg[mv.PLAYER_ID], self.msg[mv.NAME])


class BuyDevCardMsg(InputMessage):
    async def handler(self, room):
        await room.buy_dev_card(self.msg[mv.PLAYER_ID])


class ProposeTradeMsg(InputMessage):
    async def handler(self, room):
        cur_resources = {mv.field_to_res(k): v for k, v in self.msg[mv.CURRENT_RESOURCES].items()}
        other_resources = {mv.field_to_res(k): v for k, v in self.msg[mv.OTHER_RESOURCES].items()}
        await room.propose_trade(self.msg[mv.PLAYER_ID], self.msg[mv.TRADE_ID], cur_resources, other_resources)


class TradeResponseMsg(InputMessage):
    async def handler(self, room):
        await room.respond_to_trade(self.msg[mv.PLAYER_ID], self.msg[mv.TRADE_ID], self.msg[mv.ACCEPTED])


class ConfirmTradeMsg(InputMessage):
    async def handler(self, room):
        await room.confirm_trade(self.msg[mv.PLAYER_ID], self.msg[mv.TRADE_ID], self.msg[mv.NAME])


class CancelTradeMsg(InputMessage):
    async def handler(self, room):
        await room.cancel_trade(self.msg[mv.PLAYER_ID], self.msg[mv.TRADE_ID])


class UseKnightMsg(InputMessage):
    async def handler(self, room):
        await room.use_knight(self.msg[mv.PLAYER_ID])


class UseRoadBuilderMsg(InputMessage):
    async def handler(self, room):
        await room.use_road_builder(self.msg[mv.PLAYER_ID])


class UsePlentyMsg(InputMessage):
    async def handler(self, room):
        await room.use_plenty(self.msg[mv.PLAYER_ID],
                              mv.field_to_res(self.msg[mv.RESOURCE1]),
                              mv.field_to_res(self.msg[mv.RESOURCE2]))


class UseMonopolyMsg(InputMessage):
    async def handler(self, room):
        await room.use_monopoly(self.msg[mv.PLAYER_ID], mv.field_to_res(self.msg[mv.RESOURCE]))
