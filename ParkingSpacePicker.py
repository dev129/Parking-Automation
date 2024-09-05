import cv2 
import pickle # save the places/position of aprking space an bring to main code 

img=cv2.imread('carParkImg.png')
width,height=107,48 #width and height of rectangle 
try:
    with open('CarParkPos', 'rb') as f: #check wheteher an object is present or not 
        posList = pickle.load(f) #if CarParkPos file is present then assign its value in posList array 
except:
    posList = [] #every posiiton has x and y to which height and width shall be added 

def mouseClick(events, x, y, flags, params):#takes 4 inputs whic is the event which just happened , x ,y corodiantes,  flags and parameter 
    if events == cv2.EVENT_LBUTTONDOWN: #if we press left button then append to my list 
        posList.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:  # Right button click to delete
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i) #delete whatever is in the i value
                break
    with open('CarParkPos', 'wb') as f: #store the posList using pickle object in CarParkPos file with read and write permission 
        pickle.dump(posList, f) #this helps in dumping posList in file 

cv2.imshow("image", img) #Give the title of the image which is to be displayed /showed
cv2.setMouseCallback("image", mouseClick) #mouse clcik function

while True:
    img = cv2.imread('carParkImg.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)    
    
    '''
    #create reactnagle at the image(testing)
    cv2.rectangle(img,(50,192),(157,240),(255,0,255),2) #recatngle around img, starting from 100,100 and ending at 200,150 with color r-255, b-255 and g-0 (meaning purple) and thickness 2. We set teh size of our rectangle   this heplp inf ixing the size and then only intintal posiiton is needed . It is a hit and trial method to find the dimension of rectangle 
    '''
    
    cv2.imshow("image", img) #Give the title of the image which is to be displayed /showed
    #To detect mouse click
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Escape key to exit
        break

cv2.destroyAllWindows() 
