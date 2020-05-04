class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.is_setup = True
        self.is_reverse = False

    def start_settle_selection(self):
        can_build = self.model.can_build_settle()
        avail = self.model.get_available_settle_nodes(self.is_setup)
        if (can_build or self.is_setup) and len(avail) > 0:
            self.view.display_settle_options(avail)
        else:
            self.view.cannot_build_settle()

    def handle_settle_build(self, coord):
        color = self.model.build_settle(coord, self.is_setup)
        self.view.build_settle(coord, color)
        self.update_player_info()

        if self.is_setup:
            self.view.start_road_selection()

    def start_road_selection(self):
        can_build = self.model.can_build_road()
        if self.is_setup:
            avail = self.model.get_setup_avail_paths()
        else:
            avail = self.model.get_avail_paths()

        if (can_build or self.is_setup) and len(avail) > 0:
            self.view.display_road_options(avail)
        else:
            self.view.cannot_build_road()

    def handle_road_build(self, coord):
        color = self.model.build_road(coord, self.is_setup)
        self.view.build_road(coord, color)
        self.update_player_info()

        if self.is_setup:
            self.handle_turn_change()

        if self.is_setup:
            self.view.start_settle_selection()

    def handle_turn_change(self):
        self.is_setup, self.is_reverse = self.model.change_turn(self.is_setup, self.is_reverse)
        cur_player = self.model.cur_player()
        self.view.start_turn(cur_player)

    def start_game(self):
        player_states = self.model.get_player_states()
        self.view.init_player_info(player_states)
        self.view.start_turn(player_states[0])

        rcrd = self.model.get_robber_coord()
        self.view.move_robber(rcrd)
        self.view.start_settle_selection()

    def handle_robber_move(self, coord):
        self.model.move_robber(coord)
        self.view.move_robber(coord)

    def roll_dice(self):
        roll_num = self.model.roll_dice()
        print("Dice roll: {}".format(roll_num))
        if roll_num == 7:
            avail = self.model.get_avail_robber_coords()
            self.view.display_robber_options(avail)
        else:
            self.model.distribute_resources(roll_num)
            self.update_player_info()

    def update_player_info(self):
        player_states = self.model.get_player_states()
        self.view.update_player_info(player_states)
