import copy

class DBMaskCreative:
    CreativeID :int
    VideoID:int
    PicID:int
    ContentID  :int
    ProductID :int

    def toModel(self,re):
        try:
            reDB = list[DBMaskCreative]
            for item in re:
                tmp = DBMaskCreative
                tmp.CreativeID = item[0]
                tmp.VideoID = item[1]
                tmp.PicID = item[2]
                tmp.ContentID = item[3]
                tmp.ProductID = item[4]
                reDB.append(tmp)
        except:
            print("DBMaskCreative toModel Error data:",re)
        
        return reDB

    def toModelFirstLine(self,re):
        try:
                tmp = DBMaskCreative
                tmp.CreativeID = re[0][0]
                tmp.VideoID = re[0][1]
                tmp.PicID = re[0][2]
                tmp.ContentID = re[0][3]
                tmp.ProductID = re[0][4]
        except:
            print("DBMaskCreative toModelFirstLine Error data:",re)
        
        return tmp


class DBMaskVideo:
    VideoID:int
    VideoSrc  :str
    VideoName :str
    VideoAccount:str
    def __init__(self):
        self.VideoID = 0
        self.VideoSrc = ''
        self.VideoName = ''
        self.VideoAccount = ''

    def toModel(self,re):
        try:
            reDB = list[DBMaskVideo]
            for item in re:
                tmp = DBMaskVideo()
                tmp.VideoID = item[0]
                tmp.VideoSrc = item[1]
                tmp.VideoName = item[2]
                tmp.VideoAccount = item[3]
                reDB.append(tmp)
        except:
            print("DBMaskVideo toModel Error data:",re)
        
        return reDB

    def toModelFirstLine(self,re):
        try:
                tmp = DBMaskVideo()
                tmp.VideoID = re[0][0]
                tmp.VideoSrc = re[0][1]
                tmp.VideoName = re[0][2]
                tmp.VideoAccount = re[0][3]
        except:
            print("DBMaskVideo toModelFirstLine Error data:",re)
        
        return tmp

class DBMaskPicture:
    PicID :int
    PicName:str

    def toModel(self,re):
        try:
            reDB = list[DBMaskPicture]
            for item in re:
                tmp = DBMaskPicture
                tmp.PicID = item[0]
                tmp.PicName = item[1]
                reDB.append(tmp)
        except:
            print("DBMaskPicture toModel Error data:",re)
        
        return reDB

    def toModelFirstLine(self,re):
        try:
                tmp = DBMaskPicture
                tmp.PicID = re[0][0]
                tmp.PicName = re[0][1]
        except:
            print("DBMaskPicture toModelFirstLine Error data:",re)
        
        return tmp

class DBMaskTask:
    TaskUUID :str
    CreativeID :int
    Status:int
    OutVideoSrc:str
    CreateTime:str
    def __init__(self):
        self.TaskUUID = ''
        self.Status = 0
        self.OutVideoSrc = ''
        self.CreateTime = ''
        self.CreativeID = 0


    def toModel(self,re):
        try:
            reDB = list[DBMaskTask]
            for item in re:
                tmp = DBMaskTask()
                tmp.TaskUUID = item[0]
                tmp.CreativeID = item[1]
                tmp.Status = item[2]
                tmp.OutVideoSrc = item[3]
                tmp.CreateTime = item[4]
                reDB.append(tmp)
        except:
            print("DBMaskTask toModel Error data:",re)
        
        return reDB

    def toModelFirstLine(self,re):
        try:
            tmp = DBMaskTask()
            tmp.TaskUUID = re[0][0]
            tmp.CreativeID = re[0][1]
            tmp.Status = re[0][2]
            tmp.OutVideoSrc = re[0][3]
            tmp.CreateTime = re[0][4]
        except:
            print("DBMaskTask toModelFirstLine Error data:",re)
        
        return tmp

