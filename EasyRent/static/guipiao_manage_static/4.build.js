webpackJsonp([4],{54:function(e,t,a){"use strict";function i(e){a(70)}Object.defineProperty(t,"__esModule",{value:!0});var l=a(72),s=a(73),o=a(13),r=i,n=o(l.a,s.a,!1,r,"data-v-653abffd",null);t.default=n.exports},70:function(e,t,a){var i=a(71);"string"==typeof i&&(i=[[e.i,i,""]]),i.locals&&(e.exports=i.locals);a(3)("6221edef",i,!0)},71:function(e,t,a){t=e.exports=a(2)(void 0),t.push([e.i,".input-width[data-v-653abffd]{width:240px}.demo-upload-list[data-v-653abffd]{display:inline-block;width:60px;height:60px;text-align:center;line-height:60px;border:1px solid transparent;border-radius:4px;overflow:hidden;background:#fff;position:relative;box-shadow:0 1px 1px rgba(0,0,0,.2);margin-right:4px}.demo-upload-list img[data-v-653abffd]{width:100%;height:100%}.demo-upload-list-cover[data-v-653abffd]{display:none;position:absolute;top:0;bottom:0;left:0;right:0;background:rgba(0,0,0,.6)}.demo-upload-list:hover .demo-upload-list-cover[data-v-653abffd]{display:block}.demo-upload-list-cover i[data-v-653abffd]{color:#fff;font-size:20px;cursor:pointer;margin:0 2px}",""])},72:function(e,t,a){"use strict";t.a={data:function(){return{formValidate:{address:"",city:"",region:"",renttype:"",installation:[],paytype:[],minprice:"",maxprice:""},ruleValidate:{address:[{required:!0,message:"详细地址不能为空",trigger:"blur"}],minprice:[{required:!0,message:"请输入最低价格",trigger:"blur"}],maxprice:[{required:!0,message:"请输入最高价格",trigger:"blur"}],price:[{required:!0,message:"请输入价格区间",trigger:"blur"}],city:[{required:!0,message:"请选择城市",trigger:"change"}],region:[{required:!0,message:"请选择区域",trigger:"change"}],renttype:[{required:!0,message:"请选择公寓类型",trigger:"change"}],installation:[{required:!0,type:"array",min:1,message:"至少选择一个",trigger:"change"}],paytype:[{required:!0,type:"array",min:1,message:"至少选择一个",trigger:"change"}]},houseImgName:"",longImgName:"",houseImgVisible:!1,longImgVisible:!1,houseImgList:[],longImgList:[],uploadUrl:this.$api.uploadUrl,url:"/manage/add_house_info"}},methods:{handleSubmit:function(e){var t=this;this.$refs[e].validate(function(e){if(e)if(0==t.houseImgList.length||void 0==t.houseImgList[0].path)t.$Notice.warning({title:"请上传公寓图片"});else if(0==t.longImgList.length||void 0==t.longImgList[0].path)t.$Notice.warning({title:"请上传公寓长图"});else{for(var a="",i=0;i<t.houseImgList.length;i++)a+=t.houseImgList[i].path+",";var l={city:t.formValidate.city,region:t.formValidate.region,images:a,address:t.formValidate.address,minprice:t.formValidate.minprice,maxprice:t.formValidate.maxprice,renttype:t.formValidate.renttype,installation_wifi:t.isInArray(t.formValidate.installation,"无线WIFI")?1:0,installation_kitchen:t.isInArray(t.formValidate.installation,"厨房")?1:0,installation_hoods:t.isInArray(t.formValidate.installation,"油烟机")?1:0,installation_water_heater:t.isInArray(t.formValidate.installation,"热水器")?1:0,installation_washer:t.isInArray(t.formValidate.installation,"洗衣机")?1:0,installation_toilet:t.isInArray(t.formValidate.installation,"卫生间")?1:0,pay_month:t.isInArray(t.formValidate.paytype,"月付")?1:0,pay_season:t.isInArray(t.formValidate.paytype,"季付")?1:0,pay_half:t.isInArray(t.formValidate.paytype,"半年付")?1:0,pay_year:t.isInArray(t.formValidate.paytype,"年付")?1:0,longimage:t.longImgList[0].path};console.log(l),t.$api.post(t.url,l,function(e){console.log(e),e.success?(t.handleReset("formValidate"),t.$refs.upload.fileList=[],t.$refs.longUpload.fileList=[],t.houseImgList=t.$refs.upload.fileList,t.longImgList=t.$refs.longUpload.fileList,t.$Message.success(e.msg)):t.$Message.error(e.msg)})}})},handleReset:function(e){this.$refs[e].resetFields(),this.$refs.upload.fileList=[],this.$refs.longUpload.fileList=[],this.houseImgList=this.$refs.upload.fileList,this.longImgList=this.$refs.longUpload.fileList},handleView:function(e){this.houseImgName=e,this.houseImgVisible=!0},handleLongView:function(e){this.longImgName=e,this.longImgVisible=!0},handleRemove:function(e){var t=this.$refs.upload.fileList;this.$refs.upload.fileList.splice(t.indexOf(e),1)},handleLongRemove:function(e){var t=this.$refs.longUpload.fileList;this.$refs.longUpload.fileList.splice(t.indexOf(e),1)},handleSuccess:function(e,t){console.log(e),console.log(t),e.success&&(t.url=this.$api.imgUrl+e.path,t.name=this.$api.imgUrl+e.path,t.path=e.path)},handleLongSuccess:function(e,t){console.log(e),console.log(t),e.success&&(t.url=this.$api.imgUrl+e.path,t.name=this.$api.imgUrl+e.path,t.path=e.path)},handleFormatError:function(e){this.$Notice.warning({title:"文件格式不正确",desc:"请选择jpg或png格式"})},handleMaxSize:function(e){this.$Notice.warning({title:"文件大小超过限制",desc:"文件大小不能大于2M"})},handleBeforeUpload:function(){var e=this.houseImgList.length<5;return e||this.$Notice.warning({title:"最多只能上传5张图片"}),e},handleBeforeLongUpload:function(){var e=this.longImgList.length<1;return e||this.$Notice.warning({title:"最多只能上传1张长图"}),e},isInArray:function(e,t){for(var a=0;a<e.length;a++)if(t===e[a])return!0;return!1}},mounted:function(){this.houseImgList=this.$refs.upload.fileList,this.longImgList=this.$refs.longUpload.fileList}}},73:function(e,t,a){"use strict";var i=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("Card",[a("p",{attrs:{slot:"title"},slot:"title"},[e._v("公寓信息 / 添加公寓")]),e._v(" "),a("Form",{ref:"formValidate",attrs:{model:e.formValidate,rules:e.ruleValidate,"label-width":80}},[a("FormItem",{attrs:{label:"城市",prop:"city"}},[a("Select",{staticClass:"input-width",attrs:{placeholder:"请选择城市"},model:{value:e.formValidate.city,callback:function(t){e.$set(e.formValidate,"city",t)},expression:"formValidate.city"}},[a("Option",{attrs:{value:"贵阳市"}},[e._v("贵阳市")])],1)],1),e._v(" "),a("FormItem",{attrs:{label:"区域",prop:"region"}},[a("Select",{staticClass:"input-width",attrs:{placeholder:"请选择区域"},model:{value:e.formValidate.region,callback:function(t){e.$set(e.formValidate,"region",t)},expression:"formValidate.region"}},[a("Option",{attrs:{value:"观山湖"}},[e._v("观山湖区")]),e._v(" "),a("Option",{attrs:{value:"南明区"}},[e._v("南明区")]),e._v(" "),a("Option",{attrs:{value:"云岩区"}},[e._v("云岩区")]),e._v(" "),a("Option",{attrs:{value:"花溪区"}},[e._v("花溪区")])],1)],1),e._v(" "),a("FormItem",{attrs:{label:"详细地址",prop:"address"}},[a("Input",{staticClass:"input-width",attrs:{placeholder:"请输入详细地址"},model:{value:e.formValidate.address,callback:function(t){e.$set(e.formValidate,"address",t)},expression:"formValidate.address"}})],1),e._v(" "),a("FormItem",{attrs:{label:"公寓类型",prop:"renttype"}},[a("Select",{staticClass:"input-width",attrs:{placeholder:"请选择公寓类型"},model:{value:e.formValidate.renttype,callback:function(t){e.$set(e.formValidate,"renttype",t)},expression:"formValidate.renttype"}},[a("Option",{attrs:{value:"长租"}},[e._v("长租")]),e._v(" "),a("Option",{attrs:{value:"短租"}},[e._v("短租")])],1)],1),e._v(" "),a("FormItem",{attrs:{label:"价格区间"}},[a("Row",[a("Col",{attrs:{span:"5"}},[a("FormItem",{attrs:{prop:"minprice"}},[a("Input",{staticClass:"input-width",attrs:{placeholder:"最低价格"},model:{value:e.formValidate.minprice,callback:function(t){e.$set(e.formValidate,"minprice",t)},expression:"formValidate.minprice"}})],1)],1),e._v(" "),a("Col",{staticStyle:{"text-align":"center"},attrs:{span:"2"}},[e._v("-")]),e._v(" "),a("Col",{attrs:{span:"5"}},[a("FormItem",{attrs:{prop:"maxprice"}},[a("Input",{staticClass:"input-width",attrs:{placeholder:"最高价格"},model:{value:e.formValidate.maxprice,callback:function(t){e.$set(e.formValidate,"maxprice",t)},expression:"formValidate.maxprice"}})],1)],1)],1)],1),e._v(" "),a("FormItem",{attrs:{label:"公寓设施",prop:"installation"}},[a("CheckboxGroup",{model:{value:e.formValidate.installation,callback:function(t){e.$set(e.formValidate,"installation",t)},expression:"formValidate.installation"}},[a("Checkbox",{attrs:{label:"无线WIFI"}}),e._v(" "),a("Checkbox",{attrs:{label:"厨房"}}),e._v(" "),a("Checkbox",{attrs:{label:"油烟机"}}),e._v(" "),a("Checkbox",{attrs:{label:"热水器"}}),e._v(" "),a("Checkbox",{attrs:{label:"洗衣机"}}),e._v(" "),a("Checkbox",{attrs:{label:"卫生间"}})],1)],1),e._v(" "),a("FormItem",{attrs:{label:"付款方式",prop:"paytype"}},[a("CheckboxGroup",{model:{value:e.formValidate.paytype,callback:function(t){e.$set(e.formValidate,"paytype",t)},expression:"formValidate.paytype"}},[a("Checkbox",{attrs:{label:"月付"}}),e._v(" "),a("Checkbox",{attrs:{label:"季付"}}),e._v(" "),a("Checkbox",{attrs:{label:"半年付"}}),e._v(" "),a("Checkbox",{attrs:{label:"年付"}})],1)],1),e._v(" "),a("FormItem",{attrs:{label:"公寓图片"}},[e._l(e.houseImgList,function(t){return a("div",{staticClass:"demo-upload-list"},["finished"===t.status?[a("img",{attrs:{src:t.url}}),e._v(" "),a("div",{staticClass:"demo-upload-list-cover"},[a("Icon",{attrs:{type:"ios-eye-outline"},nativeOn:{click:function(a){e.handleView(t.name)}}}),e._v(" "),a("Icon",{attrs:{type:"ios-trash-outline"},nativeOn:{click:function(a){e.handleRemove(t)}}})],1)]:[t.showProgress?a("Progress",{attrs:{percent:t.percentage,"hide-info":""}}):e._e()]],2)}),e._v(" "),a("Upload",{ref:"upload",staticStyle:{display:"inline-block",width:"58px"},attrs:{"show-upload-list":!1,"on-success":e.handleSuccess,format:["jpg","jpeg","png"],"max-size":2048,"on-format-error":e.handleFormatError,"on-exceeded-size":e.handleMaxSize,"before-upload":e.handleBeforeUpload,type:"drag",action:e.uploadUrl}},[a("div",{staticStyle:{width:"58px",height:"58px","line-height":"58px"}},[a("Icon",{attrs:{type:"camera",size:"20"}})],1)]),e._v(" "),a("Modal",{attrs:{title:"查看图片"},model:{value:e.houseImgVisible,callback:function(t){e.houseImgVisible=t},expression:"houseImgVisible"}},[e.houseImgVisible?a("img",{staticStyle:{width:"100%"},attrs:{src:e.houseImgName}}):e._e()])],2),e._v(" "),a("FormItem",{attrs:{label:"公寓长图"}},[e._l(e.longImgList,function(t){return a("div",{staticClass:"demo-upload-list"},["finished"===t.status?[a("img",{attrs:{src:t.url}}),e._v(" "),a("div",{staticClass:"demo-upload-list-cover"},[a("Icon",{attrs:{type:"ios-eye-outline"},nativeOn:{click:function(a){e.handleLongView(t.name)}}}),e._v(" "),a("Icon",{attrs:{type:"ios-trash-outline"},nativeOn:{click:function(a){e.handleLongRemove(t)}}})],1)]:[t.showProgress?a("Progress",{attrs:{percent:t.percentage,"hide-info":""}}):e._e()]],2)}),e._v(" "),a("Upload",{ref:"longUpload",staticStyle:{display:"inline-block",width:"58px"},attrs:{"show-upload-list":!1,"on-success":e.handleLongSuccess,format:["jpg","jpeg","png"],"max-size":2048,"on-format-error":e.handleFormatError,"on-exceeded-size":e.handleMaxSize,"before-upload":e.handleBeforeLongUpload,type:"drag",action:e.uploadUrl}},[a("div",{staticStyle:{width:"58px",height:"58px","line-height":"58px"}},[a("Icon",{attrs:{type:"camera",size:"20"}})],1)]),e._v(" "),a("Modal",{attrs:{title:"查看图片"},model:{value:e.longImgVisible,callback:function(t){e.longImgVisible=t},expression:"longImgVisible"}},[e.longImgVisible?a("img",{staticStyle:{width:"100%"},attrs:{src:e.longImgName}}):e._e()])],2),e._v(" "),a("FormItem",[a("Button",{attrs:{type:"primary"},on:{click:function(t){e.handleSubmit("formValidate")}}},[e._v("保存")]),e._v(" "),a("Button",{staticStyle:{"margin-left":"8px"},attrs:{type:"ghost"},on:{click:function(t){e.handleReset("formValidate")}}},[e._v("重置")])],1)],1)],1)},l=[],s={render:i,staticRenderFns:l};t.a=s}});
//# sourceMappingURL=4.build.js.map