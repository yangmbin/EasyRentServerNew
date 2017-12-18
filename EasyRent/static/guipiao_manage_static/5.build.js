webpackJsonp([5],{56:function(e,t,i){"use strict";function s(e){i(76)}Object.defineProperty(t,"__esModule",{value:!0});var o=i(78),a=i(79),l=i(13),n=s,r=l(o.a,a.a,!1,n,null,null);t.default=r.exports},76:function(e,t,i){var s=i(77);"string"==typeof s&&(s=[[e.i,s,""]]),s.locals&&(e.exports=s.locals);i(3)("49364eda",s,!0)},77:function(e,t,i){t=e.exports=i(2)(void 0),t.push([e.i,".input-width{width:240px}.demo-upload-list{display:inline-block;width:60px;height:60px;text-align:center;line-height:60px;border:1px solid transparent;border-radius:4px;overflow:hidden;background:#fff;position:relative;box-shadow:0 1px 1px rgba(0,0,0,.2);margin-right:4px}.demo-upload-list img{width:100%;height:100%}.demo-upload-list-cover{display:none;position:absolute;top:0;bottom:0;left:0;right:0;background:rgba(0,0,0,.6)}.demo-upload-list:hover .demo-upload-list-cover{display:block}.demo-upload-list-cover i{color:#fff;font-size:20px;cursor:pointer;margin:0 2px}",""])},78:function(e,t,i){"use strict";t.a={data:function(){return{formValidate:{houseId:""},ruleValidate:{houseId:[{required:!0,message:"请选择对应公寓",trigger:"change"}]},imgName:"",visible:!1,houseImgList:[],houseInfoList:[],uploadUrl:this.$api.uploadUrl,getAllHouseUrl:"/manage/get_all_house_info",addBannerUrl:"/manage/add_banner"}},methods:{handleSubmit:function(e){var t=this;this.$refs[e].validate(function(e){e&&(0==t.houseImgList.length||void 0==t.houseImgList[0].path?t.$Notice.warning({title:"请上传Banner图片"}):t.$api.post(t.addBannerUrl,{image:t.houseImgList[0].path,houseid:t.formValidate.houseId},function(e){console.log(e),e.success?(t.handleReset("formValidate"),t.$refs.upload.fileList=[],t.houseImgList=t.$refs.upload.fileList,t.$Message.success(e.msg)):t.$Message.error(e.msg)}))})},handleReset:function(e){this.$refs[e].resetFields(),this.$refs.upload.fileList=[],this.houseImgList=this.$refs.upload.fileList},handleView:function(e){this.imgName=e,this.visible=!0},handleRemove:function(e){var t=this.$refs.upload.fileList;this.$refs.upload.fileList.splice(t.indexOf(e),1)},handleSuccess:function(e,t){console.log(e),console.log(t),e.success&&(t.url=this.$api.imgUrl+e.path,t.name=this.$api.imgUrl+e.path,t.path=e.path)},handleFormatError:function(e){this.$Notice.warning({title:"文件格式不正确",desc:"请选择jpg或png格式"})},handleMaxSize:function(e){this.$Notice.warning({title:"文件大小超过限制",desc:"文件大小不能大于2M"})},handleBeforeUpload:function(){var e=this.houseImgList.length<1;return e||this.$Notice.warning({title:"最多只能上传1张图片"}),e}},mounted:function(){this.houseImgList=this.$refs.upload.fileList},created:function(){var e=this;this.$api.get(this.getAllHouseUrl,null,function(t){console.log(t),e.houseInfoList=t})}}},79:function(e,t,i){"use strict";var s=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("Card",[i("p",{attrs:{slot:"title"},slot:"title"},[e._v("Banner / Banner添加")]),e._v(" "),i("Form",{ref:"formValidate",attrs:{model:e.formValidate,rules:e.ruleValidate,"label-width":80}},[i("FormItem",{attrs:{label:"Banner图片"}},[e._l(e.houseImgList,function(t){return i("div",{staticClass:"demo-upload-list"},["finished"===t.status?[i("img",{attrs:{src:t.url}}),e._v(" "),i("div",{staticClass:"demo-upload-list-cover"},[i("Icon",{attrs:{type:"ios-eye-outline"},nativeOn:{click:function(i){e.handleView(t.name)}}}),e._v(" "),i("Icon",{attrs:{type:"ios-trash-outline"},nativeOn:{click:function(i){e.handleRemove(t)}}})],1)]:[t.showProgress?i("Progress",{attrs:{percent:t.percentage,"hide-info":""}}):e._e()]],2)}),e._v(" "),i("Upload",{ref:"upload",staticStyle:{display:"inline-block",width:"58px"},attrs:{"show-upload-list":!1,"on-success":e.handleSuccess,format:["jpg","jpeg","png"],"max-size":2048,"on-format-error":e.handleFormatError,"on-exceeded-size":e.handleMaxSize,"before-upload":e.handleBeforeUpload,type:"drag",action:e.uploadUrl}},[i("div",{staticStyle:{width:"58px",height:"58px","line-height":"58px"}},[i("Icon",{attrs:{type:"camera",size:"20"}})],1)]),e._v(" "),i("Modal",{attrs:{title:"查看图片"},model:{value:e.visible,callback:function(t){e.visible=t},expression:"visible"}},[e.visible?i("img",{staticStyle:{width:"100%"},attrs:{src:e.imgName}}):e._e()])],2),e._v(" "),i("FormItem",{attrs:{label:"对应公寓",prop:"houseId"}},[i("Select",{staticClass:"input-width",attrs:{placeholder:"请选择对应公寓"},model:{value:e.formValidate.houseId,callback:function(t){e.$set(e.formValidate,"houseId",t)},expression:"formValidate.houseId"}},[e._l(e.houseInfoList,function(t){return[i("Option",{attrs:{value:t.id+""}},[e._v(e._s(t.city+t.region+t.address))])]})],2)],1),e._v(" "),i("FormItem",[i("Button",{attrs:{type:"primary"},on:{click:function(t){e.handleSubmit("formValidate")}}},[e._v("保存")]),e._v(" "),i("Button",{staticStyle:{"margin-left":"8px"},attrs:{type:"ghost"},on:{click:function(t){e.handleReset("formValidate")}}},[e._v("重置")])],1)],1)],1)},o=[],a={render:s,staticRenderFns:o};t.a=a}});
//# sourceMappingURL=5.build.js.map