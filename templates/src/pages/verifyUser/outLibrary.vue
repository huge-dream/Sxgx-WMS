<template>
  <q-page class="flex flex-center">
    <q-dialog v-model="newForm" persistent maximized>
      <q-card class="shadow-24" style="width: 700px;height: 445px;">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
           <div>出库</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width:700px" class="scroll">
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-for="(item,index) in tableFromNum"
            :readonly="isGuide!==2"
            v-model.number="data[`goodsData${index+1}`].qty"
            :key="index"
            type="number"
            :label="isGuide===2?'已取货数量':'待找货'"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-select
                :ref="`goodsData${index}Code`"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="data[`goodsData${index+1}`].code"
                :label="'商品'"
                :options="options"
                :disable="isGuide===2"
                option-value="goods_code"
                option-label="goods_code"
                @focus="getFocus(index+1)"
                @input-value="setModel($event,index)"
                autofocus
                @filter="filterFn"
                @blur="goodsCodeEnter(index)"
                @keyup.enter="goodsCodeEnter(index)"
              >
                <template v-slot:option="scope">
                  <q-item
                    v-bind="scope.itemProps"
                    v-on="scope.itemEvents"
                  >
                    <q-item-section>
                      <q-item-label v-html="scope.opt.goods_code" />
                      <q-item-label caption>{{ scope.opt.goods_desc }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </template>
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
              </q-select>
              <q-select
                :ref="`goodsData${index}BinName`"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                :disable="isGuide===2"
                v-model="data[`goodsData${index+1}`].bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @filter="filterFnBinName"
                @focus="getFocus(index+1)"
                autofocus
              >
                <template v-slot:option="scope">
                  <q-item
                    v-bind="scope.itemProps"
                    v-on="scope.itemEvents"
                  >
                    <q-item-section>
                      <q-item-label v-html="scope.opt.bin_name" />
                      <q-item-label caption>当前库位数量: {{ scope.opt.goods_qty }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </template>
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="data[`goodsData${index+1}`].bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="data[`goodsData${index+1}`].bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
            <template v-slot:after>
              <span v-if="data[`goodsData${index+1}`] && data[`goodsData${index+1}`].bin_name && data[`goodsData${index+1}`].bin_name.light_guide_sign">
                <!--  0 待指引；2指引完成；1指引中              -->
                <q-icon name="sync" v-show="data[`goodsData${index+1}`].bin_name.complete === 1" style="color:#58BD6A;animation: spin 1s linear infinite;" @click="loopClick(index)" class="cursor-pointer"/>
                <q-icon name="check_circle" v-show="data[`goodsData${index+1}`].bin_name.complete === 2" style="color:#58BD6A;" class="cursor-pointer"/>
                <q-icon name="cancel" v-show="data[`goodsData${index+1}`].bin_name.complete === 3" style="color:red;" class="cursor-pointer"/>
                <q-icon color="primary" v-show="!data[`goodsData${index+1}`].bin_name.complete" name="hourglass_top" class="cursor-pointer"/>
              </span>
            </template>
          </q-input>
        </q-card-section>
        <div style="float: left;left: 10px;" v-if="isGuide===2">
          <q-input v-model="scanInput" label="请使用条码枪进行扫码核验出库商品" autofocus :dense="false" ref="scanInput" style="width: 300px;height: 10px;margin-left: 20px;" @blur="scanInputBlur" @keyup.enter="scanInputEnter">
            <template v-slot:prepend>
              <q-icon name="photo_camera" />
            </template>
          </q-input>
        </div>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px"
                 @click="isEdit ? editDataCancel() : newDataCancel()">{{ $t('cancel') }}
          </q-btn>
          <q-btn color="primary" @click="newDataSubmit('guide')" style="margin-right: 25px" :loading="isGuide===1">开始光指引</q-btn>
          <q-btn color="primary" @click="newDataSubmit()" :disable="isGuide!==2">出库保存</q-btn>
        </div>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { SessionStorage } from 'quasar'

export default {
  name: 'outLibrary',
  props: {
    // 滚动优化的选项
    login_name: {
      type: String,
      required: false
    },
    openid: {
      type: String,
      required: true
    },
    getauth: {
      type: Function,
      required: true
    },
    postauth: {
      type: Function,
      required: true
    },
    putauth: {
      type: Function,
      required: true
    }
  },
  data () {
    return {
      authin: '0',
      pathname: 'asn/',
      pathname_previous: '',
      pathname_next: '',
      newForm: true,
      newFormData: {
        asn_code: '',
        supplier: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      },
      table_list: [],
      data: {
        goodsData1: { code: '', qty: '' },
        goodsData2: { code: '', qty: '' },
        goodsData3: { code: '', qty: '' },
        goodsData4: { code: '', qty: '' },
        goodsData5: { code: '', qty: '' },
        goodsData6: { code: '', qty: '' },
        goodsData7: { code: '', qty: '' },
        goodsData8: { code: '', qty: '' },
        goodsData9: { code: '', qty: '' },
        goodsData10: { code: '', qty: '' }
      },
      isEdit: false,
      options: SessionStorage.getItem('goods_code'),
      options1: [],
      goodsListData: [],
      binSetOptions: [],
      allBinSetOptions: [],
      optionsBinName: [],
      tableFromNum: 10,
      optionsGoodsCode: [],
      isWriteOff: false, // 是否核销
      isGuide: 0, // 是否指引完成 0 待进行；1 进行中；2完成
      scanInput: '',
      setIntervalIndex: 0,
      setInterval: false
    }
  },
  created () {
    this.getAllGoodsCode()
  },
  mounted () {
  },
  methods: {
    guideSubmit () {
      let isGuide = 2
      for (let index = 0; index < this.tableFromNum; index++) {
        if (this.data[`goodsData${index + 1}`] && this.data[`goodsData${index + 1}`].bin_name) {
          if (this.data[`goodsData${index + 1}`].bin_name.complete !== 2 && this.data[`goodsData${index + 1}`].bin_name.complete !== 3) {
            this.data[`goodsData${index + 1}`].bin_name.complete = 1
            if (!this.setInterval) {
              this.setInterval = true
              this.setIntervalIndex = index
              this.getResultsSerial(2)
            }
            isGuide = 1
          }
        }
      }
      this.isGuide = isGuide
      if (this.isGuide !== 1) {
        this.$q.notify({
          message: '光指引完毕',
          icon: 'check',
          color: 'green'
        })
        this.$refs.scanInput.focus()
      }
    },
    getResultsSerial (state = 2) {
      const lightGuideSign = this.data[`goodsData${this.setIntervalIndex + 1}`] && this.data[`goodsData${this.setIntervalIndex + 1}`].bin_name && this.data[`goodsData${this.setIntervalIndex + 1}`].bin_name.light_guide_sign
      this.getauth('in_out_warehouse/in_out_warehouse/get_serial/?light_guide_sign=' + lightGuideSign + '&state=' + state).then(res => {
        if (res.state === -1) {
          this.data[`goodsData${this.setIntervalIndex + 1}`].bin_name.complete = 3
          this.setIntervalIndex = 0
          this.setInterval = false
          this.guideSubmit()
          this.$q.notify({
            message: '光指引设备调用失败',
            icon: 'close',
            color: 'negative'
          })
          this.$refs.scanInput.focus()
        } else if (res.state === 1) {
          // 返回0不操作，返回1进行下一个判断
          this.data[`goodsData${this.setIntervalIndex + 1}`].bin_name.complete = 2
          this.setIntervalIndex = 0
          this.setInterval = false
          this.guideSubmit()
        }
      }).catch((err) => {
        console.log('err', err)
        this.setIntervalIndex = 0
        this.setInterval = false
        this.guideSubmit()
      })
    },
    goodsCodeEnter (index) {
      if (!this.data[`goodsData${index + 1}`].code) return
      let data = this.data[`goodsData${index + 1}`].code
      if (Object.prototype && Object.prototype.toString.call(data) === '[object Object]') {
        this.data[`goodsData${index + 1}`].code = data.goods_code
        data = data.goods_code
      }
      if (this.optionsGoodsCode.indexOf(data) !== -1) {
        this.$refs[`goodsData${index}BinName`][0].showPopup()
        this.getauth('/binset/?max_page=999&empty_label=true&type=out&goods_code=' + data.toLowerCase()).then(res => {
          const binNameList = []
          for (let i = 0; i < res.results.length; i++) {
            binNameList.push(res.results[i].bin_name)
          }
          this.optionsBinName = binNameList
          this.binSetOptions = []
          this.allBinSetOptions = res.results
        })
      } else {
        this.$refs[`goodsData${index}Code`][0].focus()
        this.$q.notify({
          message: '未查询到该商品编码',
          icon: 'close',
          color: 'negative'
        })
      }
    },
    // 停止光指引
    loopClick (index) {
      this.data[`goodsData${index + 1}`].bin_name.complete = 3
      this.setIntervalIndex = 0
      this.isGuide = 2
      this.$emit('cancelGetAxios')
      // this.guideSubmit()
    },
    newDataSubmit (type) {
      var _this = this
      _this.newFormData.creater = _this.login_name
      let cancelRequest = false
      const submitForm = [] // 用于提交的form
      // if (_this.newFormData.supplier !== '') {
      _this.newFormData.goods_code = []
      _this.newFormData.goods_qty = []
      let goodsDataCheck = 0
      for (let i = 0; i < 10; i++) {
        const goodsData = `goodsData${i + 1}`
        if (type === undefined && _this.data[goodsData].qty !== '' && _this.data[goodsData].qty < 1) {
          cancelRequest = true
          _this.$q.notify({
            message: '总数量必须大于0',
            icon: 'close',
            color: 'negative'
          })
        }
        if (_this.data[goodsData].code !== '' && _this.data[goodsData].bin_name && _this.data[goodsData].bin_name.bin_name !== '') {
          _this.newFormData.goods_code.push(_this.data[goodsData].code)
          _this.newFormData.goods_qty.push(_this.data[goodsData].qty)
          const dict = {
            goods_code: _this.data[goodsData].code,
            number: _this.data[goodsData].qty,
            bin_name: _this.data[goodsData].bin_name && _this.data[goodsData].bin_name.bin_name,
            type: 1,
            creater: _this.login_name
          }
          submitForm.push(dict)
          goodsDataCheck += 1
        }
      }
      if (goodsDataCheck === 0) {
        cancelRequest = true
        _this.$q.notify({
          message: '请输入货物和数量',
          icon: 'close',
          color: 'negative'
        })
      }
      // } else {
      //   cancelRequest = true
      //   _this.$q.notify({
      //     message: 'Please Enter The Supplier',
      //     icon: 'close',
      //     color: 'negative'
      //   })
      // }
      if (!cancelRequest) {
        if (type) {
          this.guideSubmit()
          return
        }
        this.postauth('in_out_warehouse/in_out_warehouse/', submitForm)
          .then(res => {
            this.table_list = []
            if (res.status_code !== 500) {
              _this.newDataCancel()
              _this.$q.notify({
                message: 'Success Create',
                icon: 'check',
                color: 'green'
              })
            }
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      }
    },
    getFocus (number) {
      this.listNumber = number
    },
    filterFn (val, update, abort) {
      if (val && this.optionsGoodsCode && this.optionsGoodsCode.indexOf(val) !== -1) {
        abort()
        return
      }
      if (val) {
        let newAllOptions = []
        newAllOptions = this.allOptions.filter(res => {
          return res.goods_code.toLowerCase().indexOf(val.toLowerCase()) !== -1 || res.goods_desc.toLowerCase().indexOf(val.toLowerCase()) !== -1
        })
        update(() => {
          this.options = newAllOptions
        })
        return
      }
      update(() => {
        this.options = this.allOptions
      })
    },
    filterFnBinName (val, update, abort) {
      if (val && this.optionsBinName && this.optionsBinName.indexOf(val) !== -1) {
        abort()
        return
      }
      if (val) {
        let newAllOptions = []
        newAllOptions = this.allBinSetOptions.filter(res => {
          return res.bin_name.toLowerCase().indexOf(val.toLowerCase()) !== -1
        })
        update(() => {
          this.binSetOptions = newAllOptions
        })
        return
      }
      update(() => {
        this.binSetOptions = this.allBinSetOptions
      })
    },
    newDataCancel () {
      this.$emit('cancel', !this.value)
      this.$emit('cancelGetAxios')
      var _this = this
      _this.newForm = false
      _this.newFormData = {
        asn_code: '',
        supplier: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    goodsDataClear () {
      var _this = this
      for (let i = 1; i <= 10; i++) {
        _this[`goodsData${i}`] = { code: '', qty: '' }
      }
    },
    setModel (val, index) {
      this.data[`goodsData${index + 1}`].qty = val ? 0 : ''
      this.data[`goodsData${index + 1}`].code = val
    },
    // 获取全部商品信息
    getAllGoodsCode () {
      this.getauth('goods/').then(res => {
        const goodscodelist = []
        for (let i = 0; i < res.results.length; i++) {
          goodscodelist.push(res.results[i].goods_code)
        }
        this.optionsGoodsCode = goodscodelist
        this.options = []
        this.allOptions = res.results
      })
    },
    scanInputBlur () {
      if (this.isGuide === 2) {
        this.$refs.scanInput.focus()
      }
    },
    scanInputEnter () {
      // 进行匹配是否存在该商品
      if (this.optionsGoodsCode.indexOf(this.scanInput) !== -1) {
        // 进行数量叠加
        let goBeyond = false
        for (const ele in this.data) {
          if (this.data[ele].code === this.scanInput) {
            if (this.data[ele].qty === '') {
              this.data[ele].qty = 0
              goBeyond = false
            } else {
              if (this.data[ele].bin_name.goods_qty >= this.data[ele].qty + 1) {
                this.data[ele].qty += 1
                goBeyond = false
              } else {
                goBeyond = true
              }
              break
            }
          }
        }
        this.scanInput = ''
        if (goBeyond) {
          this.$q.notify({
            message: '超出该库存数量',
            icon: 'close',
            color: 'negative'
          })
          return
        }
        this.$q.notify({
          message: '扫码成功，数量已叠加',
          icon: 'check',
          color: 'green'
        })
      } else {
        // 提示错误，清空值
        this.scanInput = ''
        this.$q.notify({
          message: '商品条码无效，请重新扫码',
          icon: 'close',
          color: 'negative'
        })
      }
    }
  }

}
</script>

<style scoped>

</style>
