import os
import argparse
from google.cloud import translate_v2 as translate

def main(key, src, trg, text):

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key

    translate_client = translate.Client()
    output = translate_client.translate(text, source_language=src, target_language=trg)

    print(output)







if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, type=str, metavar="SRC_TEXT",
                        help="Text to be translated")
    parser.add_argument("--json", required=True, type=str, metavar="KEY_PATH",
                        help="PATH to the JSON file")
    parser.add_argument("--src", required=True, type=str, metavar="SRC_LANG",
                        help="Source Language in ISO-639-1 Code")
    parser.add_argument("--trg", required=True, type=str, metavar="TRG_LANG",
                        help="Target Language in ISO-639-1 Code")

    args = parser.parse_args()

    main(args.json, args.src, args.trg, args.text)