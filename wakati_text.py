from janome.tokenizer import Tokenizer


def wakati_text(text, pos=["名詞", "動詞"]):
    tokenizer = Tokenizer()
    doc = tokenizer.tokenize(text)
    wakati = None
    word_list = []
    for token in doc:
        p = token.part_of_speech.split(",")[0]
        if p in pos:
            word_list.append(token.base_form)
    if 0 < len(word_list):
        wakati = " ".join(word_list)
    return wakati


if __name__ == "__main__":
    s = wakati_text(
        "ある日の事でございます。御釈迦様は極楽の蓮池のふちを、独りでぶらぶら御歩きになっていらっしゃいました。池の中に咲いている蓮の花は、みんな玉のようにまっ白で、そのまん中にある金色の蕊からは、何とも云えない好い匂が、絶間なくあたりへ溢れて居ります。極楽は丁度朝なのでございましょう。"
    )
    print(s)
