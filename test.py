import google.generativeai as genai
genai.configure(api_key="AIzaSyBseSWyewIbTuCSWFKDMtVXZfsIPi_E4NM")
model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
response = model.generate_content("Why did Tesla stock drop today?")
print(response.text)