class DBMaskContent:
    ContentID  :int
    VideoContent :str
    PostContent: str

    def toModel(self,re):
        try:
            reDB = list[DBMaskContent]
            for item in re:
                tmp = DBMaskContent
                tmp.ContentID = item[0]
                tmp.VideoContent = item[1]
                tmp.PostContent = item[2]
                reDB.append(tmp)
        except:
            print("DBMaskContent toModel Error data:",re)
        
        return reDB

    def toModelFirstLine(self,re):
        try:
                tmp = DBMaskContent
                tmp.ContentID = re[0][0]
                tmp.VideoContent = re[0][1]
                tmp.PostContent = re[0][2]
        except:
            print("DBMaskContent toModelFirstLine Error data:",re)
        
        return tmp

class DBMaskProduct:
    ID:int
    ProductID:int
    ProductName:str
    def __init__(self):
        self.ID = 0
        self.ProductID = 0
        self.ProductName = ''

    def toModel(self,re):
        try:
            reDB = list()
            for item in re:
                reDB.append(item[2])
        except Exception as e:
            print("DBMaskProduct toModel Error data:",re,"error:",e)
        
        return reDB

    def toModelFirstLine(self,re):
        try:
            tmp = DBMaskProduct
            tmp.ID = re[0][0]
            tmp.ProductID = re[0][1]
            tmp.ProductName = re[0][2]
        except:
            print("DBMaskProduct toModelFirstLine Error data:",re)
        
        return tmp
    
class UsoProduct:
    ID:int
    ProductName:str
    ProductDir:str
    def __init__(self):
        self.ID = 0
        self.ProductName = 0
        self.ProductDir = ''

    def toModelList(self,re):
        try:
            reDB = list()
            for t in re:
                tmp = UsoProduct()
                tmp.ID =t[0]
                tmp.ProductName = t[1]
                reDB.append(tmp)

        except Exception as e:
            print("UsoProduct toModelList Error data:",re,"error:",e)
        
        return reDB

    def toModelFirstLine(self,re):
        try:
            tmp = UsoProduct()
            tmp.ID = re[0][0]
            tmp.ProductName = re[0][1]
            tmp.ProductDir = re[0][2]
        except:
            print("UsoProduct toModelFirstLine Error data:",re)
        
        return tmp
    
class UsoVideo:
    ID:int
    ProductID:int
    VideoLength:float
    VideoName:str
    VideoType:str
    UploadPerson:str
    UpdateTime:str
    VideoFullPath:str

    def __init__(self):
        self.ID = 0
        self.ProductID = 0
        self.VideoLength = 0.0
        self.VideoName = ''
        self.VideoType = ''
        self.UploadPerson = ''
        self.UpdateTime = ''
        self.VideoFullPath = ''

    def toIDList(self,re):
        try:
            reDB = list()
            for item in re:
                reDB.append(item[0])

        except Exception as e:
            print("UsoVideo toIDList Error data:",re,"error:",e)
        
        return reDB

    def toModelList(self,re):
        try:
            reDB = list()
            for t in re:
                tmp = UsoVideo()
                tmp.ID =t[0]
                tmp.ProductID = t[1]
                tmp.VideoLength =t[2]
                tmp.VideoName = t[3]
                tmp.VideoType = t[4]
                tmp.UploadPerson = t[5]
                tmp.UpdateTime = t[6]
                tmp.VideoFullPath = t[7]
                reDB.append(tmp)

        except Exception as e:
            print("UsoVideo toModelList Error data:",re,"error:",e)
        
        return reDB
    
    def toModelFirstLine(self,re):
        try:
            tmp = UsoVideo
            tmp.ID = re[0][0]
            tmp.ProductID = re[0][1]
            tmp.VideoLength = re[0][2]
            tmp.VideoName = re[0][3]
            tmp.VideoType = re[0][4]
            tmp.UploadPerson = re[0][5]
            tmp.UpdateTime = re[0][6]
            tmp.VideoFullPath = re[0][7]

        except:
            print("UsoVideo toModelFirstLine Error data:",re)
        
        return tmp