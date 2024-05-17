from repo.straddlerepo import StraddleRepo

class StraddleService:
    def __init__(self):
        self.straddle_repo = StraddleRepo()

    def process_data(self, data):
        self.straddle_repo.insert_data(data)

    