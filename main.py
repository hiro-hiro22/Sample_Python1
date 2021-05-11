import streamlit as st
from PIL import Image
import requests
from PIL import ImageDraw,ImageFont
import io

st.title('顔認識アプリ')

subscription_key='fad155da11e841cc84a336142a2fa2a2'
assert subscription_key

face_api_url='https://hiro0324.cognitiveservices.azure.com/face/v1.0/detect'


uploaded_file=st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
    img=Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output,format="JPEG")
        binary_img=output.getvalue()#バイナリ取得
    
    headers={
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    params={
        'returnFaceId':'true',
        'returnFaceAttributes':'age, gender, headPose, smile, facialHair, glasses, emotion, hair, makeup, occlusion, accessories, blur, exposure'
    }

    res=requests.post(face_api_url,params=params,headers= headers,data=binary_img)  

    draw=ImageDraw.Draw(img)
    results=res.json()
    for result in  results:
    
        rect=result['faceRectangle']
    
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green',width=5)
        draw_x=rect['left']
        draw_y=rect['top']-15
        
        text = result['faceAttributes']['gender']+'/'+str(result['faceAttributes']['age'])
        draw.text((draw_x,draw_y),text,fill='red')


    st.image(img, caption='Uploaded Image.', use_column_width=True)


