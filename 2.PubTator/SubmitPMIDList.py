import requests
import io
from requests.adapters import HTTPAdapter

HTTPAdapter(max_retries=10)


def SubmitPMIDList(Inputfile, Format, Outfile, Bioconcept):

    json_file = {}

    # load pmids
    with io.open(Inputfile, 'r', encoding="utf-8") as file_input:
        json_file = {"pmids": [pmid.strip() for pmid in file_input.readlines()]}

    # load bioconcepts
    if Bioconcept != "":
        json_file["concepts"] = Bioconcept.split(",")

    # request
    r = requests.post(
        "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/"
        + Format,
        json=json_file)

    # r = requests.post(
    # 	"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/"+Format,
    # 	json = json_file,
    # 	timeout= (120, 120))

    if r.status_code != 200:
        print("[Error]: HTTP code " + str(r.status_code))
    else:
        # 		print(r.text.encode("utf-8"))
        response = r.text
        outputfile = open(Outfile, 'w')
        outputfile.write(response)
        outputfile.close()
