from functions.anzeigen import ApiRequestError, format_api_error_message


def test_format_api_error_message_includes_status_and_details():
    error = ApiRequestError("https://example.test", 503, "service unavailable")

    message = format_api_error_message(error)

    assert "503" in message
    assert "https://example.test" in message
    assert "service unavailable" in message
