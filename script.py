from PyPDF2 import PdfReader
from tqdm import tqdm
from collections import defaultdict
from typing import List, Dict
from pathlib import Path

def main(pdfpath: str, output_file_name: str = "output"):
    pdfpath = Path(pdfpath).resolve()
    with open("wordlist.txt","r") as f:
        word_list: List[str] = [s.strip().lower() for s in f.readlines()]

    reader = PdfReader(pdfpath)
    
    # printing number of pages in pdf file
    print(len(reader.pages))

    word_map: Dict[str, Dict[int,List[str]]] = defaultdict(lambda:defaultdict(list))

    for i, page in tqdm(enumerate(reader.pages), desc="Parsing pages"):
        txt: str = page.extract_text().lower()
        for word in word_list:
            if word in txt:
                # pull snippets
                start = 0
                sub = txt[start:]
                while (ii:=sub.find(word)) > 0:
                    s_index = max(ii-100,0)
                    e_index = min(len(sub),ii+len(word)+100)
                    snippet = sub[s_index:e_index]
                    word_map[word][i+1].append(snippet)
                    sub = sub[ii+len(word):]

    ms = ""
    for w,index_dict in word_map.items():
        print(f"{w}: {list(index_dict.keys())}")
        txt = f"""
            ____________________________
            ########### {w} ############
            """
        for i, snippets in index_dict.items():
            txt += f"\n{'-'*20} PAGE -> {i} {'-'*20}\n"
            for j, snip in enumerate(snippets):
                txt+=f"Snippet {j+1}: \n\n"
                txt+=snip+f"\n\n{'-'*20}\n\n"

        ms+=txt
    with open(f"{output_file_name}.txt","ab") as f:
        f.write(bytes(ms, encoding="utf-8"))

