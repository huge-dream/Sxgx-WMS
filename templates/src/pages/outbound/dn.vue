<template>
  <div>
    <transition appear enter-active-class="animated fadeIn">
      <q-table
        class="my-sticky-header-column-table shadow-24"
        :data="table_list"
        row-key="id"
        :separator="separator"
        :loading="loading"
        :filter="filter"
        :columns="columns"
        hide-bottom
        :pagination.sync="pagination"
        no-data-label="No data"
        no-results-label="No data you want"
        :table-style="{ height: height }"
        flat
        bordered
      >
        <template v-slot:top>
          <q-btn-group push>
            <q-btn
              v-show="
                $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                  $q.localStorage.getItem('staff_type') !== 'Customer' &&
                  $q.localStorage.getItem('staff_type') !== 'Outbound' &&
                  $q.localStorage.getItem('staff_type') !== 'StockControl'
              "
              :label="$t('new')"
              icon="add"
              @click="newFormOpen()"
            >
              <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('newtip') }}</q-tooltip>
            </q-btn>
            <q-btn
              v-show="$q.localStorage.getItem('staff_type') !== 'Supplier' && $q.localStorage.getItem('staff_type') !== 'Customer'"
              :label="$t('refresh')"
              icon="refresh"
              @click="reFresh()"
            >
              <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('refreshtip') }}</q-tooltip>
            </q-btn>
          </q-btn-group>
          <q-space />
          <q-input outlined rounded dense debounce="300" color="primary" v-model="filter" :placeholder="$t('search')" @blur="getSearchList()" @keyup.enter="getSearchList()">
            <template v-slot:append>
              <q-icon name="search" @click="getSearchList()" />
            </template>
          </q-input>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="goods_code" :props="props">{{ props.row.goods_code }}</q-td>
            <q-td key="goods_desc" :props="props">{{ props.row.goods_desc }}</q-td>
            <q-td key="bin_name" :props="props">{{ props.row.bin_name }}</q-td>
            <q-td key="number" :props="props">{{ props.row.number }}</q-td>
            <q-td key="creater" :props="props">{{ props.row.creater }}</q-td>
            <q-td key="create_time" :props="props">{{ props.row.create_time }}</q-td>
            <q-td key="update_time" :props="props">{{ props.row.update_time }}</q-td>
            <!--            <q-td key="action" :props="props" style="width: 100px">-->
            <!--              <q-btn-->
            <!--                v-show="-->
            <!--                  $q.localStorage.getItem('staff_type') !== 'Supplier' &&-->
            <!--                    $q.localStorage.getItem('staff_type') !== 'Customer' &&-->
            <!--                    $q.localStorage.getItem('staff_type') !== 'Outbound' &&-->
            <!--                    $q.localStorage.getItem('staff_type') !== 'StockControl'-->
            <!--                "-->
            <!--                round-->
            <!--                flat-->
            <!--                push-->
            <!--                color="purple"-->
            <!--                icon="edit"-->
            <!--                @click="editData(props.row)"-->
            <!--              >-->
            <!--                <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('edit') }}</q-tooltip>-->
            <!--              </q-btn>-->
            <!--              <q-btn-->
            <!--                v-show="-->
            <!--                  $q.localStorage.getItem('staff_type') !== 'Supplier' &&-->
            <!--                    $q.localStorage.getItem('staff_type') !== 'Customer' &&-->
            <!--                    $q.localStorage.getItem('staff_type') !== 'Outbound' &&-->
            <!--                    $q.localStorage.getItem('staff_type') !== 'StockControl'-->
            <!--                "-->
            <!--                round-->
            <!--                flat-->
            <!--                push-->
            <!--                color="dark"-->
            <!--                icon="delete"-->
            <!--                @click="deleteData(props.row)"-->
            <!--              >-->
            <!--                <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('delete') }}</q-tooltip>-->
            <!--              </q-btn>-->
            <!--            </q-td>-->
          </q-tr>
        </template>
      </q-table>
    </transition>
    <template>
      <div class="q-pa-lg flex flex-center">
        <q-btn v-show="pathname_previous" flat push color="purple" :label="$t('previous')" icon="navigate_before" @click="getListPrevious()">
          <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('previous') }}</q-tooltip>
        </q-btn>
        <q-btn v-show="pathname_next" flat push color="purple" :label="$t('next')" icon-right="navigate_next" @click="getListNext()">
          <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('next') }}</q-tooltip>
        </q-btn>
        <q-btn v-show="!pathname_previous && !pathname_next" flat push color="dark" :label="$t('no_data')"></q-btn>
      </div>
    </template>
    <q-dialog v-model="newForm">
      <q-card class="shadow-30" style="width: 800px">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <q-space />
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
            ref="goodsData1Qty"
            :error="!numberValid"
            autofocus
            type="number"
            min="1"
            :max="goodsData1.maxNumber"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData1Code" v-model="goodsData1.code"  @focus="getFocus(1)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData1.code,$event)" />
              <q-select
                ref="goodsData1Bin_name"
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
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData1.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData1.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
<!--          2-->
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData2.qty"
            ref="goodsData2Qty"
            @input="inputNumber"
            autofocus
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData2Code" v-model="goodsData2.code"  @focus="getFocus(2)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData2.code,$event)" />
              <q-select
                ref="goodsData2Bin_name"
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
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData2.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData2.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
<!--          3-->
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData3.qty"
            ref="goodsData3Qty"
            @input="inputNumber"
            autofocus
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData3Code" v-model="goodsData3.code"  @focus="getFocus(3)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData3.code,$event)" />
              <q-select
                ref="goodsData3Bin_name"
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
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData3.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData3.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
<!--          4-->
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData4.qty"
            ref="goodsData4Qty"
            @input="inputNumber"
            autofocus
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData4Code" v-model="goodsData4.code"  @focus="getFocus(4)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData4.code,$event)" />
              <q-select
                ref="goodsData4Bin_name"
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
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData4.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData4.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
<!--          5-->
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData5.qty"
            ref="goodsData5Qty"
            @input="inputNumber"
            autofocus
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData5Code" v-model="goodsData5.code"  @focus="getFocus(5)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData5.code,$event)" />
              <q-select
                ref="goodsData5Bin_name"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData5.bin"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData5.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData5.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
