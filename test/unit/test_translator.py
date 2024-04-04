from src.translator import translate_content #, CONTEXT
from mock import patch

class Response:
    def __init__(self, text):
        self.text = text
        
# def test_chinese():
#     is_english, translated_content = translate_content("这是一条中文消息")
#     assert is_english == False
#     assert translated_content == "This is a Chinese message"

# def test_french():
#     is_english, translated_content = translate_content("Voici mon ami Jean-Paul!")
#     assert is_english == False
#     assert translated_content == "Here is my friend Jean-Paul!"

# def test_english():
#     is_english, translated_content = translate_content("What are you blokes yapping about?")
#     assert is_english == True
#     assert translated_content == "What are you blokes yapping about?"

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
@patch('vertexai.preview.language_models.ChatModel.start_chat')
@patch('vertexai.preview.language_models._PreviewChatSession')
@patch('vertexai.preview.language_models.ChatModel')
@patch('vertexai.preview.language_models.ChatModel.from_pretrained')
def test_llm_normal_response(mocker_from_pretrained, mocker_chat_model, mocker_preview_chat_session, mocker_start_chat, mocker_send_message):
    mocker_from_pretrained.return_value = mocker_chat_model
    mocker_start_chat.return_value = mocker_preview_chat_session
    mocker_send_message.return_value.text = "(True,hello)"

    assert translate_content("hello") == (True, "hello")

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
@patch('vertexai.preview.language_models.ChatModel.start_chat')
@patch('vertexai.preview.language_models._PreviewChatSession')
@patch('vertexai.preview.language_models.ChatModel')
@patch('vertexai.preview.language_models.ChatModel.from_pretrained')
def test_llm_gibberish_response(mocker_from_pretrained, mocker_chat_model, mocker_preview_chat_session, mocker_start_chat, mocker_send_message):
    # mocker_pretrained.return_value = mocker_chat_model
    # mocker_start_chat.return_value = mocker_preview_chat_session
    # mocker_send_message.return_value.text = "malformed"

    # assert query_llm_robust("malformed") == (True, "<LangError>: Post text LLM response is malformed")

    mocker_from_pretrained.return_value = mocker_chat_model
    mocker_start_chat.return_value = mocker_preview_chat_session
    mocker_send_message.return_value.text = "(False, '-')"

    assert translate_content("DAFOEWGAIB WODFfjdskl aisdfow") == (False, "-")

    # # we mock the model's response to return a random message
    # mocker.return_value.text = "(True, <LangError>: Post text LLM response is malformed)"

    # # TODO assert the expected behavior
    # response1 = translate_content("Aquí está su primer ejemplo.")
    # mocker.assert_called_with("Aquí está su primer ejemplo.", temperature=0.7, max_output_tokens=256)
    # # mocker.assert_called_with([CONTEXT, "Aquí está su primer ejemplo."])
    # assert(response1 == mocker.return_value.text)

    # response2 = translate_content("DAFOEWGAIB WODFfjdskl aisdfow")
    # mocker.assert_called_with("DAFOEWGAIB WODFfjdskl aisdfow", temperature=0.7, max_output_tokens=256)
    # # mocker.assert_called_with([CONTEXT, "DAFOEWGAIB WODFfjdskl aisdfow"])
    # assert(response2 == mocker.return_value.text)

    # response3 = translate_content("ζͰէ۞ɯƨޝघටŧ𓂜꧈ໃ࿈Ϩɔȣפռ҂")
    # mocker.assert_called_with("ζͰէ۞ɯƨޝघටŧ𓂜꧈ໃ࿈Ϩɔȣפռ҂", temperature=0.7, max_output_tokens=256)
    # # mocker.assert_called_with([CONTEXT, "ζͰէ۞ɯƨޝघටŧ𓂜꧈ໃ࿈Ϩɔȣפռ҂"])
    # assert(response3 == mocker.return_value.text)
