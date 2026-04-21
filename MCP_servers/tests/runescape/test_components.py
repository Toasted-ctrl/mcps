from runescape.components import get_player_hiscore

class TestPlayerHiscore:

    def test_success(self):
        result = get_player_hiscore(player_name="")
        assert result is not None
        assert result == {}