(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-e03b87b0"],{"020f":function(t,e,o){},2949:function(t,e,o){"use strict";o("020f")},"93b0":function(t,e,o){"use strict";var r=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"login-container"},[o("el-form",{ref:"loginData",staticClass:"login-page",attrs:{model:t.loginData,rules:t.rules2,"status-icon":"","label-position":"left","label-width":"100px"}},[o("h3",{staticClass:"title"},[t._v("iMotion MTS "+t._s(t.formTitle))]),o("el-form-item",{attrs:{label:"项目",prop:"product_id"}},[o("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择",clearable:""},on:{change:t.getWorkCodeNameSearchList},model:{value:t.loginData.product_id,callback:function(e){t.$set(t.loginData,"product_id",e)},expression:"loginData.product_id"}},t._l(t.ProductIdNameList,(function(t,e){return o("el-option",{key:e+" search",attrs:{label:t.product_name,value:t.product_id}})})),1)],1),"- 后台"!=t.formTitle&&t.loginData.product_id?o("el-form-item",{attrs:{label:"工站",prop:"work_id"}},[o("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择"},model:{value:t.loginData.work_id,callback:function(e){t.$set(t.loginData,"work_id",e)},expression:"loginData.work_id"}},t._l(t.WorkCodeNameSearchList,(function(t,e){return o("el-option",{key:e+" search",attrs:{label:t.work_id+"_"+t.work_name,value:t.work_id}})})),1)],1):t._e(),o("el-form-item",{attrs:{label:"用户名",prop:"user"}},[o("el-input",{attrs:{type:"text","auto-complete":"off",placeholder:"用户名"},model:{value:t.loginData.user,callback:function(e){t.$set(t.loginData,"user",e)},expression:"loginData.user"}})],1),o("el-form-item",{attrs:{label:"密码",prop:"password"}},[o("el-input",{attrs:{type:"password","auto-complete":"off",placeholder:"密码"},model:{value:t.loginData.password,callback:function(e){t.$set(t.loginData,"password",e)},expression:"loginData.password"}})],1),o("div",{staticStyle:{"text-align":"right","margin-bottom":"22px",color:"#3185dc"}},[o("span",{staticStyle:{cursor:"pointer"},on:{click:t.gotoLogin}},[t._v("跳转到："+t._s(t.toLoginUrlTitle))])]),o("div",{staticStyle:{"text-align":"center","margin-bottom":"22px"}},[o("el-button",{staticStyle:{width:"80%"},attrs:{type:"primary",loading:t.logining},on:{click:t.handleSubmit}},[t._v("登录")])],1)],1)],1)},i=[],n=o("1da1"),a=o("5530"),s=(o("96cf"),o("fd03")),l=o("2f62"),c={props:{toUrl:{type:String,default:"/"},toLoginUrl:{type:String,default:"/"},formTitle:{type:String,default:""},toLoginUrlTitle:{type:String,default:""}},computed:Object(a["a"])({},Object(l["c"])(["ProductIdNameList","WorkCodeNameSearchList","CurrentUserInfo"])),data:function(){return{logining:!1,loginData:{product_id:"",work_id:"",user:"",password:""},rules2:{product_id:[],work_id:[{required:!0,message:"请选择工站",trigger:"change"}],user:[{required:!0,message:"请输入用户名",trigger:"blur"}],password:[{required:!0,message:"请输入密码",trigger:"blur"}]},checked:!1}},created:function(){window.addEventListener("keydown",this.handleKeyDown,!0)},methods:Object(a["a"])(Object(a["a"])({},Object(l["b"])(["getLogisticGetProductId","getLogisticProjectSearchWorkcode","getLogisticCurrentUserInfo"])),{},{gotoLogin:function(){this.$router.push({path:this.toLoginUrl})},getWorkCodeNameSearchList:function(){"- 后台"!=this.formTitle&&this.getLogisticProjectSearchWorkcode({product_id:this.loginData.product_id})},handleSubmit:function(){var t=this;console.log(this.loginData),this.$refs.loginData.validate((function(e){e?"- 后台"!=t.formTitle?s["b"].getLogisticLogin(t.loginData).then((function(e){console.log("登录信息",e),e&&0==e.code?(t.getLogisticCurrentUserInfo(),s["b"].getLogisticCurrentUserInfo().then((function(e){console.log("当前登陆人的接口 用户端",e),0==e.code&&("加工"==t.CurrentUserInfo.work_type?t.$router.push({path:"/userUrl/MissStation"}):"维修"==t.CurrentUserInfo.work_type?t.$router.push({path:"/userUrl/MissStationM"}):"检验"==t.CurrentUserInfo.work_type||"测试"==t.CurrentUserInfo.work_type?t.$router.push({path:"/userUrl/ProductLifecycleSearch"}):"包装"==t.CurrentUserInfo.work_type?t.$router.push({path:"/userUrl/MissStationPack"}):"入库出库"==t.CurrentUserInfo.work_type?t.$router.push({path:"/userUrl/FinishedProductDispatch"}):t.$router.push({path:t.toUrl}))}))):t.$message({message:e.message,type:"error"})})):s["b"].getLogisticManageLogisticLogin(t.loginData).then((function(e){console.log("登录信息",e),e&&0==e.code?(t.getLogisticCurrentUserInfo(),s["b"].getLogisticCurrentUserInfo().then((function(e){console.log("当前登陆人的接口 管理端",e),"其他"==t.CurrentUserInfo.user_role?t.$router.push({path:"/DashBoard"}):t.$router.push({path:t.toUrl})}))):t.$message({message:e.message,type:"error"})})):t.$message({message:"请修改正确的数据格式！",type:"warning"})}))},handleKeyDown:function(t){var e=null;e=void 0===window.event?t.keyCode:window.event.keyCode,13===e&&this.handleSubmit()},getProductIdNameList:function(){var t=this;return Object(n["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,t.getLogisticGetProductId();case 2:case"end":return e.stop()}}),e)})))()}}),mounted:function(){this.getProductIdNameList(),"- 后台"!=this.formTitle?this.rules2.product_id=[{required:!0,message:"请选择项目",trigger:"change"}]:this.rules2.product_id=[],console.log("this.CurrentUserInfo CurrentUserInfo",this.CurrentUserInfo)}},u=c,d=(o("2949"),o("2877")),g=Object(d["a"])(u,r,i,!1,null,"6563623b",null);e["a"]=g.exports},de78:function(t,e,o){"use strict";o.r(e);var r=function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("CommonLogin",{attrs:{formTitle:t.formTitle,toLoginUrlTitle:t.toLoginUrlTitle,toUrl:t.toUrl,toLoginUrl:t.toLoginUrl}})},i=[],n=o("93b0"),a={name:"UserLogin",data:function(){return{formTitle:"",toUrl:"/userUrl/DashBoard",toLoginUrlTitle:"后台",toLoginUrl:"/ManagerLogin"}},components:{CommonLogin:n["a"]}},s=a,l=o("2877"),c=Object(l["a"])(s,r,i,!1,null,null,null);e["default"]=c.exports}}]);
//# sourceMappingURL=chunk-e03b87b0.1e59ce2c.js.map