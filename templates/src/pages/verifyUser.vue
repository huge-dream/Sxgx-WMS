<template>
  <q-page class="flex flex-center">
    <q-dialog v-model="value" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">请进行扫码验证</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input dense v-model="loginCode" autofocus type="password" hint="请使用扫码枪进行扫码识别身份"
                   @keyup.enter="loginCodeOk">
            <template v-slot:before>
              <q-icon name="filter_center_focus"/>
            </template>
          </q-input>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="取消" @click="cancel"/>
          <q-btn flat label="确定" @click="loginCodeOk"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <!--  入库  -->
    <q-dialog v-model="inDialog" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">入库</div>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="取消" @click="inDialogCancel"/>
          <q-btn flat label="入库" @click="inDialogOk"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <!--  出库  -->
    <q-dialog v-model="outDialog" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">出库</div>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="取消" @click="outDialogCancel"/>
          <q-btn flat label="出库" @click="outDialogOk"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script>
import { getauth, post, baseurl } from 'boot/axios_request'

export default {
  name: 'verifyUser',
  props: {
    // 滚动优化的选项
    value: {
      type: Boolean,
      required: false,
      default: false
    },
    type: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      loginCode: '',
      inDialog: false,
      outDialog: false,
      username: '',
      openid: ''
    }
  },
  created () {
  },
  mounted () {
  },
  methods: {
    cancel () {
      this.$emit('update:value', !this.value)
      this.loginCode = ''
    },
    // 进行登录获取token
    loginCodeOk () {
      if (!this.loginCode) {
        this.$q.notify({
          message: '请使用扫码枪进行扫码识别身份',
          icon: 'close',
          color: 'negative'
        })
        return
      }
      // 进行登录获取token
      this.$axios.post(
        baseurl + '/staff/code_login',
        { code: this.loginCode }
      ).then((res) => {
        if (res.data.status_code === 200) {
          this.$emit('update:value', !this.value)
          this.loginCode = ''
          // 弹出入库或出库需要填写信息
          if (this.type === 'in') {
            this.inDialog = true
          } else {
            this.outDialog = true
          }
          this.username = res.data.name
          this.openid = res.data.openid
          this.$q.notify({
            message: '认证成功',
            icon: 'close',
            color: 'green'
          })
        } else {
          this.$q.notify({
            message: res.data.detail,
            icon: 'close',
            color: 'negative'
          })
          this.loginCode = ''
        }
      }).catch((err) => {
        console.log(3333, err)
        this.loginCode = ''
        this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
    inDialogCancel () {
      this.inDialog = false
      this.username = ''
      this.token = ''
    },
    outDialogCancel () {
      this.outDialog = false
      this.username = ''
      this.token = ''
    },
    inDialogOk () {
      this.inDialog = false
      this.username = ''
      this.token = ''
    },
    outDialogOk () {
      this.outDialog = false
      this.username = ''
      this.token = ''
    }
  }

}
</script>

<style scoped>

</style>
