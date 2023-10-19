import cv2
import io
import easyocr
import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

def interference(img):
    dh, dw, _ = img.shape
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)
    buffered = io.BytesIO()
    pilImage.save(buffered, quality=100, format="JPEG")
    m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

    response = requests.post("<your roboflow api key>", data=m,
                             headers={'Content-Type': m.content_type})
    # print(response)
    # print(response.json())
    return response.json()['predictions']

def plate(predictions,img):
    img_copy = img
    try:
        for prediction in predictions:
            if prediction['confidence'] > 0.25:
                x = int(prediction['x'])
                y = int(prediction['y'])
                w = int(prediction['width'])
                h = int(prediction['height'])

                gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
                crop_img = gray[int(y - h / 2):int(y + h / 2), int(x - w / 2):int(x + w / 2)]
                reader = easyocr.Reader(['en'])
                number = reader.readtext(crop_img)
                # try:
                #     plate=number[len(number) - 1][1]
                #     dictionary[plate]={x,y,w,h}
                # except IndexError:
                #     continue
                # return dictionary
                img = cv2.rectangle(img, (int((x - w / 2)), int((y - h / 2))), (int((x + w / 2)), int((y + h / 2))),
                                    (0, 255, 0), 2)
                try:
                    cv2.putText(img, number[len(number) - 1][1], (int((x - w / 2)) + 6, int((y + h / 2)) - 6),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    print(number)
                except IndexError:
                    continue

                # print(number[len(number) - 1][1])
                # pr.recognizer(crop_img)
                # cv2.imshow("cropped", crop_img)
    except:
        return
    cv2.imshow("image", img)
    cv2.waitKey(1)
# def track(previous,current):
#     list=[]
#     for x in previous.keys():
#         for y in current.keys():
#             if x==y and previous[x]== current[y]:
#                 break
#             else:
#                 list.append(x)
#     return list
# def predict(video):
#     cap = cv2.VideoCapture(video)
#     previous={}
#     current={}
#     misplaced={}
#     while True:
#         ret, frame = cap.read()
#     # frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         if ret==True:
#             predictions=interference(frame)
#             current =plate(predictions,frame)
#             misplaced = track(previous,current)
#         else:
#             cap.release()
#             break
#     return misplaced
#     # if cv2.waitKey(1) == 13:
#     #     break
#     # cv2.destroyAllWindows()
# # res=predict("sample.mp4")
# img=cv2.imread("car.jpg")
# res = interference(img)
# print(res)
