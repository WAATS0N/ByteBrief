import win32com.client
import os

def extract_docx(path):
    try:
        import zipfile, xml.etree.ElementTree as ET
        with zipfile.ZipFile(path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
            text = [node.text for node in tree.iter(NAMESPACE + 't') if node.text]
            with open("docx_text.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(text))
        print("DOCX extracted via zipfile")
    except Exception as e2:
        print(f"Failed DOCX zipfile: {e2}")
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(path)
            text = doc.Content.Text
            doc.Close()
            word.Quit()
            with open("docx_text.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print("DOCX extracted via COM")
        except Exception as e:
            print(f"Failed DOCX COM: {e}")

def extract_ppt(path):
    try:
        ppt = win32com.client.Dispatch("PowerPoint.Application")
        pres = ppt.Presentations.Open(path, True, False, False)
        text = ""
        for slide in pres.Slides:
            text += f"--- SLIDE ---\n"
            for shape in slide.Shapes:
                if shape.HasTextFrame:
                    if shape.TextFrame.HasText:
                        text += shape.TextFrame.TextRange.Text + "\n"
        pres.Close()
        ppt.Quit()
        with open("ppt_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("PPT extracted via COM")
    except Exception as e:
        print(f"Failed PPT COM: {e}")

if __name__ == "__main__":
    extract_docx(os.path.abspath("ByteBrief AI-Powered News Digest Platform.docx"))
    extract_ppt(os.path.abspath("BATCH 21-Final.ppt"))
