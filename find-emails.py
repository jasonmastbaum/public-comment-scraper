import os
import re

import pandas as pd
import pymupdf

#data_files = os.listdir("data")

curdir = os.getcwd()
data = os.listdir("data")
for d in data:
	if "sb-79" in d:
	#if "pdf" in d:
		data = d
		break
filepath = os.path.join(curdir, "data", data)

doc = pymupdf.open(filepath)

def find_senders(page):
	senders = re.findall(r'From:\s*.*?<([^<>@\s]+@[^<>@\s]+)>', page, re.DOTALL)
	subjects = re.findall(r'Subject:\s*\n([^\n\r]+)', page)
	#subjects = re.findall(r'Subject:\s*\n([^\n\r]+)\s*\nEXTERNAL', page)
	return senders, subjects

pages = [page.get_text() for page in doc]

#decode("utf-8")
senders = []
for page_index, page in enumerate(pages):
	page_senders, page_subjects = find_senders(page)

	if len(page_senders) == 0:
		continue
	'''
	this isn't just an if/else because I wanted the elif to do more
	to find the actual sender of the email, not just spit out the mulitple
	possible matches it finds on some pages
	'''
	elif len(page_senders) > 1:
		for sender in page_senders:
			senders.append((sender, page_subjects[0], page_index+1))
		#raise ValueError("found more than one sender on a page")
	else:
		senders.append((page_senders[0], page_subjects[0], page_index+1))

df = pd.DataFrame(senders, columns=["email", "subject", "page"])
df.to_csv(os.path.join(curdir, "data", "senders-sb79.csv"), index=False)

'''
Can also pull the Action Network report of members and look for email addresses
in the public comment packet that are friendly to our position/used our form email
that are not already in the Action Network list, so that they can be sent an invite
to join Forward.
'''
listfile = "neighborhood-association-emails.csv"
#listfile = "an_report_santa-monica-families-for-safe-streets_2025-04-24-04-16.csv"
listfile_path = os.path.join(curdir, "data", listfile)
#print(listfile_path)
email_list = pd.read_csv(listfile_path)

#sender_list_merge = pd.merge(df, email_list, on="email", how="inner")
#sender_list_merge.to_excel(os.path.join(curdir, "data", "neighborhood_org-hits.xlsx"), index=False)