<!--          6-->
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData6.qty"
            ref="goodsData6Qty"
            @input="inputNumber"
            autofocus
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData6Code" v-model="goodsData6.code"  @focus="getFocus(6)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData6.code,$event)" />
              <q-select
                ref="goodsData6Bin_name"
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
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData6.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData6.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
<!--          7-->
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData7.qty"
            ref="goodsData7Qty"
            @input="inputNumber"
            autofocus
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData7Code" v-model="goodsData7.code"  @focus="getFocus(7)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData7.code,$event)" />
              <q-select
                ref="goodsData7Bin_name"
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
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData7.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData7.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
<!--          8-->
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData8.qty"
            ref="goodsData8Qty"
            @input="inputNumber"
            autofocus
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData8Code" v-model="goodsData8.code"  @focus="getFocus(8)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData8.code,$event)" />
              <q-select
                ref="goodsData8Bin_name"
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
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData8.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData8.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
<!--          9-->
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData9.qty"
            ref="goodsData9Qty"
            @input="inputNumber"
            autofocus
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData9Code" v-model="goodsData9.code"  @focus="getFocus(9)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData9.code,$event)" />
              <q-select
                ref="goodsData9Bin_name"
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
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData9.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData9.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
<!--          10-->
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-model.number="goodsData10.qty"
            ref="goodsData10Qty"

            autofocus
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-input outlined ref="goodsData1Code" v-model="goodsData10.code"  @focus="getFocus(10)"  autofocus :label="$t('goods.view_goodslist.goods_code')" @keyup.enter="codeEnter(goodsData10.code,$event)" />
              <q-select
                ref="goodsData10Bin_name"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="goodsData10.bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @input-value="setBinSetOptions"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item><q-item-section class="text-grey">No results</q-item-section></q-item>
                </template>
                <template v-if="goodsData10.bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="goodsData10.bin_name = ''" class="cursor-pointer" />
                </template>
              </q-select>
            </template>
          </q-input>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="isEdit ? editDataCancel() : newDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="isEdit ? editDataSubmit() : newDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="deleteForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('delete') }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">{{ $t('deletetip') }}</q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="deleteDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="deleteDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="preloadForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('confirmdelivery') }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">{{ $t('deletetip') }}</q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="preloadDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="preloadDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="presortForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('finishloading') }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">{{ $t('deletetip') }}</q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="presortDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="presortDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="viewForm">
      <q-card id="printMe">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ viewAsn }}</div>
          <q-space />
          {{ $t('inbound.asn') }}
        </q-bar>
        <q-card-section>
          <div class="row">
            <div class="col-8">
              <div class="text-h6">Sender: {{ supplier_detail.supplier_name }}</div>
              <div class="text-subtitle2">Address: {{ supplier_detail.supplier_city }}{{ supplier_detail.supplier_address }}</div>
              <div class="text-subtitle2">Tel: {{ supplier_detail.supplier_contact }}</div>
              <div class="text-h6">Receiver: {{ warehouse_detail.warehouse_name }}</div>
              <div class="text-subtitle2">Address: {{ warehouse_detail.warehouse_city }}{{ warehouse_detail.warehouse_address }}</div>
              <div class="text-subtitle2">Tel: {{ warehouse_detail.warehouse_contact }}</div>
            </div>
            <div class="col-4"><img :src="bar_code" style="width: 70%; margin-left: 15%" /></div>
          </div>
        </q-card-section>
        <q-markup-table>
          <thead>
          <tr>
            <th class="text-left">{{ $t('goods.view_goodslist.goods_code') }}</th>
            <th class="text-right">{{ $t('stock.view_stocklist.goods_qty') }}</th>
            <th class="text-right">{{ $t('inbound.view_asn.total_weight') }}</th>
            <th class="text-right">{{ $t('inbound.view_asn.total_volume') }}</th>
            <th class="text-right">{{ $t('inbound.view_asn.goods_actual_qty') }}</th>
            <th class="text-right">Comments</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(view, index) in viewprint_table" :key="index">
            <td class="text-left">{{ view.goods_code }}</td>
            <td class="text-right">{{ view.goods_qty }}</td>
            <td class="text-right">{{ view.goods_weight }}</td>
            <td class="text-right">{{ view.goods_volume }}</td>
            <td class="text-right">{{ view.goods_actual_qty }}</td>
            <td class="text-right"></td>
          </tr>
          </tbody>
        </q-markup-table>
      </q-card>
      <div style="float: right; padding: 15px 15px 15px 0"><q-btn color="primary" icon="print" v-print="printObj">print</q-btn></div>
    </q-dialog>
    <q-dialog v-model="sortedForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ sorted_list.asn_code }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-input
            dense
            outlined
            square
            debounce="500"
            disable
            readonly
            v-model="sorted_list.supplier"
            :label="$t('baseinfo.view_supplier.supplier_name')"
            style="margin-bottom: 5px"
          />
          <div v-for="(item, index) in sorted_list.goodsData" :key="index">
            <q-input dense outlined square bottom-slots type="number" v-model="item.goods_actual_qty" :label="$t('inbound.view_asn.goods_actual_qty')">
              <template v-slot:append>
                {{ item.goods_code }}
              </template>
            </q-input>
          </div>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="sortedDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="sortedDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>
