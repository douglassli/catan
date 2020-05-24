class Trade:
    def __init__(self, trade_id, proposer_id, cur_resources, other_resources):
        self.trade_id = trade_id
        self.proposer_id = proposer_id
        self.cur_resources = cur_resources
        self.other_resources = other_resources
        self.responders = {}

    def is_proposed_by(self, plyr_id):
        return self.proposer_id == plyr_id

    def has_responded(self, plyr_id):
        return plyr_id in self.responders

    def respond(self, responder_id, accept):
        self.responders[responder_id] = accept

    def all_rejected(self, num_players):
        return len(self.responders) == num_players and all([not accepted for accepted in self.responders.values()])

    def has_accepted(self, plyr_id):
        return self.has_responded(plyr_id) and self.responders[plyr_id]
