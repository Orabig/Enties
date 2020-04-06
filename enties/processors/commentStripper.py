import re


def strip_comments(content, config):
    """
    Strip comments from the given content string.

    config is a dict :
       style: python | C

    TODO : python style does NOT take into account quotes ('"a string with # inside"' -> '"a string with ')

    :param content: an input string
    :param config: a set of options about how interpret the comment token
    :return: the stripped string
    """
    style = config['style']
    content = str(content)
    if style == "python":
        return re.sub(r'(?m)\s*#.*\n?', '\n', content)
    elif style == "C":
        raise BaseException("C content not implemented yet")
    else:
        raise BaseException("strip_comment type '%s' is not implemented")
