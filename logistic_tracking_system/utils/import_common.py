import os.path



class test11:
    def sub(self, stem1, stem2, stem3, stem4, stem5, stem6, print_path):
        Get_items = stem1
        Get_supplier = stem2
        pub_N_box = stem3
        Get_No = stem4
        Get_Rev = stem5
        date_one = stem6
        print_path = print_path
        str_all = '''
            Private Sub print_SN()
            Dim 打印内容 As String
            Dim bat文件内容 As String
            Dim 打印txt文件 As Object
            Dim 打印bat文件 As Object
            Dim fs As Object
            打印内容 = "^XA
        ^PW1300
        ^LL0827
        ^LH0,60
        ^FO480,50
        ^AS,30,30
        ^FDFlex Part Number^FS
        ^FO65,90
        ^BCN,100,Y,N,N
        ^FD" & {0} & "^FS
    
        ^FO150,270
        ^AS,30,30
        ^FDVendor Code^FS
        ^FO20,310
        ^BCN,100,Y,N,N
        ^FD" & {1} & "^FS
    
        ^FO525,270
        ^AS,30,30
        ^FDPart QTY/P^FS
        ^FO465,310
        ^BCN,100,Y,N,N
        ^FD " & {2} & "^FS
    
        ^FO815,270
        ^AS,30,30
        ^FDPackage Sequence^FS
        ^FO740,310
        ^BCN,100,Y,N,N
        ^FD " & Str(pub_No_box) & "-" & {3} & "^FS
    
        ^FO275,480
        ^AS,30,30
        ^FDPart Revision^FS
        ^FO200,520
        ^BCN,100,Y,N,N
        ^FD" & {4} & "^FS
    
        ^FO640,480
        ^AS,30,30
        ^FDManufacturing Date^FS
        ^FO583,520
        ^BCN,100,Y,N,N
        ^FD" & pub_{5} & "^FS
        '''
        if os.path.exists(print_path):
            pass
        else:
            os.makedirs(print_path)
        path_one = os.path.join(print_path, "text1")
        str_all = str_all.format(Get_items, Get_supplier, pub_N_box, Get_No, Get_Rev, date_one)
        with open(path_one, "w", encoding="utf-8") as f:
            f.write(str_all)
    def zhou(self, stem1, stem2, stem3, stem4, stem5, stem6, print_path):
        Get_items = stem1
        Get_supplier = stem2
        pub_N_box = stem3
        Get_No = stem4
        Get_Rev = stem5
        date_one = stem6
        print_path = print_path
        str_all = '''
            Private Sub print_SN()
            Dim 打印内容 As String
            Dim bat文件内容 As String
            Dim 打印txt文件 As Object
            Dim 打印bat文件 As Object
            Dim fs As Object
            打印内容 = "^XA
        ^PW1300
        ^LL0827
        ^LH0,60
        ^FO480,50
        ^AS,30,30
        ^FDFlex Part Number^FS
        ^FO65,90
        ^BCN,100,Y,N,N
        ^FD" & {0} & "^FS
    
        ^FO150,270
        ^AS,30,30
        ^FDVendor Code^FS
        ^FO20,310
        ^BCN,100,Y,N,N
        ^FD" & {1} & "^FS
    
        ^FO525,270
        ^AS,30,30
        ^FDPart QTY/P^FS
        ^FO465,310
        ^BCN,100,Y,N,N
        ^FD " & {2} & "^FS
    
        ^FO815,270
        ^AS,30,30
        ^FDPackage Sequence^FS
        ^FO740,310
        ^BCN,100,Y,N,N
        ^FD " & Str(pub_No_box) & "-" & {3} & "^FS
    
        ^FO275,480
        ^AS,30,30
        ^FDPart Revision^FS
        ^FO200,520
        ^BCN,100,Y,N,N
        ^FD" & {4} & "^FS
    
        ^FO640,480
        ^AS,30,30
        ^FDManufacturing Date^FS
        ^FO583,520
        ^BCN,100,Y,N,N
        ^FD" & pub_{5} & "^FS
        '''
        if os.path.exists(print_path):
            pass
        else:
            os.makedirs(print_path)
        path_one = os.path.join(print_path, "text1")
        str_all = str_all.format(Get_items, Get_supplier, pub_N_box, Get_No, Get_Rev, date_one)
        with open(path_one, "w", encoding="utf-8") as f:
            f.write(str_all)

    def tets(self):
        pass