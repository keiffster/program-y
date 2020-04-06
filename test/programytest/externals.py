
google_translate = True
google_translate_disabled = "Google Translate is currently disabled"

sentiment_analysis = True
sentiment_analysis_disabled = "Sentiment Analysis is currently disabled"

rslp_stemming = True
rslp_stemming_disabled = "RSLP disabled, first nltk.download('rslp'), and then enable here"

admin_tool = True
admin_tool_disabled = "Admin tool download from github disabled"

integration_tests_disabled = "Integration tests disabled"
integration_tests = False

allow_license_keys_disabled = "License keys disbaled"
allow_license_keys = True

all_externals = False


def google_translate_active():
    return bool(all_externals is True and google_translate is True)


def sentiment_analysis_active():
    return bool(all_externals is True and sentiment_analysis is True)


def rslp_stemming_active():
    return bool(all_externals is True and rslp_stemming is True)


def admin_tool_active():
    return bool(all_externals is True and admin_tool is True)


def integration_tests_active():
    return bool(all_externals is True and integration_tests is True)


def allow_license_keys_active():
    return bool(all_externals is True and allow_license_keys is True)
