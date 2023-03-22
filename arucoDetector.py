import cv2

class arucoDetector():

	def __init__(self) -> None:
		self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
		self.arucoParams = cv2.aruco.DetectorParameters()	

	def arucoDetect(self, imgArr):
		corners, ids, _ = cv2.aruco.detectMarkers(
				imgArr, self.arucoDict, parameters=self.arucoParams)
		return corners, ids

	def drawArucos(self, imgArr):
		corners, ids = self.arucoDetect(imgArr)
		drawnImg = cv2.aruco.drawDetectedMarkers(imgArr.copy(), corners, ids, (0,255,0))
		return drawnImg
		
if __name__=="__main__":
	aru = arucoDetector()
	img = cv2.imread("images/aruco_check.png")
	cv2.imwrite("images/arucoSaver.png",aru.drawArucos(img.copy()))
	cv2.imshow("img", aru.drawArucos(img))
	cv2.waitKey(0)
	
	corners, ids = aru.arucoDetect(img)
	print(corners)
	print(ids)
	cv2.destroyAllWindows()