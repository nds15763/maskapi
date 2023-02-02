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

    def toModel(self,re):
        try:
            reDB = list[DBMaskVideo]
            for item in re:
                tmp = DBMaskVideo
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
                tmp = DBMaskVideo
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


    def toModel(self,re):
        try:
            reDB = list[DBMaskTask]
            for item in re:
                tmp = DBMaskTask
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
            tmp = DBMaskTask
            tmp.TaskUUID = re[0][0]
            tmp.CreativeID = re[0][1]
            tmp.Status = re[0][2]
            tmp.OutVideoSrc = re[0][3]
            tmp.CreateTime = re[0][4]
        except:
            print("DBMaskTask toModelFirstLine Error data:",re)
        
        return tmp