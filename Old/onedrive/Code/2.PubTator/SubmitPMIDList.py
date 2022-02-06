import requests
import io
import json
import sys
from requests.adapters import HTTPAdapter
HTTPAdapter(max_retries=10)

def SubmitPMIDList(Inputfile,Format,Outfile,Bioconcept):
	
	json = {}
	
	# load pmids
	with io.open(Inputfile,'r',encoding="utf-8") as file_input:
		json = {"pmids": [pmid.strip() for pmid in file_input.readlines()]}
	
	# load bioconcepts
	if Bioconcept != "": 
		json["concepts"]=Bioconcept.split(",")
        
	# request
	r = requests.post(
		"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/"+Format, 
		json = json)
	
	# r = requests.post(
	# 	"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/"+Format, 
	# 	json = json,
	# 	timeout= (120, 120))

	if r.status_code != 200 :
		print ("[Error]: HTTP code "+ str(r.status_code))
	else:
# 		print(r.text.encode("utf-8"))
		response = r.text
		outputfile = open(Outfile, 'w')
		outputfile.write(response)
		outputfile.close()
