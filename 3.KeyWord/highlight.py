def replace_html_tag(text, word_l):

    for word in word_l:

        new_word = '<font color="red">' + word + '</font>'
        len_w = len(word)
        len_t = len(text)
        for i in range(len_t - len_w, -1, -1):
            if text[i:i + len_w] == word:
                text = text[:i] + new_word + text[i + len_w:]

    return text


def save_html(ls_of_ls, prefix):
    fname = prefix + '.html'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(
            '<html><head><meta charset="UTF-8"></head><body><body style="background-color:rgb(157, 255, 0);"><table border="1">\n'
        )
        for ls in ls_of_ls:
            f.write('<tr>')
            for i in ls:
                f.write('<td><font size="4">{}</font></td>'.format(i))
            f.write('</tr>\n')
        f.write('</table></body></html>')
