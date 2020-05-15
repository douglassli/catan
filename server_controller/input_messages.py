from server_controller.message_values import FieldNames, InTypes


class InputMessage:
    def __init__(self, msg, websocket):
        self.msg = msg
        self.websocket = websocket
        self.msg_type = InTypes(msg[FieldNames.TYPE])

    def is_valid(self, rooms):
        room_id = self.msg[FieldNames.ROOM_ID]
        plyr_id = self.msg[FieldNames.PLAYER_ID]
        return room_id in rooms and rooms[room_id].has_plyr_id(plyr_id)

    async def handler(self, room):
        pass


class CreateRoomMsg(InputMessage):
    def is_valid(self, rooms):
        return self.msg[FieldNames.NAME].isalnum()

    async def handler(self, room):
        await room.add_player(self.websocket, self.msg[FieldNames.NAME])


class JoinRoomMsg(InputMessage):
    def is_valid(self, rooms):
        room_id = self.msg[FieldNames.ROOM_ID]
        name = self.msg[FieldNames.NAME]
        return room_id in rooms and name.isalnum() and rooms[room_id].is_name_available(name)

    async def handler(self, room):
        await room.add_player(self.websocket, self.msg[FieldNames.NAME])


class ReadyMsg(InputMessage):
    async def handler(self, room):
        await room.mark_ready(self.msg[FieldNames.PLAYER_ID])


class StartGameMsg(InputMessage):
    def is_valid(self, rooms):
        return super().is_valid(rooms) and rooms[self.msg[FieldNames.ROOM_ID]].is_room_ready()

    async def handler(self, room):
        await room.start_game()


class StartSettleSelectMsg(InputMessage):
    async def handler(self, room):
        await room.start_settle_select(self.msg[FieldNames.PLAYER_ID])


class StartRoadSelectMsg(InputMessage):
    async def handler(self, room):
        await room.start_road_select(self.msg[FieldNames.PLAYER_ID])


class SettleBuiltMsg(InputMessage):
    async def handler(self, room):
        await room.settle_built(self.msg[FieldNames.PLAYER_ID], self.msg[FieldNames.ROW], self.msg[FieldNames.COL])


class RoadBuiltMsg(InputMessage):
    async def handler(self, room):
        await room.road_built(self.msg[FieldNames.PLAYER_ID], self.msg[FieldNames.ROW], self.msg[FieldNames.COL])


class EndTurnMsg(InputMessage):
    async def handler(self, room):
        await room.end_turn()
