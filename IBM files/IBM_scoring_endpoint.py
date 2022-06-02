import requests
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Bw7s8Ck0jh1mkIE_g3-WCWPoDOr_r_Q-3mv4r4orZ03e"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + mltoken}
t = [[-0.53102197, -0.33011729, -0.54797313, -1.69107192, -4.8551487,
      87.5530974,  0.87169756, -0.46080981, -0.45755831, -0.30184617,
      -0.64103006, -0.77754432,  1.41854501]]
# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"values": t}]}

# "field": [array_of_input_fields],
response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/00b5287b-b674-435e-9403-da3cf0440196/predictions?version=2022-05-31', json=payload_scoring,
                                 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
# predictions
print(response_scoring.json()['predictions'][0]['values'][0][0])
# print(predictions['predictions'][0]['values'][0][0])
