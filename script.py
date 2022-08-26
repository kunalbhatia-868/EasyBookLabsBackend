lab_ids=[
    'fed4d5f6-56d0-4e44-bcb7-b73c8465f62f',
	'f2fd3578-c098-4f7d-9920-aedf6c09c378',
	'f150582d-becd-4cd4-bbd2-d97acb2908a9',
	'ef64d5e4-a500-4c04-9b2b-51b21af59316',
	'eb2d878d-15e1-4646-9340-a0536f034cc0',
	'e1198b73-b705-471c-8dc1-98f2d1362048',
	'dda8116a-3590-4075-bd65-abdf30f4e060',
	'd23ebb37-1dcb-4479-9ba8-cd399c8d79b4',
	'd1e3bf24-81f8-4277-a3b7-fb4a1ecc25db',
	'd1497203-1108-4b55-978c-e2d24a74057a',
	'c6e4af81-2837-4b0b-b945-1686c6f2b1e8',
	'c1e3bc5a-38ea-4189-b7e8-8b85f022fb8f',
	'c163cfd3-41ad-404c-9480-0ec5ad313dcb',
	'c1588569-64f6-48b4-abf8-7811cf4b157b',
	'b2acbe23-808c-476e-b3b1-24ef06f3c4b4',
	'aa4648db-8064-4cab-852e-fccb3b03f472',
	'aa1a4fcf-bd14-4334-ac51-53dd7cc6160d',
	'a79fb741-37fb-4af1-afb7-d2aaca070b7c',
	'a42396f5-21c4-43eb-ac72-548a6dc7893f',
	'a1eeebea-9672-4600-a490-0b5af9e51614',
	'9f41479b-e13b-49cb-8b4d-1ec3f1ad02c2',
	'91e2e499-165c-438e-8a9e-cf5041f2b280',
	'88e189a4-9c10-4291-a48d-4d3d21d72014',
	'864cf561-a0ab-429d-b38a-f06912e4df22',
	'785fba0c-e6c6-41a9-96e3-66134558dfba',
	'780f8793-7040-4ae0-afa8-1f3d67fea318',
	'73de8f58-e014-4542-b9ed-26b52c22720e',
	'6ba8a142-003a-440b-803c-e963d9c7f186',
	'694d337f-1dbc-4e95-9fa5-affa604f4f83',
	'67f83b41-7740-4a5a-b4e8-1508591be0f5',
	'66fc0ab3-60d4-4a6d-b2a4-d2f158294da7',
	'63f9a2f8-b1b5-4e79-b249-84395ebc8904',
	'61c37051-b45e-40c7-82e5-6619e7ea2a89',
	'5d8c647a-40e7-4e08-9632-95b1164a0694',
	'5ac0b974-a592-483e-bc3e-f0f428fa1bab',
	'5a4c6c93-94fe-4dec-aca6-826b5dbb238f',
	'5842f88a-b5c4-4271-9bf7-d91688fdcf6e',
	'51b27610-316c-4976-8ea3-e90485cf1e65',
	'50ef7d93-cb1d-4fdd-9969-f7b752a6ba93',
	'4e158619-ceb7-4147-9d9c-1e0aa695a90b',
	'3f590c0e-0af2-4800-979f-df05fc7f3d3e',
	'395d3fc6-5c13-4c06-98d7-630787e5bc70',
	'37fbcac7-62af-4a97-b33a-2eabb9d91999',
	'346f5316-5e9f-4633-ac15-2ce24fc445c0',
	'33bc8923-00c2-4f9d-8852-fd8a79f8d8f2',
	'22fc31db-023f-429a-a681-19c7462a88a2',
	'1b969df1-2ef1-4c77-bd3a-1372bd561e73',
	'1991b841-bb3a-4fa4-895e-5b271f196eb1',
	'196ff692-8073-47ee-99e4-cdeee960214c',
	'17a1fd07-cd2e-49bc-9eb4-eac29578a3e8',
	'1696c7db-b0b3-4798-b845-04ac6a4bf645',
	'1553d9dc-926a-4491-aac8-e96df6fd2e0b',
	'1005463c-9d15-490b-9786-e5056af7279f',
	'10010b95-1b1d-4043-86ec-389b0fc82821',
	'0eb8ebb1-f83f-4db3-99ee-6edbb1194242',
	'05e90c1b-5761-4e3b-b732-2d360966f9b8',
	'01987b9d-2ff9-4075-a1c4-27cf11487376',
]

# from booking_api.models import Lab,Slot
# for lab_id in lab_ids:
#     start_time='11:00:00'
#     end_time='12:00:00'
#     days=["MO","TU","TH","FR"]
#     for day in days:    
#         slot=Slot(day=day,start_time=start_time,end_time=end_time,lab_id=Lab.objects.get(id=lab_id))
#         if slot.exists():
#             slot.first().save()
        
for lab_id in lab_ids:
    curl --location --request POST 'https://eazybooklabs.herokuapp.com/labs/${lab_id}/slots/' \
    --header 'accept: application/json' \
    --header 'X-CSRFToken: nOgMBqJboEjJLuEzvO2cSzj2LNnaYGPCFP1UJiU5MjRaTLNjuPN1sdyH4mwW900o' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "start_time":"17:00:00",
        "end_time":"18:00:00",
        "days":["MO","TU","TH","FR"]
    }'