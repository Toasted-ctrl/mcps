from components import get_player_hiscore

class TestGetPlayerHiscore:

    def test_success(self, monkeypatch):
        
        class MockResponse:
            def __init__(self):
                self.text = "test response"
                self.status_code = 200
            def raise_for_status(self):
                pass

        def mock_get(*args, **kwargs):
            return MockResponse()
        
        def mock_unpack_hiscore(*args, **kwargs):
            return {
                "test_input": "test_output"
            }
        
        monkeypatch.setattr("components.requests.get", mock_get)
        monkeypatch.setattr("components.unpack_hiscore", mock_unpack_hiscore)

        result = get_player_hiscore(player_name="test_name")
        assert isinstance(result, dict)
        assert result == {
            "message": "Success",
            "detail": {
                "test_input": "test_output"
            }
        }


    def test_ValueError(self):
        result = get_player_hiscore(player_name="")
        assert isinstance(result, dict)
        assert result == {
            "error": "ValueError",
            "message": "Player name must not be None"
        }