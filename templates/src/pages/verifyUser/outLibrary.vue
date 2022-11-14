<template>
  <q-page class="flex flex-center">
    <q-dialog v-model="newForm" persistent>
      <q-card class="shadow-24" style="width: 700px;height: 425px;">
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
            v-model.number="goodsData1.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData1.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(1)"
                @input-value="setOptions"
                @filter="filterFn"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData1.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData1.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData1.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData1.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData1.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData2.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData2.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(2)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData2.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData2.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData2.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData2.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData2.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData3.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData3.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(3)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData3.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData3.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData3.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData3.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData3.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData4.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData4.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(4)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData4.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData4.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData4.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData4.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData4.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData5.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData5.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(5)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData5.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData5.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData5.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData5.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData5.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData6.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData6.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(6)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData6.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData6.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData6.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData6.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData6.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData7.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData7.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(7)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData7.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData7.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData7.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData7.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData7.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData8.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData8.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(8)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData8.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData8.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData8.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData8.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData8.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData9.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData9.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(9)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData9.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData9.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData9.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData9.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData9.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData10.qty"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
            @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
          >
            <template v-slot:before>
              <q-select
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData10.code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(10)"
                @input-value="setOptions"
                @filter="filterFn"
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData10.code" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData10.code = ''" class="cursor-pointer"/>
                </template>
              </q-select>
              <q-select
                ref="one"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData10.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"

                @focus="getFocus(1)"
                @input-value="setBinSetOptions"
                autofocus
                @keyup.enter="isEdit ? editDataSubmit() : newDataSubmit()"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="goodsData10.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData10.bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px"
                 @click="isEdit ? editDataCancel() : newDataCancel()">{{ $t('cancel') }}
          </q-btn>
          <q-btn color="primary" @click="isEdit ? editDataSubmit() : newDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { getauth, postauth, putauth } from 'boot/axios_request'
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
      goodsData1: { code: '', qty: '' },
      goodsData2: { code: '', qty: '' },
      goodsData3: { code: '', qty: '' },
      goodsData4: { code: '', qty: '' },
      goodsData5: { code: '', qty: '' },
      goodsData6: { code: '', qty: '' },
      goodsData7: { code: '', qty: '' },
      goodsData8: { code: '', qty: '' },
      goodsData9: { code: '', qty: '' },
      goodsData10: { code: '', qty: '' },
      isEdit: false,
      options: SessionStorage.getItem('goods_code'),
      options1: [],
      goodsListData: [],
      binSetOptions: []
    }
  },
  created () {
  },
  mounted () {
  },
  methods: {
    newDataSubmit () {
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
        if (_this[goodsData].code !== '' && _this[goodsData].qty !== '') {
          if (_this[goodsData].qty < 1) {
            cancelRequest = true
            _this.$q.notify({
              message: 'Total Quantity Must Be > 0',
              icon: 'close',
              color: 'negative'
            })
          } else {
            _this.newFormData.goods_code.push(_this[goodsData].code)
            _this.newFormData.goods_qty.push(_this[goodsData].qty)
            const dict = {
              good: _this[goodsData].good,
              number: _this[goodsData].qty,
              binset: _this[goodsData].bin,
              type: 1,
              creater: _this.login_name
            }
            submitForm.push(dict)
          }
          goodsDataCheck += 1
        }
      }
      if (goodsDataCheck === 0) {
        cancelRequest = true
        _this.$q.notify({
          message: 'Please Enter The Goods & Qty',
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
        console.log(submitForm)
        postauth('in_out_warehouse/in_out_warehouse/', submitForm)
          .then(res => {
            this.table_list = []
            _this.newDataCancel()
            _this.$q.notify({
              message: 'Success Create',
              icon: 'check',
              color: 'green'
            })
          })
          .catch(err => {
            console.log(111, err)
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      }
    },
    editDataSubmit () {
      var _this = this
      _this.newFormData.creater = _this.login_name
      let cancelRequest = false
      if (_this.newFormData.supplier !== '') {
        _this.newFormData.goods_code = []
        _this.newFormData.goods_qty = []
        let goodsDataCheck = 0
        for (let i = 0; i < 10; i++) {
          const goodsData = `goodsData${i + 1}`
          if (_this[goodsData].code !== '' && _this[goodsData].qty !== '') {
            if (_this[goodsData].qty < 1) {
              cancelRequest = true
              _this.$q.notify({
                message: 'Total Quantity Must Be > 0',
                icon: 'close',
                color: 'negative'
              })
            } else {
              _this.newFormData.goods_code.push(_this[goodsData].code)
              _this.newFormData.goods_qty.push(_this[goodsData].qty)
            }
            goodsDataCheck += 1
          }
        }
        if (goodsDataCheck === 0) {
          cancelRequest = true
          _this.$q.notify({
            message: 'Please Enter The Goods & Qty',
            icon: 'close',
            color: 'negative'
          })
        }
      }
      if (!cancelRequest) {
        putauth(_this.pathname + 'detail/', _this.newFormData)
          .then(res => {
            this.table_list = []
            this.newDataCancel()
            _this.$q.notify({
              message: '出库成功',
              icon: 'check',
              color: 'green'
            })
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
    setOptions (val) {
      const _this = this
      if (!val) {
        this[`goodsData${this.listNumber}`].code = ''
      }
      const needle = val.toLowerCase()
      getauth('goods/?goods_code__icontains=' + needle).then(res => {
        const goodscodelist = []
        for (let i = 0; i < res.results.length; i++) {
          goodscodelist.push(res.results[i].goods_code)
          if (this.listNumber) {
            if (res.results[i].goods_code === val) {
              this[`goodsData${this.listNumber}`].good = res.results[i].id
            }
          }
        }
        _this.options1 = goodscodelist
      })
    },
    filterFn (val, update, abort) {
      if (val.length < 1) {
        abort()
        return
      }
      update(() => {
        this.options = this.options1
      })
    },
    setBinSetOptions (val) {
      const _this = this
      if (!val) {
        this[`goodsData${this.listNumber}`].bin = ''
      }
      const needle = val.toLowerCase()
      getauth('/binset/?empty_label=true&bin_name__icontains=' + needle).then(res => {
        for (let i = 0; i < res.results.length; i++) {
          if (this.listNumber) {
            if (res.results[i].bin_name === val) {
              this[`goodsData${this.listNumber}`].bin = res.results[i].id
            }
          }
        }
        _this.binSetOptions = res.results
      })
    },
    newDataCancel () {
      this.$emit('cancel', !this.value)
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
    }
  }

}
</script>

<style scoped>

</style>
