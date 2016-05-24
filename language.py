def sanitize_language(string):
    string = remove_stray_quotes(string)
    string = remove_stray_brackets(string)
    string = capitalize_after_punctuation(string)
    return string

def remove_stray_quotes(string):
    count = string.count("\"")
    if count % 2 != 0:
       string = string.replace("\"","")   
    
    count = string.count("\'")
    if count % 2 != 0:
        string = string.replace("\'","")

    return string

def remove_stray_brackets(string):
    count_open = string.count("(")
    count_closed = string.count(")")
    if (count_open + count_closed) % 2 != 0:
        string = string.replace(")","")   
        string = string.replace("(","")   
    return string


def capitalize_after_punctuation(string):
    offset = 0
    for index, char in enumerate(string):
        if is_punctuation(char) and len(string) > index + 1:
            if(string[index + 1] == ' '):
                try:
                     string =  string[:index + 2] + string[index + 2:].capitalize()
                except:
                    pass
    return string
            
def is_punctuation(char):
    if char == "." or char == "?" or char == "!":
        return True
    else:
        return False