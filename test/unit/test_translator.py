import vertexai
from src.translator import translate_content, fullExtract #, CONTEXT
from mock import patch

class Response:
    def __init__(self, text):
        self.text = text

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
    mocker_send_message.return_value.text = "(False,-)"

    assert translate_content("DAFOEWGAIB WODFfjdskl aisdfow") == (False, "-")

@patch('vertexai.preview.language_models._PreviewChatSession.send_message')
@patch('vertexai.preview.language_models.ChatModel.start_chat')
@patch('vertexai.preview.language_models._PreviewChatSession')
@patch('vertexai.preview.language_models.ChatModel')
@patch('vertexai.preview.language_models.ChatModel.from_pretrained')
def test_spanish_response(mocker_from_pretrained, mocker_chat_model, mocker_preview_chat_session, mocker_start_chat, mocker_send_message):
    # mocker_pretrained.return_value = mocker_chat_model
    # mocker_start_chat.return_value = mocker_preview_chat_session
    # mocker_send_message.return_value.text = "malformed"

    # assert query_llm_robust("malformed") == (True, "<LangError>: Post text LLM response is malformed")

    mocker_from_pretrained.return_value = mocker_chat_model
    mocker_start_chat.return_value = mocker_preview_chat_session
    mocker_send_message.return_value.text = "(True,Testing the new translation feature)"

    assert translate_content("Probando la nueva función de traducción") == (False, "Testing the new translation feature")