def clean_text_and_get_video_data(text):
    char_to_replace = {'[',']','.webm'}
    replaced_text = text
    for key in char_to_replace:
        replaced_text = replaced_text.replace(key, '')
    return replaced_text.split('-')

def genarate_uuid():
    return str(uuid.uuid4())