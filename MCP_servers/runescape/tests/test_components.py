from components import get_player_hiscore

class TestGetPlayerHiscore:

    def test_success(self):
        pass

    def test_ValueError(self):
        result = get_player_hiscore(player_name="")
        assert isinstance(result, dict)
        assert result == {
            "error": "ValueError",
            "message": "Player name must not be None"
        }