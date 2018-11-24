from preprocess import process

def main():
    input_file = 'zh_wiki_00'
    output_file = 'zh_words'

    in_file = open(input_file, 'r')
    out_file = open(output_file, 'w+')

    for line in in_file.readlines():
        out = process(line)
        if len(out):
            out_file.write(str(out))
            out_file.write('\n')

    in_file.close()
    out_file.close()

if __name__ == '__main__':
    main()
