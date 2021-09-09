from django.contrib import admin
from django.urls import path
from lts.views import LogisticLogin, NewDatabase,PersonTable,CreatePersonMatter,PersonMatter,PersonDeal
from lts.views import CreateBOMProductList,CreateBOMMatterList,PutPerson,DeletePerson,PutPersonMatter,DeletePersonMatter
from lts.views import BOMProductList, PutBOMProductList,DeleteBOMProductList, BOMMatterList,ShowDatabase
from lts.views import CreateWorkStation, WorkStation, PutWorkStation, DeleteWorkStation, CreateProductPlanDeal
from lts.views import ProductPlanDeal, PutProductPlanDeal, DeleteProductPlanDeal,ProductCodeName,CreateProductPickMatter
from lts.views import ProductPickMatter, PutProductPickMatter, DeleteProductPickMatter, NoPagePersonMatter
from lts.views import CreateProcessDeal, ProcessDeal, PutProcessDeal, DeleteProcessDeal, ProductPlanCodeName
from lts.views import PersonCodeName, WorkCodeName, CreateCheckProductDeal, CreateProductParameter,CheckProductDeal
from lts.views import PutCheckProductDeal, DeleteCheckProductDeal, CreateProductTransitInfo, ProductTransitInfo
from lts.views import MatterNameCode, ProcessNameCode, CurrentUserInfo, ManageLogisticLogin
from lts.views import ProjectSearchWorkcode, GetProductId, UnqualifiedProduct, PutUnqualifiedProduct
from lts.views import DeleteUnqualifiedProduct, QualifiedMatterCode, BomMatterCodeName, WorkStationGetData
from lts.views import FinishedCodeGetMatterCodeID, PutFinishedCodeGetMatterCodeID, DeleteFinishedCodeGetMatterCodeID
from lts.views import Pick, PutPick, DeletePick, FinishedProductStorage, PutFinishedProductStorage
from lts.views import DeleteFinishedProductStorage, stockInStockOut, BackMatter, PutBackMatter, DeleteBackMatter
from lts.views import ModifyFinishProductStatus, MatterSearch, ProductInfoSearch, NoPageMatterSearch,NoPageProductInfoSearch
from lts.views import OperationSystem, PutOperationSystem, DeleteOperationSystem, test, AddModel, PrintApai,ModifyPassword
from lts.views import WorkManage, PutWorkManage, DeleteWorkManage, NoPageProcessMatterDeal,PackCheckFinishedProduct
from lts.views import TransitProductQualifiedSearch, WorkUnqualifiedResult, PutWorkUnqualifiedResult
from lts.views import DeleteWorkUnqualifiedResult, NopageWorkUnqualifiedResultName, OneProductInAllWorkStationInfo
from lts.views import ProductCodeResponseResult, ModifyInWorkStation, test2, FromDataModel, downloads, FinishedProductOut
from lts.views import GetProductOutInfo, AnalyseWorkStationInfo,OneProductLiveDeal, ManagePickMatter, PutManagePickMatter
from lts.views import DeleteManagePickMatter
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
  path('LogisticLogin', LogisticLogin.as_view()),   # 用户侧登录路径
  path('LogisticManageLogisticLogin', ManageLogisticLogin.as_view()),  # 管理侧登录路径
  path('LogisticShowDatabase', ShowDatabase.as_view()),   # 展示数据库里面的所有表格
  path('LogisticNewDatabase', NewDatabase.as_view()),  # 新建数据库路径
  path('LogisticPersonTable', PersonTable.as_view()),  # 个人详情数据表
  path('LogisticCreatePersonMatter', CreatePersonMatter.as_view()),  # 创建物料详情结构表
  path('LogisticPersonMatter', PersonMatter.as_view()),  # 创建物料详情表(新增和查询)
  path('LogisticPutPersonMatter', PutPersonMatter.as_view()),  # 创建物料详情表(修改)
  path('LogisticDeletePersonMatter', DeletePersonMatter.as_view()),  # 创建物料详情表(删除)
  path('LogisticPersonDeal', PersonDeal.as_view()),  # 人员调取接口（新增和查询）
  path('LogisticPutPerson', PutPerson.as_view()),  # 人员调取接口（修改）
  path('LogisticDeletePerson', DeletePerson.as_view()),  # 人员调取接口（删除）
  path('LogisticCreateBOMProductList', CreateBOMProductList.as_view()),  # 创建产品列表结构表
  path('LogisticCreateBOMMatterList', CreateBOMMatterList.as_view()),  # 创建物料列表结构表
  path('LogisticBOMProductList', BOMProductList.as_view()),  # 查询新建产品列表
  path('LogisticPutBOMProductList', PutBOMProductList.as_view()),  # 修改产品列表（修改）
  path('LogisticDeleteBOMProductList', DeleteBOMProductList.as_view()),  # 删除产品列表（删除）
  path('LogisticBOMMatterList', BOMMatterList.as_view()),  # 新增查询物料列表（新增/删除）
  path('LogisticCreateWorkStation', CreateWorkStation.as_view()),  # 创建工站信息表结构表
  path('LogisticWorkStation', WorkStation.as_view()),  # 创建工站信息表信息表
  path('LogisticPutWorkStation', PutWorkStation.as_view()),  # 修改工站信息表信息表
  path('LogisticDeleteWorkStation', DeleteWorkStation.as_view()),  # 删除工站信息表信息表
  path('LogisticCreateProductPlanDeal', CreateProductPlanDeal.as_view()),  # 创建生产计划详情结构表
  path('LogisticProductPlanDeal', ProductPlanDeal.as_view()),  # 新增查询生产计划详情表
  path('LogisticPutProductPlanDeal', PutProductPlanDeal.as_view()),  # 修改生产计划详情表
  path('LogisticDeleteProductPlanDeal', DeleteProductPlanDeal.as_view()),  # 修改生产计划详情表
  path('LogisticProductCodeName', ProductCodeName.as_view()),  # 产品名称和内码查询
  path('LogisticCreateProductPickMatter', CreateProductPickMatter.as_view()),  # 创建物料领料详情表
  path('LogisticProductPickMatter', ProductPickMatter.as_view()),  # 新增查询物料领表详情
  path('LogisticPutProductPickMatter', PutProductPickMatter.as_view()),  # 修改物料领表详情
  path('LogisticDeleteProductPickMatter', DeleteProductPickMatter.as_view()),  # 删除物料领表详情
  path('LogisticNoPagePersonMatter', NoPagePersonMatter.as_view()),  # 不分页的物料详情表接口
  path('LogisticCreateProcessDeal', CreateProcessDeal.as_view()),  # 工序结构详情表接口
  path('LogisticProcessDeal', ProcessDeal.as_view()),  # 新增查询工序详情表
  path('LogisticPutProcessDeal', PutProcessDeal.as_view()),  # 修改工序详情表
  path('LogisticDeleteProcessDeal', DeleteProcessDeal.as_view()),  # 删除工序详情表
  # path('LogisticProductPlanCodeName', ProductPlanCodeName.as_view()),  # 生产计划内码和名称表
  path('LogisticProductPlanCodeName', ProductPlanCodeName.as_view()),  # 生产计划内码和名称表
  path('LogisticPersonCodeName', PersonCodeName.as_view()),  # 人员内码和名称表
  path('LogisticWorkCodeName', WorkCodeName.as_view()),  # 工站内码和名称表
  path('LogisticCreateCheckProductDeal', CreateCheckProductDeal.as_view()),  # 创建检验产品详情表结构v表
  path('LogisticCreateProductParameter', CreateProductParameter.as_view()),  # 创建检验产品参数结构v表
  path('LogisticCheckProductDeal', CheckProductDeal.as_view()),  # 新增查询检查详情表
  path('LogisticPutCheckProductDeal', PutCheckProductDeal.as_view()),  # 修改检查详情表
  path('LogisticDeleteCheckProductDeal', DeleteCheckProductDeal.as_view()),  # 删除检查详情表
  path('LogisticCreateProductTransitInfo', CreateProductTransitInfo.as_view()),  # 创建产品过站信息结构表
  path('LogisticProductTransitInfo', ProductTransitInfo.as_view()),  # 查询产品过站信息结构表
  path('LogisticMatterNameCode', MatterNameCode.as_view()),  # 物料内码和物料名称
  path('LogisticProcessNameCode', ProcessNameCode.as_view()),  # 物料内码和物料名称
  path('LogisticCurrentUserInfo', CurrentUserInfo.as_view()),  # 当前登录人的信息
  # path('Logistictest', test.as_view()),  # 测试
  path('LogisticProjectSearchWorkcode', ProjectSearchWorkcode.as_view()),  # 根据前端传入的project_id 得到work_station
  path('LogisticGetProductId', GetProductId.as_view()),  # 根据前端传入的project_id 得到work_station
  path('LogisticUnqualifiedProduct', UnqualifiedProduct.as_view()),  # 不良品查询
  path('LogisticPutUnqualifiedProduct', PutUnqualifiedProduct.as_view()),  # 不良品修改
  path('LogisticDeleteUnqualifiedProduct', DeleteUnqualifiedProduct.as_view()),  # 不良品查询
  path('LogisticQualifiedMatterCode', QualifiedMatterCode.as_view()),  # 前端传入一个物料内码，寻找上一站的物料是否合格
  path('LogisticBomMatterCodeName', BomMatterCodeName.as_view()),  # 得到mattercode和matter_name
  path('LogisticWorkStationGetData', WorkStationGetData.as_view()),  # 得到workstaion
  path('LogisticFinishedCodeGetMatterCodeID', FinishedCodeGetMatterCodeID.as_view()),  # 前端传入成品码 根据成品码得到陈成品码下面的物料等信息(产品维修工站的接口)
  path('LogisticPutFinishedCodeGetMatterCodeID', PutFinishedCodeGetMatterCodeID.as_view()),  # 修改成品码的物料信息
  path('LogisticDeleteFinishedCodeGetMatterCodeID', DeleteFinishedCodeGetMatterCodeID.as_view()),  # 删除成品码的物料等信息和删除成品码
  path('LogisticPick', Pick.as_view()),  # 包装管理的包装箱查询新增
  path('LogisticPutPick', PutPick.as_view()),  # 包装管理的包装箱修改
  path('LogisticDeletePick', DeletePick.as_view()),  # 包装管理的包装箱删除
  path('LogisticFinishedProductStorage', FinishedProductStorage.as_view()),  # 成品入包装接口（包i装过站接口）
  path('LogisticPutFinishedProductStorage', PutFinishedProductStorage.as_view()),  # 成品修改包装接口
  path('LogisticDeleteFinishedProductStorage', DeleteFinishedProductStorage.as_view()),  # 成品删除包装接口
  path('LogisticstockInStockOut', stockInStockOut.as_view()),  # 成品出入库状态（成品出入库工站接口）
  path('LogisticBackMatter', BackMatter.as_view()),  # 生产退料查询新增
  path('LogisticPutBackMatter', PutBackMatter.as_view()),  # 生产退料修改
  path('LogisticDeleteBackMatter', DeleteBackMatter.as_view()),  # 生产退料删除
  path('LogisticModifyFinishProductStatus', ModifyFinishProductStatus.as_view()),  # 改变成品状态(检验过站接口)
  path('LogisticMatterSearch', MatterSearch.as_view()),  # 物料查询
  path('LogisticProductInfoSearch', ProductInfoSearch.as_view()),  # 产品信息查询
  path('LogisticNoPageMatterSearch', NoPageMatterSearch.as_view()),  # 不分页的物料信息查询
  path('LogisticOperationSystem', OperationSystem.as_view()),  # 查询和新增的接口
  path('LogisticPutOperationSystem', PutOperationSystem.as_view()),  # 修改接口
  path('LogisticDeleteOperationSystem', DeleteOperationSystem.as_view()),  # 删除接口
  path('Logistictest', test.as_view()),  # 测试
  path('LogisticPrintApai', PrintApai.as_view()),  # 测试
  path('LogisticAddModel', AddModel.as_view()),  # 测试
  path('LogisticModifyPassword', ModifyPassword.as_view()),  # 修改密码
  path('LogisticNoPageProductInfoSearch', NoPageProductInfoSearch.as_view()),  # 不分页的产品查询
  path('LogisticWorkManage', WorkManage.as_view()),  # 工站数据表新增和查询
  path('LogisticPutWorkManage', PutWorkManage.as_view()),  # 工站数据表新增和查询
  path('LogisticDeleteWorkManage', DeleteWorkManage.as_view()),  # 工站数据表新增和查询
  path('LogisticNoPageProcessMatterDeal', NoPageProcessMatterDeal.as_view()), # 寻找工站的最大包装数量（不能超过包装的最大数量）
  path('LogisticPackCheckFinishedProduct', PackCheckFinishedProduct.as_view()), # 包装前的产品编号检验是否合格,合格才包装
  path('LogisticTransitProductQualifiedSearch', TransitProductQualifiedSearch.as_view()), # 产品过站合格不合格信息查询
  path('LogisticWorkUnqualifiedResult', WorkUnqualifiedResult.as_view()), # 工站和不良原因表（新增和查询） 在管理端
  path('LogisticPutWorkUnqualifiedResult', PutWorkUnqualifiedResult.as_view()), # 修改工站和不良原因表
  path('LogisticDeleteWorkUnqualifiedResult', DeleteWorkUnqualifiedResult.as_view()), # 删除工站和不良原因表
  path('LogisticNopageWorkUnqualifiedResultName', NopageWorkUnqualifiedResultName.as_view()), # 不分页的返回不合格原因内码和不合格原因名称
  path('LogisticOneProductInAllWorkStationInfo', OneProductInAllWorkStationInfo.as_view()), # 产品的生命周期（一个产品在各个工站的信息）
  path('LogisticProductCodeResponseResult', ProductCodeResponseResult.as_view()), # 传入的成品码 返回他的不合格原因内码
  path('LogisticModifyInWorkStation', ModifyInWorkStation.as_view()),
  path('Logistictest2', test2.as_view()),
  path('LogisticFromDataModel', FromDataModel.as_view()),
  path('Logisticdownloads', downloads.as_view()),
  path('LogisticFinishedProductOut', FinishedProductOut.as_view()),
  path('LogisticGetProductOutInfo', GetProductOutInfo.as_view()),
  path('LogisticAnalyseWorkStationInfo', AnalyseWorkStationInfo.as_view()),
  path('LogisticOneProductLiveDeal', OneProductLiveDeal.as_view()),
  path('LogisticManagePickMatter', ManagePickMatter.as_view()),
  path('LogisticPutManagePickMatter', PutManagePickMatter.as_view()),
  path('LogisticDeleteManagePickMatter', DeleteManagePickMatter.as_view()),
]
# urlpatterns += staticfiles_urlpatterns()
