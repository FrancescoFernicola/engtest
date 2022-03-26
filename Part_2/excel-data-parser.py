import pandas as pd
import pathlib
import argparse
import logging


def main(dir_path, save_path, steps_after):

    save_log = pathlib.Path(save_path) / "Summary.log"

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s: %(levelname)s: %(message)s",
                        datefmt="[%m/%d/%Y] %I:%M:%S %p",
                        handlers=[logging.FileHandler(save_log), logging.StreamHandler()],
                        )

    folder = pathlib.Path(dir_path)

    if not folder.is_dir():
        logging.error(f"The directory name is invalid")
        exit()

    summary = {
        "File" : [], "Language": [], "Segments (All)": [], "Words (All)": [], "Segments (before LQA)": [],
        "Words (before LQA)": [], "Segments (after LQA)": [], "Words (after LQA)": [],
        "Percent Segments (before LQA)": [], "Percent Words (before LQA)": [], "Percent Segments (after LQA)": [],
        "Percent Words (after LQA)": [], "Avg PE Distance (before LQA)": [], "Avg PE Distance (after LQA)": [],
    }

    # RegEx formatting to match the afterLQA step in the file
    steps_after = [f"\(?{step}\)?" for step in steps_after]
    pattern = '|'.join(steps_after)

    for n in folder.glob("**/*.xlsx"):

        filename = pathlib.Path(n.parent.name) / n.name
        logging.debug(f"Parsing results from file: {filename}")

        # Here xlrd is implemented. Change import to pd.read_excel([...], engine="openpyxl") to use openpyxl (slower).

        df_corpus = pd.read_excel(n, sheet_name="Corpus", encoding="utf-8")
        df_corpus_rev = pd.read_excel(n, sheet_name="Corpus revision steps", encoding="utf-8")

        summary["File"].append(df_corpus.iloc[0]['File'])
        summary["Language"].append(n.stem)
        summary["Segments (All)"].append(df_corpus.iloc[0]['Segments'])
        summary["Words (All)"].append(df_corpus.iloc[0]['Words'])

        # AFTERLQA

        afterLQA = df_corpus_rev["Revision step"].str.contains(pattern, case=False, na=False)

        after_segments = df_corpus_rev[afterLQA]["Segments"].sum()
        after_words = df_corpus_rev[afterLQA]["Words"].sum()

        summary["Segments (after LQA)"].append(after_segments)
        summary["Words (after LQA)"].append(after_words)
        summary["Percent Segments (after LQA)"].append(after_segments / df_corpus.iloc[0]['Segments'])
        summary["Percent Words (after LQA)"].append(after_words / df_corpus.iloc[0]['Words'])
        summary["Avg PE Distance (after LQA)"].append(df_corpus_rev[afterLQA]["PE Distance"].mean())

        # BEFORELQA

        before_segments = df_corpus_rev[~afterLQA]["Segments"].sum()
        before_words = df_corpus_rev[~afterLQA]["Words"].sum()

        summary["Segments (before LQA)"].append(before_segments)
        summary["Words (before LQA)"].append(before_words)
        summary["Percent Segments (before LQA)"].append(before_segments/df_corpus.iloc[0]['Segments'])
        summary["Percent Words (before LQA)"].append(before_words/df_corpus.iloc[0]['Words'])
        summary["Avg PE Distance (before LQA)"].append(df_corpus_rev[~afterLQA]["PE Distance"].mean())

    logging.info(f"All results files have been parsed")

    summary = pd.DataFrame.from_dict(summary)
    save_summary = pathlib.Path(save_path) / "Summary.xlsx"

    logging.debug(f"Writing results to a summary Excel file")

    summary.to_excel(save_summary, index=False, na_rep='NA')

    logging.info(f"Summary Excel file generated and saved here: {save_summary.resolve()}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True,
                        type=str, metavar="DIR_PATH",
                        help="PATH to the directory containing the files")
    parser.add_argument("--save_to", nargs="?",
                        default=pathlib.Path.cwd(),
                        type=str, metavar="SAVE_PATH",
                        help="PATH where the Summary and LOG file will be saved")
    parser.add_argument("--afterLQA", nargs="*",
                        default=["correct2", "correct3"],
                        metavar="AFTER_LQA",
                        help="Steps included in after LQA. Default only considers 'correct2' and 'correct3'")

    args = parser.parse_args()

    main(args.dir, args.save_to, args.afterLQA)