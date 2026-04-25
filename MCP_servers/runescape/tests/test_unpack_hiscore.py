from unpack_hiscore import unpack_hiscore_item, unpack_hiscore

class TestUnpackHiscoreItem:

    def test_success_skill(self):
        result = unpack_hiscore_item(
            type="skill",
            listing=["88", "87", "86"])
        
        assert isinstance(result, dict)
        assert result == {
            "exp_score": "86",
            "level": "87",
            "ranking": "88",
            "type": "skill"
        }

    def test_success_activity(self):
        result = unpack_hiscore_item(
            type="activity",
            listing=["88", "87"])
        
        assert isinstance(result, dict)
        assert result == {
            "exp_score": "87",
            "level": None,
            "ranking": "88",
            "type": "activity"
        }

class TestUnpackHiscore:

    def test_success(self):
        test_input = """12,13,14\n15,16,17"""
        result = unpack_hiscore(input=test_input)
        assert isinstance(result, dict)
        assert result == {
            "Overall": {
                "exp_score": "14",
                "level": "13",
                "ranking": "12",
                "type": "skill"
            },
            "Attack": {
                "exp_score": "17",
                "level": "16",
                "ranking": "15",
                "type": "skill"
            }
        }