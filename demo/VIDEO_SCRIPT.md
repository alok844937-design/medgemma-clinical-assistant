\# MedGemma Offline Clinical Assistant - Demo Video Script (90 sec)



\## 0-10 sec: Problem 

Clinical environments often lack reliable internet and cannot use cloud-based LLMs.

Privacy and offline capability are critical in healthcare.



\## 10-25 sec: Solution 

This project uses Google's open-weight MedGemma (HAI-DEF) model to run completely offline and assist in: 

* Structuring clinical notes for doctors 
* Explaining medical documents to patients in simple Hinglish 



\## 25-45 sec: Live Demo

1. Show terminal: 

&nbsp;  pytest -v → all tests passing

2\. Run: 

&nbsp;  python app.py 

3\. Open browser: 

&nbsp;  http://127.0.0.1:5000



\## 45-70 sec: App Features 

* Patient Mode: Converts discharge summaries into Hinglish explanations
* Doctor Mode: Structures unorganized notes into clean clinical format 
* Offline-start, no cloud calls 
* Clear safety disclaimers (non-diagnostic) 



\## 70-90 sec: Impact

This tool can be deployed in: 

* Rural clinics 
* Low-resource hospitals 
* Privacy-sensitive environments



Build using MedGemma as part of the HAI-DEF ecosystem.

