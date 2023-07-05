# py_opencv_identify
py+opencv+flask - 自用人脸模型建立+人脸识别api

注意:\
人脸建模上传文件格式:\
    user.id.序列.后缀
    
后缀支持:\
    jpg
    jpeg
    
使用\
    1.cd 到主模块 (pymain)\
    2.flask --app FaceIdentify run\
    3.按需访问相关api\
        3.1 人脸建模\
            3.1.0 参数\ 
                (1)file require\
                (2)modelId unrequire
            3.1.1 参数释义\ 
                (1)file必传不传会返回异常\ 
                (2)传递可指定id,不传递生成随机id;modelId在第一次建模的时候会返回,建议持久化;已建立过模型,想要提高校验准确度则需要传递自定义或随机modelId;\
        3.2 人脸检测\
            3.2.0 参数\
                (1)file require\
                (2)modelId require\
            3.2.1 参数释义\
                (1)必填\
                (2)必填,第一次建模会返回modelId 建议持久化
            