<router-view />

<script>
import { getauth, postauth, putauth, deleteauth, ViewPrintAuth } from 'boot/axios_request'
import { SessionStorage, LocalStorage } from 'quasar'

export default {
  name: 'Pageasnlist',
  computed: {
    numberValid () {
      const _this = this
      return _this[`goodsData${_this.listNumber}`].qty <= _this[`goodsData${_this.listNumber}`].maxNumber
    }
  },
  data () {
    return {
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'asn/',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      table_list: [],
      viewprint_table: [],
      bar_code: '',
      warehouse_detail: {},
      supplier_list: [],
      supplier_list1: [],
      supplier_detail: {},
      columns: [
        { name: 'goods_code', required: true, label: this.$t('inbound.view_asn.goods_code'), align: 'left', field: 'goods_code' },
        { name: 'goods_desc', label: this.$t('inbound.view_asn.goods_desc'), align: 'left', field: 'goods_desc' },
        { name: 'bin_name', label: this.$t('inbound.view_asn.bin_name'), align: 'left', field: 'bin_name' },
        { name: 'number', label: this.$t('inbound.view_asn.number'), field: 'number', align: 'center' },
        { name: 'creater', label: this.$t('creater'), field: 'creater', align: 'center' },
        { name: 'create_time', label: this.$t('createtime'), field: 'create_time', align: 'center' },
        { name: 'update_time', label: this.$t('updatetime'), field: 'update_time', align: 'center' }
        // { name: 'action', label: this.$t('action'), align: 'right' }
      ],
      filter: '',
      pagination: {
        page: 1,
        rowsPerPage: '30'
      },
      newForm: false,
      options: SessionStorage.getItem('goods_code'),
      options1: [],
      isEdit: false,
      listNumber: 1,
      newAsn: { creater: '' },
      newFormData: {
        asn_code: '',
        supplier: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      },
      goodsData1: { code: '', qty: '', maxNumber: 0 },
      goodsData2: { code: '', qty: '', maxNumber: 0 },
      goodsData3: { code: '', qty: '', maxNumber: 0 },
      goodsData4: { code: '', qty: '', maxNumber: 0 },
      goodsData5: { code: '', qty: '', maxNumber: 0 },
      goodsData6: { code: '', qty: '', maxNumber: 0 },
      goodsData7: { code: '', qty: '', maxNumber: 0 },
      goodsData8: { code: '', qty: '', maxNumber: 0 },
      goodsData9: { code: '', qty: '', maxNumber: 0 },
      goodsData10: { code: '', qty: '', maxNumber: 0 },
      editid: 0,
      editFormData: {},
      sortedForm: false,
      sortedid: 0,
      sorted_list: {
        asn_code: '',
        supplier: '',
        goodsData: [],
        creater: ''
      },
      deleteForm: false,
      deleteid: 0,
      preloadForm: false,
      preloadid: 0,
      presortForm: false,
      presortid: 0,
      viewForm: false,
      viewAsn: '',
      viewid: 0,
      printObj: {
        id: 'printMe',
        popTitle: this.$t('inbound.asn')
      },
      devi: window.device,
      error1: this.$t('baseinfo.view_supplier.error1'),
      goodsListData: [],
      binSetOptions: [],
      maxNumber: 0,
      refIndex: null
    }
  },
  methods: {
    getList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth('in_out_warehouse/in_out_warehouse/?type=1', {
        })
          .then(res => {
            _this.table_list = []
            res.results.forEach(item => {
              if (item.asn_status === 1) {
                item.asn_status = _this.$t('inbound.predeliverystock')
              } else if (item.asn_status === 2) {
                item.asn_status = _this.$t('inbound.preloadstock')
              } else if (item.asn_status === 3) {
                item.asn_status = _this.$t('inbound.presortstock')
              } else if (item.asn_status === 4) {
                item.asn_status = _this.$t('inbound.sortstock')
              } else if (item.asn_status === 5) {
                item.asn_status = _this.$t('inbound.asndone')
              } else {
                item.asn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.supplier_list = res.supplier_list
            _this.supplier_list1 = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
            _this.goodsListData = res.results
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getSearchList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth('in_out_warehouse/in_out_warehouse/?type=1&search=' + _this.filter, {})
          .then(res => {
            _this.table_list = []
            res.results.forEach(item => {
              if (item.asn_status === 1) {
                item.asn_status = _this.$t('inbound.predeliverystock')
              } else if (item.asn_status === 2) {
                item.asn_status = _this.$t('inbound.preloadstock')
              } else if (item.asn_status === 3) {
                item.asn_status = _this.$t('inbound.presortstock')
              } else if (item.asn_status === 4) {
                item.asn_status = _this.$t('inbound.sortstock')
              } else if (item.asn_status === 5) {
                item.asn_status = _this.$t('inbound.asndone')
              } else {
                item.asn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.supplier_list = res.supplier_list
            _this.supplier_list1 = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getListPrevious () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_previous, {})
          .then(res => {
            _this.table_list = []
            res.results.forEach(item => {
              if (item.asn_status === 1) {
                item.asn_status = _this.$t('inbound.predeliverystock')
              } else if (item.asn_status === 2) {
                item.asn_status = _this.$t('inbound.preloadstock')
              } else if (item.asn_status === 3) {
                item.asn_status = _this.$t('inbound.presortstock')
              } else if (item.asn_status === 4) {
                item.asn_status = _this.$t('inbound.sortstock')
              } else if (item.asn_status === 5) {
                item.asn_status = _this.$t('inbound.asndone')
              } else {
                item.asn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.supplier_list = res.supplier_list
            _this.supplier_list1 = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getListNext () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_next, {})
          .then(res => {
            _this.table_list = []
            res.results.forEach(item => {
              if (item.asn_status === 1) {
                item.asn_status = _this.$t('inbound.predeliverystock')
              } else if (item.asn_status === 2) {
                item.asn_status = _this.$t('inbound.preloadstock')
              } else if (item.asn_status === 3) {
                item.asn_status = _this.$t('inbound.presortstock')
              } else if (item.asn_status === 4) {
                item.asn_status = _this.$t('inbound.sortstock')
              } else if (item.asn_status === 5) {
                item.asn_status = _this.$t('inbound.asndone')
              } else {
                item.asn_status = 'N/A'
              }
              _this.table_list.push(item)
            })
            _this.supplier_list = res.supplier_list
            _this.supplier_list1 = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    reFresh () {
      var _this = this
      _this.table_list = []
      _this.getList()
    },
    newFormOpen () {
      var _this = this
      _this.isEdit = false
      _this.goodsDataClear()
      _this.newForm = true
      _this.newAsn.creater = _this.login_name
      postauth(_this.pathname + 'list/', _this.newAsn)
        .then(res => {
          if (!res.detail) {
            _this.newFormData.asn_code = res.asn_code
          }
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
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
              goods_code: _this[goodsData].code,
              number: _this[goodsData].qty,
              bin_name: _this[goodsData].bin_name.bin_name,
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
        postauth('in_out_warehouse/in_out_warehouse/', submitForm)
          .then(res => {
            _this.table_list = []
            _this.getList()
            _this.newDataCancel()
            if (res.detail === 'success') {
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
    newDataCancel () {
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
    editData (e) {
      var _this = this
      _this.isEdit = true
      _this.goodsDataClear()
      if (e.asn_status !== _this.$t('inbound.predeliverystock')) {
        _this.$q.notify({
          message: e.asn_code + ' ASN Status Is Not ' + _this.$t('inbound.predeliverystock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.newFormData.asn_code = e.asn_code
        _this.newFormData.supplier = e.supplier
        getauth(_this.pathname + 'detail/?asn_code=' + e.asn_code).then(res => {
          _this.newForm = true
          _this.editid = e.id
          res.results.forEach((detail, index) => {
            _this[`goodsData${index + 1}`] = { code: detail.goods_code, qty: detail.goods_qty }
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
      } else {
        cancelRequest = true
        _this.$q.notify({
          message: 'Please Enter The Supplier',
          icon: 'close',
          color: 'negative'
        })
      }
      if (!cancelRequest) {
        putauth(_this.pathname + 'detail/', _this.newFormData)
          .then(res => {
            _this.table_list = []
            _this.editDataCancel()
            _this.getList()
            if (res.detail === 'success') {
              _this.$q.notify({
                message: 'Success Edit Data',
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
    editDataCancel () {
      var _this = this
      _this.newForm = false
      _this.editid = 0
      _this.newFormData = {
        asn_code: '',
        supplier: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    deleteData (e) {
      var _this = this
      if (e.asn_status !== _this.$t('inbound.predeliverystock')) {
        _this.$q.notify({
          message: e.asn_code + ' ASN Status Is Not ' + _this.$t('inbound.predeliverystock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.deleteForm = true
        _this.deleteid = e.id
      }
    },
    deleteDataSubmit () {
      var _this = this
      deleteauth(_this.pathname + 'list/' + _this.deleteid + '/')
        .then(res => {
          _this.table_list = []
          _this.deleteDataCancel()
          _this.getList()
          if (!res.data) {
            _this.$q.notify({
              message: 'Success Delete Data',
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
    },
    deleteDataCancel () {
      var _this = this
      _this.deleteForm = false
      _this.deleteid = 0
    },
    preloadData (e) {
      var _this = this
      if (e.asn_status !== _this.$t('inbound.predeliverystock')) {
        _this.$q.notify({
          message: e.asn_code + ' ASN Status Is Not ' + _this.$t('inbound.predeliverystock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.preloadForm = true
        _this.preloadid = e.id
      }
    },
    preloadDataSubmit () {
      var _this = this
      postauth(_this.pathname + 'preload/' + _this.preloadid + '/', {})
        .then(res => {
          _this.table_list = []
          _this.preloadDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Confirm ASN Delivery',
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
    },
    preloadDataCancel () {
      var _this = this
      _this.preloadForm = false
      _this.preloadid = 0
    },
    presortData (e) {
      var _this = this
      if (e.asn_status !== _this.$t('inbound.preloadstock')) {
        _this.$q.notify({
          message: e.asn_code + ' ASN Status Is Not ' + _this.$t('inbound.preloadstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.presortForm = true
        _this.presortid = e.id
      }
    },
    presortDataSubmit () {
      var _this = this
      postauth(_this.pathname + 'presort/' + _this.presortid + '/', {})
        .then(res => {
          _this.table_list = []
          _this.presortDataCancel()
          _this.getList()
          if (!res.detail) {
            _this.$q.notify({
              message: 'Success Load ASN',
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
    },
    presortDataCancel () {
      var _this = this
      _this.presortForm = false
      _this.presortid = 0
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
      const obj = _this.binSetOptions.filter(item => {
        if (item.bin_name === val) {
          return item
        }
      })
      if (obj.length > 0) {
        _this[`goodsData${this.listNumber}`].maxNumber = obj[0].goods_qty
      }
    },
    setModel (val) {
      const _this = this
      _this.newFormData.supplier = val
    },
    filterFnS (val, update, abort) {
      var _this = this
      update(() => {
        const needle = val.toLocaleLowerCase()
        const data_filter = _this.supplier_list1
        _this.supplier_list = data_filter.filter(v => v.toLocaleLowerCase().indexOf(needle) > -1)
      })
    },
    sortedData (e) {
      var _this = this
      _this.goodsDataClear()
      if (e.asn_status !== _this.$t('inbound.presortstock')) {
        _this.$q.notify({
          message: e.asn_code + ' ASN Status Is Not ' + _this.$t('inbound.presortstock'),
          icon: 'close',
          color: 'negative'
        })
      } else {
        _this.sorted_list.asn_code = e.asn_code
        _this.sorted_list.supplier = e.supplier
        getauth(_this.pathname + 'detail/?asn_code=' + e.asn_code).then(res => {
          _this.sortedForm = true
          _this.sortedid = e.id
          _this.sorted_list.goodsData = res.results
        })
      }
    },
    sortedDataSubmit () {
      var _this = this
      _this.sorted_list.creater = _this.login_name
      postauth(_this.pathname + 'sorted/' + _this.sortedid + '/', _this.sorted_list)
        .then(res => {
          _this.table_list = []
          _this.sortedDataCancel()
          _this.getList()
          if (!res.data) {
            _this.$q.notify({
              message: 'Success Sorted ASN',
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
    },
    sortedDataCancel () {
      var _this = this
      _this.sortedForm = false
      _this.sortedid = 0
      _this.sorted_list = {
        asn_code: '',
        supplier: '',
        goodsData: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    viewData (e) {
      var _this = this
      ViewPrintAuth(_this.pathname + 'viewprint/' + e.id + '/').then(res => {
        _this.viewprint_table = res.asn_detail
        _this.warehouse_detail = res.warehouse_detail
        _this.supplier_detail = res.supplier_detail
        _this.viewAsn = e.asn_code
        var QRCode = require('qrcode')
        QRCode.toDataURL(e.bar_code, [
          {
            errorCorrectionLevel: 'H',
            mode: 'byte',
            version: '2',
            type: 'image/jpeg'
          }
        ])
          .then(url => {
            _this.bar_code = url
          })
          .catch(err => {
            console.error(err)
          })
        _this.viewForm = true
      })
    },
    /**
     * 商品编码enter事件
     */
    codeEnter (val, event) {
      const _this = this
      if (val) {
        _this.$refs[`goodsData${_this.listNumber}Bin_name`].focus()
        getauth('in_out_warehouse/in_out_warehouse/code_to_detail/?goods_code=' + val).then(res => {
          // console.log(res)
          if (res.length === 0) {
            _this.$q.notify({
              message: '未查询到该商品编码',
              icon: 'close',
              color: 'negative'
            })
            _this[`goodsData${_this.listNumber}`].code = ''
            const refName = `goodsData${_this.listNumber}Code`
            _this.$refs[refName].focus()
          } else {
            _this.binSetOptions = res
          }
        })
      } else {
        _this.$q.notify({
          message: '商品编码不能为空',
          icon: 'close',
          color: 'negative'
        })
      }
    },
    /**
     * 数量输入事件
     */
    inputNumber (val) {
      const _this = this
      if (Number(val) < 0) {
        _this[`goodsData${_this.listNumber}`].qty = null
        _this.$q.notify({
          message: '出库数量必须大于0',
          icon: 'close',
          color: 'negative'
        })
      }
      if (Number(val) > _this.maxNumber) {
        _this[`goodsData${_this.listNumber}`].qty = null
        _this.$q.notify({
          message: `当前库位库存数量为:${_this.maxNumber}`,
          icon: 'close',
          color: 'negative'
        })
      }
    }
  },
  created () {
    var _this = this
    if (LocalStorage.has('openid')) {
      _this.openid = LocalStorage.getItem('openid')
    } else {
      _this.openid = ''
      LocalStorage.set('openid', '')
    }
    if (LocalStorage.has('login_name')) {
      _this.login_name = LocalStorage.getItem('login_name')
    } else {
      _this.login_name = ''
      LocalStorage.set('login_name', '')
    }
    if (LocalStorage.has('auth')) {
      _this.authin = '1'
      _this.table_list = []
      _this.getList()
    } else {
      _this.authin = '0'
    }
    if (SessionStorage.has('goods_code')) {
    } else {
      SessionStorage.set('goods_code', [])
    }
  },
  mounted () {
    var _this = this
    if (_this.$q.platform.is.electron) {
      _this.height = String(_this.$q.screen.height - 290) + 'px'
    } else {
      _this.height = _this.$q.screen.height - 290 + '' + 'px'
    }
  },
  updated () {},
  destroyed () {}
}
</script>
