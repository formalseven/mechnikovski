class StateManager:
    states = {}

    @classmethod
    def set(cls, user_id, data):
        cls.states[user_id] = data

    @classmethod
    def get(cls, user_id):
        return cls.states.get(user_id)

    @classmethod
    def delete(cls, user_id):
        del cls.states[user_id]