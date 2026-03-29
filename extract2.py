import zipfile, xml.etree.ElementTree as ET
import os
import re

def extract_docx(path):
    with open("docx_text.txt", "w", encoding="utf-8") as f:
        try:
            with zipfile.ZipFile(path) as docx:
                xml_content = docx.read('word/document.xml')
                tree = ET.XML(xml_content)
                NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
                text = [node.text for node in tree.iter(NAMESPACE + 't') if node.text]
                f.write('\n'.join(text))
            print("DOCX extracted via zipfile")
        except Exception as e:
            print("DOCX failed:", e)

def extract_ppt_strings(path):
    with open("ppt_text.txt", "w", encoding="utf-8") as out:
        try:
            with open(path, "rb") as f:
                data = f.read()
            ascii_strings = re.findall(b'[ -~]{4,}', data)
            utf16_strings = re.findall(b'(?:[\x20-\x7E]\x00){4,}', data)
            
            for s in ascii_strings:
                try:
                    text = s.decode('ascii')
                    if not any(c in text for c in ['xml', 'http', 'urn:schemas']):
                        out.write(text + '\n')
                except:
                    pass
            for s in utf16_strings:
                try:
                    text = s.decode('utf-16le')
                    out.write(text + '\n')
                except:
                    pass
            print("PPT strings extracted")
        except Exception as e:
            print("PPT failed:", e)

if __name__ == "__main__":
    extract_docx(os.path.abspath("ByteBrief AI-Powered News Digest Platform.docx"))
    extract_ppt_strings(os.path.abspath("BATCH 21-Final.ppt"))
