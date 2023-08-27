PAT = '29d9803eb6f34718ba01d597a4a4e3b5'
USER_ID = 'meta'
APP_ID = 'Llama-2'
MODEL_ID = 'llama2-13b-chat'
MODEL_VERSION_ID = '79a1af31aa8249a99602fc05687e8f40'

storyname = input("ENTER PROMPT : ")

prompt = """
Generate a compelling video story script about """ + storyname + """. For each sentence in the story, provide a related visual image scene description to enhance the storytelling. Remember to format the output as follows: Image Prompt: [Insert image description or scene here] Narrator: [Write the narration or dialogue for the sentence] Image Prompt: [Insert image description or scene here] Narrator: [Write the narration or dialogue for the sentence] and so on untill the end of the story"""

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

post_model_outputs_response = stub.PostModelOutputs(
    service_pb2.PostModelOutputsRequest(
        user_app_id=userDataObject,
        model_id=MODEL_ID,
        version_id=MODEL_VERSION_ID,
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    text=resources_pb2.Text(
                        raw=prompt
                    )
                )
            )
        ]
    ),
    metadata=metadata
)
if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
    print(post_model_outputs_response.status)
    raise Exception(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")

# Since we have one input, one output will exist here
output = post_model_outputs_response.outputs[0]

print("Completion:\n")
print(output.data.text.raw)

