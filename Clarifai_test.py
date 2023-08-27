# from langchain.llms import Clarifai
#
# CLARIFAI_PAT = "29d9803eb6f34718ba01d597a4a4e3b5"
# llm = Clarifai(pat = CLARIFAI_PAT,user_id = 'meta',app_id = 'Llama-2',model_id = 'llama2-70b-chat')
#
#
# print("INPUT : ")
# storyname = 'health is wealth'
#
# text = 'write some story about ' + storyname + ' and give some line by line prompts for image generation in stable diffusion for every 5 seconds related to the script'
#
# prompts = llm(text)
#
# print(prompts)
#
# print(type(prompts))
import streamlit as st
from langchain.llms import Clarifai

CLARIFAI_PAT = "29d9803eb6f34718ba01d597a4a4e3b5"
llm = Clarifai(pat = CLARIFAI_PAT,user_id = 'meta',app_id = 'Llama-2',model_id = 'llama2-70b-chat')


print("INPUT : ")
storyname = st.text_input("ENTER SOME TOPIC")
if(st.button("SUBMIT")):
    text = 'write some story about ' + storyname + ' and give some line by line prompts for image generation in stable diffusion for every 5 seconds related to the script'
    st.write(storyname)
    prompts = llm(text)
    st.write(prompts)
    USER_ID = 'stability-ai'
    APP_ID = 'stable-diffusion-2'
    # Change these to whatever model and text URL you want to use
    MODEL_ID = 'stable-diffusion-xl'
    MODEL_VERSION_ID = '0c919cc1edfc455dbc96207753f178d7'
    TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'

    ############################################################################
    # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
    ############################################################################

    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    PAT = '29d9803eb6f34718ba01d597a4a4e3b5'

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw="A woman slumped over her desk, surrounded by papers and office supplies. Her face is pale and sweaty, and her eyes are closed."
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]

    print("Predicted concepts:")
    for concept in output.data.concepts:
        print("%s %.2f" % (concept.name, concept.value))

    # Uncomment this line to print the full Response JSON
    # parsed_output = json.loads(output)
    # base64 = parsed_output["data"]["image"]["base64"]
    # with open(r'C:\Users\pagal\PycharmProjects\TEXT\utube-vid-text\AI-Video-Generator-Using-OpenAI-Python-main\jobs .txt','w')as f:
    #     f.write(str(base64))

    base64_image = output.data.image.base64

    # print("Base64 image data saved to: ",output_path)
    # print(base64_image)

    import base64
    imgdata = base64.decodebytes(base64_image)
    print(base64_image)
    print(imgdata)
    filename = 'Clarifai_image.jpg'
    with open(filename, 'wb') as f:
        f.write(base64_image)

    from moviepy.editor import *
    from gtts import gTTS
    para = "A woman slumped over her desk, surrounded by papers and office supplies. Her face is pale and sweaty, and her eyes are closed."
    tts = gTTS(text=para, lang='en', slow=False)
    tts.save("Clarifai_audio.mp3")

    audio_clip = AudioFileClip("Clarify_audio.mp3")
    audio_duration = audio_clip.duration

    print("Extract Image Clip and Set Duration...")
    image_clip = ImageClip('Clarifai_image.jpg').set_duration(audio_duration)

    clip = image_clip.set_audio(audio_clip)
    video = CompositeVideoClip([clip])

    video = video.write_videofile("Clarify_video.mp4", fps=24)
    st.video("Clarify_video.mp4")
